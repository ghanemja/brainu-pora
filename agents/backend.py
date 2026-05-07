"""
Pluggable model backends.

Supports calling specialist agents from either:
  - Anthropic API (Claude Haiku/Sonnet)
  - Local HuggingFace transformer (your fine-tuned Gemma + LoRA adapter)
  - Ollama / vLLM (future)

The orchestrator uses Backend.complete() — backends handle their own
auth, batching, retries.

Configure the default per-specialist via the `base_model` field in
Specialist:
  base_model="claude-haiku-4-5"               → AnthropicBackend
  base_model="hf:jang0294/gemma-2-9b-..."     → HuggingFaceBackend
  base_model="hf:google/gemma-2-9b-it"        → HuggingFaceBackend
"""

from __future__ import annotations

import os
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass


class Backend(ABC):
    name: str

    @abstractmethod
    def complete(self, system: str, user: str, max_tokens: int = 1500) -> str:
        ...


# ── Anthropic ────────────────────────────────────────────────────────────────

class AnthropicBackend(Backend):
    """Wraps Claude API. Default for the prototype."""
    def __init__(self, model: str = "claude-haiku-4-5"):
        self.name = model
        self.model = model
        self._client = None

    def _client_(self):
        if self._client is None:
            import anthropic
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise RuntimeError("ANTHROPIC_API_KEY not set")
            self._client = anthropic.Anthropic(api_key=api_key)
        return self._client

    def complete(self, system: str, user: str, max_tokens: int = 1500,
                 retries: int = 5) -> str:
        client = self._client_()
        for attempt in range(retries):
            try:
                msg = client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    system=system,
                    messages=[{"role": "user", "content": user}],
                )
                return msg.content[0].text
            except Exception as e:
                err = str(e)
                if "rate_limit" in err or "429" in err or "overloaded" in err:
                    time.sleep(10 * (attempt + 1))
                    continue
                raise
        raise RuntimeError(f"Anthropic call failed after {retries} retries")


# ── HuggingFace Inference Endpoints (managed, no local GPU needed) ──────────

class HFEndpointBackend(Backend):
    """Calls a HuggingFace Inference Endpoint over HTTPS.

    Why this is the right fit for serving fine-tuned LoRA adapters:
      - HF Endpoints natively support PEFT adapters via the model card config
      - Scales to zero when idle (no idle billing)
      - One A10G endpoint runs Gemma 2 9B + LoRA at ~$0.50-1.50/hr
      - No local GPU needed — works from your Mac, Colab, anywhere

    To create endpoints:
      1. Go to https://ui.endpoints.huggingface.co/
      2. New endpoint → pick model (e.g. jang0294/gemma-2-9b-aero-lora)
      3. Hardware: A10G or L4, Region: us-east-1, Scale-to-zero: 5 min
      4. Copy the endpoint URL (looks like
         https://abc123.us-east-1.aws.endpoints.huggingface.cloud)
      5. Set in agents/config_specialists.json under "specialists_after_phase5"

    Resolver string format:
      "hf-endpoint:<URL>"
    """
    def __init__(self, endpoint_url: str, hf_token: str | None = None):
        self.name = endpoint_url
        self.endpoint_url = endpoint_url.rstrip("/")
        self.hf_token = hf_token or os.environ.get("HF_TOKEN")
        if not self.hf_token:
            raise RuntimeError("HFEndpointBackend needs HF_TOKEN")

    def complete(self, system: str, user: str, max_tokens: int = 1500,
                 retries: int = 3) -> str:
        import requests
        # Use Gemma chat template formatting via a simple wrapper
        prompt = (
            f"<start_of_turn>user\n{system}\n\n{user}<end_of_turn>\n"
            f"<start_of_turn>model\n"
        )
        for attempt in range(retries):
            try:
                r = requests.post(
                    self.endpoint_url,
                    headers={
                        "Authorization": f"Bearer {self.hf_token}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "inputs": prompt,
                        "parameters": {
                            "max_new_tokens": max_tokens,
                            "temperature": 0.0,
                            "do_sample": False,
                            "return_full_text": False,
                        },
                    },
                    timeout=120,
                )
                if r.status_code == 503:  # endpoint cold-starting
                    time.sleep(15)
                    continue
                r.raise_for_status()
                payload = r.json()
                if isinstance(payload, list) and payload:
                    return payload[0].get("generated_text", "")
                if isinstance(payload, dict):
                    return payload.get("generated_text", str(payload))
                return str(payload)
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(5 * (attempt + 1))
                    continue
                raise
        raise RuntimeError("HFEndpoint call failed after retries")


