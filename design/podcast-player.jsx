/* global React, BU_API */
//
// PodcastPlayer — two-host paper podcast with pause-and-ask interjections.
//
// Props:
//   topic        : str          — episode topic (node name or cluster name)
//   sourceKind   : "wiki" | "paper" | "cluster"
//   sourceId     : str | null   — defaults to topic
//   length       : "short" | "medium" | "long"
//   onClose      : () => void
//
// Behavior:
//   1. On mount: fetch script (BU_API.podcastScript).
//   2. Render turn list. Click "Play episode" → BU_API.podcastRender → <audio>.
//   3. Pause + click "Ask a question" → BU_API.podcastInterject → splice
//      interjection turns + play interjection audio → resume.
//   4. Falls back to script-only mode if render fails (text reader).

(function () {
  const { useState, useEffect, useRef, useMemo } = React;

  function PodcastPlayer({ topic, sourceKind = "wiki", sourceId = null,
                          length = "medium", onClose }) {
    const [script, setScript] = useState(null);
    const [scriptError, setScriptError] = useState(null);
    const [scriptLoading, setScriptLoading] = useState(true);
    const [mediaPaths, setMediaPaths] = useState(null);
    const [rendering, setRendering] = useState(false);
    const [currentTurn, setCurrentTurn] = useState(0);
    const [paused, setPaused] = useState(true);
    const [question, setQuestion] = useState("");
    const [interjecting, setInterjecting] = useState(false);
    const [interjections, setInterjections] = useState([]);  // [{turnIndex, turns, audio}]
    const audioRef = useRef(null);
    const interjectAudioRef = useRef(null);

    // ─── 1. Fetch script ───────────────────────────────────────────
    useEffect(() => {
      let abort = false;
      setScriptLoading(true);
      setScriptError(null);
      BU_API.podcastScript({ topic, length, source_kind: sourceKind,
                              source_id: sourceId })
        .then(s => { if (!abort) setScript(s); })
        .catch(e => { if (!abort) setScriptError(e.message); })
        .finally(() => { if (!abort) setScriptLoading(false); });
      return () => { abort = true; };
    }, [topic, sourceKind, sourceId, length]);

    // ─── 2. Render audio on demand ────────────────────────────────
    async function handlePlay() {
      if (!script) return;
      if (mediaPaths) { audioRef.current?.play(); setPaused(false); return; }
      setRendering(true);
      try {
        const r = await BU_API.podcastRender(script);
        setMediaPaths(r);
        setPaused(false);
        // wait one tick for <audio> to mount
        setTimeout(() => audioRef.current?.play(), 50);
      } catch (e) {
        setScriptError("Render failed: " + e.message);
      } finally {
        setRendering(false);
      }
    }

    // ─── 3. Pause + ask ────────────────────────────────────────────
    async function handleAsk() {
      if (!question.trim() || !script) return;
      audioRef.current?.pause();
      setPaused(true);
      setInterjecting(true);
      try {
        const r = await BU_API.podcastInterject({
          script, turn_index: currentTurn, question: question.trim(),
        });
        const entry = {
          turnIndex: currentTurn,
          turns: r.turns || [],
          audio: BU_API.mediaUrl(r.audio_path),
        };
        setInterjections(prev => [...prev, entry]);
        setQuestion("");
        // play interject audio if present, then resume main on ended
        setTimeout(() => {
          const ia = interjectAudioRef.current;
          if (ia && entry.audio) {
            ia.src = entry.audio;
            ia.onended = () => { audioRef.current?.play(); setPaused(false); };
            ia.play();
          } else {
            audioRef.current?.play();
            setPaused(false);
          }
        }, 50);
      } catch (e) {
        setScriptError("Interjection failed: " + e.message);
      } finally {
        setInterjecting(false);
      }
    }

    // ─── Track currentTurn from audio time using cumulative turn durations ─
    // Without real per-turn time codes, approximate uniformly across duration.
    useEffect(() => {
      const audio = audioRef.current;
      if (!audio || !script) return;
      const onTime = () => {
        const dur = audio.duration || 1;
        const total = (script.turns || []).length;
        const idx = Math.min(total - 1, Math.floor((audio.currentTime / dur) * total));
        setCurrentTurn(idx);
      };
      audio.addEventListener("timeupdate", onTime);
      audio.addEventListener("play",  () => setPaused(false));
      audio.addEventListener("pause", () => setPaused(true));
      return () => audio.removeEventListener("timeupdate", onTime);
    }, [script, mediaPaths]);

    // ─── Render ───────────────────────────────────────────────────
    if (scriptLoading) {
      return <PodcastShell onClose={onClose} title={`Loading podcast: ${topic}…`}>
        <div style={{ padding: 40, textAlign: "center", color: "var(--c-ink-muted)" }}>
          Generating script…
        </div>
      </PodcastShell>;
    }

    if (scriptError && !script) {
      return <PodcastShell onClose={onClose} title="Podcast unavailable">
        <div style={{ padding: 40, color: "var(--c-ink-muted)" }}>
          <div style={{ marginBottom: 12 }}>Could not generate this episode.</div>
          <code style={{ fontSize: 12 }}>{scriptError}</code>
          <div style={{ marginTop: 18, fontSize: 13 }}>
            Make sure the FastAPI server is running:<br/>
            <code>uvicorn api.server:app --reload --port 8080</code>
          </div>
        </div>
      </PodcastShell>;
    }

    const turns = script?.turns || [];
    const activeTurn = turns[currentTurn];
    const turnInterjections = interjections.filter(i => i.turnIndex <= currentTurn);

    return <PodcastShell onClose={onClose} title={script?.title || topic}>
      <div style={{ padding: "16px 24px", display: "flex", flexDirection: "column", gap: 16 }}>
        <p style={{ margin: 0, color: "var(--c-ink-muted)", fontSize: 13.5, lineHeight: 1.5 }}>
          {script?.summary}
        </p>

        {/* Audio player + controls */}
        <div style={{
          display: "flex", gap: 12, alignItems: "center",
          padding: 14, background: "var(--c-bg-elev)",
          border: "1px solid var(--c-line)", borderRadius: "var(--r-md)",
        }}>
          {mediaPaths ? (
            <audio ref={audioRef} controls
                   src={BU_API.mediaUrl(mediaPaths.mp3)}
                   style={{ flex: 1, height: 36 }} />
          ) : (
            <button className="btn primary" onClick={handlePlay}
                    disabled={rendering}>
              {rendering ? "Rendering audio…" : "▶ Generate & play episode"}
            </button>
          )}
        </div>
        <audio ref={interjectAudioRef} style={{ display: "none" }} />

        {/* Pause + ask */}
        {mediaPaths && (
          <div style={{
            padding: 14, background: "color-mix(in oklch, var(--c-bridge) 8%, transparent)",
            border: "1px solid var(--c-bridge)", borderRadius: "var(--r-md)",
          }}>
            <div className="t-tag" style={{ marginBottom: 8, color: "var(--c-bridge)" }}>
              ASK THE HOSTS (TURN {currentTurn + 1} / {turns.length})
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              <input
                value={question}
                onChange={e => setQuestion(e.target.value)}
                onKeyDown={e => { if (e.key === "Enter") handleAsk(); }}
                placeholder="wait, why does that work?"
                disabled={interjecting}
                style={{
                  flex: 1, padding: "8px 12px",
                  background: "var(--c-bg)", color: "var(--c-ink)",
                  border: "1px solid var(--c-line)", borderRadius: 6,
                  fontFamily: "var(--f-sans)", fontSize: 14,
                }}
              />
              <button className="btn" onClick={handleAsk}
                      disabled={interjecting || !question.trim()}>
                {interjecting ? "Asking…" : "Ask →"}
              </button>
            </div>
            <div className="t-cap" style={{ marginTop: 6, color: "var(--c-ink-muted)" }}>
              Pauses the episode, hosts answer in 1-3 turns, then resumes.
            </div>
          </div>
        )}

        {/* Turn list — highlights currentTurn + interjections */}
        <div style={{ maxHeight: 360, overflowY: "auto",
                       border: "1px solid var(--c-line)",
                       borderRadius: "var(--r-md)" }}>
          {turns.map((t, i) => {
            const inj = interjections.filter(x => x.turnIndex === i);
            const active = i === currentTurn;
            const speakerColor = t.speaker === "A" ? "var(--c-here)" : "var(--c-bridge)";
            return <React.Fragment key={i}>
              <div style={{
                padding: "10px 14px",
                background: active ? "color-mix(in oklch, " + speakerColor + " 10%, transparent)" : "transparent",
                borderLeft: `3px solid ${active ? speakerColor : "transparent"}`,
                display: "grid", gridTemplateColumns: "48px 1fr",
                gap: 12, fontSize: 13.5, lineHeight: 1.5,
              }}>
                <div style={{
                  fontFamily: "var(--f-mono)", fontSize: 11,
                  color: speakerColor, paddingTop: 2,
                }}>HOST {t.speaker}</div>
                <div>
                  <div style={{ color: "var(--c-ink)" }}>{t.text}</div>
                  {t.visual && (
                    <div className="t-cap" style={{ marginTop: 4, color: "var(--c-ink-muted)" }}>
                      🎬 {t.visual}
                    </div>
                  )}
                </div>
              </div>
              {inj.map((entry, j) => (
                <div key={`inj-${i}-${j}`} style={{
                  padding: "8px 14px 8px 50px",
                  background: "color-mix(in oklch, var(--c-bridge) 6%, transparent)",
                  borderLeft: `3px dashed var(--c-bridge)`,
                  fontSize: 13, lineHeight: 1.5,
                }}>
                  <div className="t-tag" style={{ color: "var(--c-bridge)", marginBottom: 4 }}>
                    INTERJECTION ({entry.turns.length} turns)
                  </div>
                  {entry.turns.map((it, k) => (
                    <div key={k} style={{ marginBottom: 4 }}>
                      <span style={{
                        fontFamily: "var(--f-mono)", fontSize: 10.5,
                        color: it.speaker === "A" ? "var(--c-here)" : "var(--c-bridge)",
                        marginRight: 8,
                      }}>HOST {it.speaker}</span>
                      <span style={{ color: "var(--c-ink)" }}>{it.text}</span>
                    </div>
                  ))}
                </div>
              ))}
            </React.Fragment>;
          })}
        </div>
      </div>
    </PodcastShell>;
  }

  function PodcastShell({ title, children, onClose }) {
    return <div style={{
      position: "fixed", top: 56, right: 0, bottom: 0, width: 540,
      zIndex: 20, background: "var(--c-bg)",
      borderLeft: "1px solid var(--c-line)",
      boxShadow: "-12px 0 32px -16px rgba(0,0,0,0.5)",
      display: "flex", flexDirection: "column",
    }}>
      <div style={{
        padding: "14px 22px", borderBottom: "1px solid var(--c-line)",
        display: "flex", alignItems: "center", justifyContent: "space-between",
      }}>
        <div>
          <div className="t-tag" style={{ color: "var(--c-ink-muted)" }}>PODCAST</div>
          <div className="t-h3" style={{ marginTop: 2 }}>{title}</div>
        </div>
        <button className="btn ghost" onClick={onClose}>✕</button>
      </div>
      <div style={{ flex: 1, overflowY: "auto" }}>{children}</div>
    </div>;
  }

  window.PodcastPlayer = PodcastPlayer;
})();