# ── Local HuggingFace transformers ──────────────────────────────────────────

class HuggingFaceBackend(Backend):
    """Wraps a local HuggingFace transformer + tokenizer.
    Lazy-loads model weights on first call (so importing this module is cheap).

    For per-specialist LoRA adapters (Phase 5):
        backend = HuggingFaceBackend(
            base_model="google/gemma-2-9b-it",
            adapter="jang0294/gemma-aero-adapter",
        )
    """

    def __init__(
        self,
        base_model: str,
        adapter: str | None = None,
        device: str = "cuda",
        load_in_4bit: bool = True,
    ):
        self.name = base_model + (f"+{adapter}" if adapter else "")
        self.base_model = base_model
        self.adapter = adapter
        self.device = device
        self.load_in_4bit = load_in_4bit
        self._model = None
        self._tokenizer = None

    def _load(self):
        if self._model is not None:
            return
        from transformers import AutoModelForCausalLM, AutoTokenizer
        kwargs = {"device_map": "auto"}
        if self.load_in_4bit:
            from transformers import BitsAndBytesConfig
            import torch
            kwargs["quantization_config"] = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
            )
            kwargs["torch_dtype"] = torch.bfloat16
        self._tokenizer = AutoTokenizer.from_pretrained(self.base_model)
        if self._tokenizer.pad_token is None:
            self._tokenizer.pad_token = self._tokenizer.eos_token
        self._model = AutoModelForCausalLM.from_pretrained(self.base_model, **kwargs)
        if self.adapter:
            from peft import PeftModel
            self._model = PeftModel.from_pretrained(self._model, self.adapter)

    def complete(self, system: str, user: str, max_tokens: int = 1500) -> str:
        self._load()
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
        prompt = self._tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        import torch
        inputs = self._tokenizer(prompt, return_tensors="pt").to(self._model.device)
        with torch.inference_mode():
            out = self._model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=False,
                pad_token_id=self._tokenizer.pad_token_id,
            )
        text = self._tokenizer.decode(out[0][inputs["input_ids"].shape[1]:],
                                       skip_special_tokens=True)
        return text


# ── Resolver ─────────────────────────────────────────────────────────────────

def get_backend(spec_str: str) -> Backend:
    """Resolve a Specialist.base_model string to a Backend.

    Conventions:
      "claude-haiku-4-5"           → AnthropicBackend
      "claude-sonnet-4-5"          → AnthropicBackend
      "hf:google/gemma-2-9b-it"    → HuggingFaceBackend (local, needs CUDA)
      "hf:base+adapter"            → HuggingFaceBackend with LoRA adapter (CUDA)
      "hf-endpoint:https://..."    → HFEndpointBackend (managed, no local GPU)
    """
    if spec_str.startswith("claude"):
        return AnthropicBackend(spec_str)
    if spec_str.startswith("hf-endpoint:"):
        return HFEndpointBackend(endpoint_url=spec_str[len("hf-endpoint:"):])
    if spec_str.startswith("hf:"):
        rest = spec_str[3:]
        if "+" in rest:
            base, adapter = rest.split("+", 1)
            return HuggingFaceBackend(base_model=base, adapter=adapter)
        return HuggingFaceBackend(base_model=rest)
    raise ValueError(f"Unknown backend spec: {spec_str}")
