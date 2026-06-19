/* global React, BU_DATA, BU_API, PodcastPlayer */
//
// SCREEN — PODCAST STUDIO
// Browse podcast-able sources (wiki concepts + ingested papers), pick one,
// generate a two-host conversational episode. Pause + ask the hosts.
//
// Two source columns:
//   Concepts  — every node in the knowledge graph (BU_DATA.NODES)
//   Papers    — ingested papers from /papers (defense corpus + paper-drop)
//
// Controls: length (short/medium/long), cloud vs offline engine.

(function () {
  const { useState, useEffect, useMemo } = React;

  function PodcastStudio() {
    const [tab, setTab] = useState("concepts");   // concepts | papers
    const [q, setQ] = useState("");
    const [papers, setPapers] = useState([]);
    const [papersErr, setPapersErr] = useState(null);
    const [length, setLength] = useState("short");
    const [engine, setEngine] = useState("cloud"); // cloud | offline
    const [active, setActive] = useState(null);     // {topic, sourceKind, sourceId}
    const [localState, setLocalState] = useState(null); // {running, mp3, error, source, title}

    useEffect(() => {
      let abort = false;
      (async () => {
        try {
          const r = await BU_API.papers();
          if (!abort) setPapers(r.papers || []);
        } catch (e) {
          if (!abort) setPapersErr(e.message);
        }
      })();
      return () => { abort = true; };
    }, []);

    const concepts = useMemo(() => {
      const all = (BU_DATA?.NODES || []);
      if (!q.trim()) return all.slice(0, 60);
      const ql = q.toLowerCase();
      return all.filter(n =>
        (n.name || n.id || "").toLowerCase().includes(ql)
      ).slice(0, 60);
    }, [q]);

    const filteredPapers = useMemo(() => {
      if (!q.trim()) return papers;
      const ql = q.toLowerCase();
      return papers.filter(p =>
        (p.title + " " + (p.abstract || "") + " " + (p.topics || []).join(" "))
          .toLowerCase().includes(ql)
      );
    }, [papers, q]);

    function launchCloud(topic, sourceKind, sourceId) {
      setActive({ topic, sourceKind, sourceId });
    }

    async function launchOffline(topic, source) {
      setLocalState({ running: true, title: topic, source, phase: "queued" });
      try {
        // Async job: doesn't block the request; poll for status.
        const result = await BU_API.runJob(
          () => BU_API.podcastLocalAsync({ source, mode: "auto", length, tts: "edge" }),
          { interval: 2500, onTick: s =>
              setLocalState(prev => prev && ({ ...prev, phase: s.status })) },
        );
        setLocalState(s => s && ({ ...s, running: false,
                                   mp3: BU_API.mediaUrl(result.mp3) }));
      } catch (e) {
        setLocalState(s => s && ({ ...s, running: false, error: e.message }));
      }
    }

    function onConceptPick(node) {
      const topic = (node.name || node.id).replace(/_/g, " ");
      if (engine === "cloud") {
        launchCloud(topic, "wiki", node.id);
      } else {
        launchOffline(topic, "TITLE: " + topic);
      }
    }

    function onPaperPick(p) {
      if (engine === "cloud") {
        launchCloud(p.title, "paper", p.id);
      } else {
        const src = p.url || [
          "TITLE: " + p.title,
          "ABSTRACT: " + (p.abstract || ""),
          "TOPICS: " + ((p.topics || []).join(", ")),
        ].join("\n\n");
        launchOffline(p.title, src);
      }
    }

    return <div style={{ padding: "24px 32px", minHeight: "calc(100vh - 56px)" }}>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between",
                     alignItems: "flex-start", marginBottom: 18, flexWrap: "wrap", gap: 16 }}>
        <div>
          <div className="t-tag" style={{ color: "var(--c-bridge)" }}>PODCAST STUDIO</div>
          <h2 style={{ margin: "4px 0 0" }}>Turn any concept or paper into a podcast</h2>
          <div className="t-cap" style={{ marginTop: 4, color: "var(--c-ink-muted)" }}>
            Two-host conversational episode. Pause anytime to ask the hosts a question.
          </div>
        </div>
        <div style={{ display: "flex", gap: 16, alignItems: "center" }}>
          <Segmented label="Length" value={length} onChange={setLength}
                     options={[["short","3 min"],["medium","8 min"],["long","15 min"]]} />
          <Segmented label="Engine" value={engine} onChange={setEngine}
                     options={[["cloud","Cloud"],["offline","Offline"]]} />
        </div>
      </div>

      {/* Source tabs + search */}
      <div style={{ display: "flex", gap: 10, alignItems: "center", marginBottom: 14 }}>
        <button className={"btn" + (tab === "concepts" ? " primary" : " ghost")}
                onClick={() => setTab("concepts")}>Concepts</button>
        <button className={"btn" + (tab === "papers" ? " primary" : " ghost")}
                onClick={() => setTab("papers")}>Papers</button>
        <input
          value={q} onChange={e => setQ(e.target.value)}
          placeholder="Search…"
          style={{
            flex: 1, padding: "8px 12px",
            background: "var(--c-bg-elev)", color: "var(--c-ink)",
            border: "1px solid var(--c-line)", borderRadius: "var(--r-md)",
            fontFamily: "var(--f-sans)", fontSize: 13,
          }}
        />
      </div>

      {/* Grid */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))",
        gap: 10,
      }}>
        {tab === "concepts" && concepts.map(n => (
          <SourceCard key={n.id}
            title={(n.name || n.id).replace(/_/g, " ")}
            sub={BU_DATA.CLUSTERS?.[n.cluster]?.name || ""}
            accent={BU_DATA.CLUSTERS?.[n.cluster]?.color}
            onClick={() => onConceptPick(n)} />
        ))}
        {tab === "papers" && papersErr && (
          <div style={{ color: "var(--c-here)", gridColumn: "1/-1" }}>
            Server offline — launch FastAPI to list papers.
          </div>
        )}
        {tab === "papers" && filteredPapers.map(p => (
          <SourceCard key={p.id}
            title={p.title}
            sub={p.cluster_name || (p.topics || []).slice(0,2).join(" · ")}
            accent="var(--c-bridge)"
            onClick={() => onPaperPick(p)} />
        ))}
      </div>

      {/* Cloud player drawer */}
      {active && engine === "cloud" && typeof PodcastPlayer !== "undefined" && (
        <PodcastPlayer
          topic={active.topic}
          sourceKind={active.sourceKind}
          sourceId={active.sourceId}
          length={length}
          onClose={() => setActive(null)}
        />
      )}

      {/* Offline player modal */}
      {localState && (
        <OfflinePlayer state={localState} onClose={() => setLocalState(null)} />
      )}
    </div>;
  }

  function SourceCard({ title, sub, accent, onClick }) {
    const [hover, setHover] = useState(false);
    return <div onClick={onClick}
      onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
      style={{
        padding: 14, cursor: "pointer",
        background: "var(--c-bg-elev)",
        border: `1px solid ${hover ? (accent || "var(--c-bridge)") : "var(--c-line)"}`,
        borderLeft: `3px solid ${accent || "var(--c-bridge)"}`,
        borderRadius: "var(--r-md)",
        transition: "border-color 0.15s, transform 0.15s",
        transform: hover ? "translateY(-2px)" : "none",
      }}>
      <div style={{ fontWeight: 600, fontSize: 14, color: "var(--c-ink)",
                      lineHeight: 1.35, marginBottom: 4 }}>
        {title}
      </div>
      {sub && <div style={{ fontSize: 11.5, color: "var(--c-ink-muted)" }}>{sub}</div>}
      <div style={{ marginTop: 10, fontSize: 12, color: accent || "var(--c-bridge)" }}>
        🎙 Make podcast →
      </div>
    </div>;
  }

  function Segmented({ label, value, onChange, options }) {
    return <div>
      <div className="t-cap" style={{ color: "var(--c-ink-muted)", marginBottom: 4 }}>
        {label}
      </div>
      <div style={{ display: "flex", border: "1px solid var(--c-line)",
                     borderRadius: "var(--r-md)", overflow: "hidden" }}>
        {options.map(([v, lbl]) => (
          <button key={v} onClick={() => onChange(v)} style={{
            padding: "6px 12px", fontSize: 12, border: "none",
            cursor: "pointer",
            background: value === v ? "var(--c-bridge)" : "var(--c-bg-elev)",
            color: value === v ? "var(--c-bg)" : "var(--c-ink-muted)",
            fontFamily: "var(--f-mono)",
          }}>{lbl}</button>
        ))}
      </div>
    </div>;
  }

  // ── Offline player w/ pause-and-ask ──────────────────────────────────────
  function OfflinePlayer({ state, onClose }) {
    const audioRef = React.useRef(null);
    const interjectAudioRef = React.useRef(null);
    const [question, setQuestion] = useState("");
    const [interjecting, setInterjecting] = useState(false);
    const [log, setLog] = useState([]);

    async function handleAsk() {
      if (!question.trim() || !state.mp3) return;
      audioRef.current?.pause();
      setInterjecting(true);
      try {
        const filename = state.mp3.split("/").pop().split("?")[0];
        const r = await BU_API.podcastLocalInterject({
          mp3: filename, question: question.trim(), voice_backend: "kokoro",
        });
        const entry = { turns: r.turns || [], audio: BU_API.mediaUrl(r.audio_path) };
        setLog(prev => [...prev, entry]);
        setQuestion("");
        setTimeout(() => {
          const ia = interjectAudioRef.current;
          if (ia && entry.audio) {
            ia.src = entry.audio;
            ia.onended = () => audioRef.current?.play();
            ia.play();
          } else audioRef.current?.play();
        }, 50);
      } catch (e) {
        alert("Interjection failed: " + e.message);
      } finally { setInterjecting(false); }
    }

    return <div style={{
      position: "fixed", top: 56, right: 0, bottom: 0, width: 480, zIndex: 40,
      background: "var(--c-bg)", borderLeft: "1px solid var(--c-line)",
      boxShadow: "-12px 0 32px -16px rgba(0,0,0,0.5)",
      display: "flex", flexDirection: "column",
    }}>
      <div style={{ padding: "14px 20px", borderBottom: "1px solid var(--c-line)",
                     display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <div className="t-tag" style={{ color: "var(--c-bridge)" }}>OFFLINE PODCAST</div>
          <div className="t-h3" style={{ marginTop: 2 }}>{state.title}</div>
        </div>
        <button className="btn ghost" onClick={onClose}>✕</button>
      </div>
      <div style={{ padding: 20, flex: 1, overflowY: "auto" }}>
        {state.running && <div style={{ color: "var(--c-ink-muted)" }}>
          Generating offline{state.phase ? ` · ${state.phase}` : ""}… runs in the
          background, first run downloads the TTS model.
        </div>}
        {state.error && <div style={{ color: "var(--c-here)",
                                        fontFamily: "var(--f-mono)", fontSize: 12.5 }}>
          {state.error}
        </div>}
        {state.mp3 && <>
          <audio ref={audioRef} src={state.mp3} controls
                  style={{ width: "100%", height: 38 }} />
          <audio ref={interjectAudioRef} style={{ display: "none" }} />
          <div style={{ marginTop: 14, padding: 12,
                          background: "var(--c-bg-elev)",
                          border: "1px dashed var(--c-bridge)",
                          borderRadius: "var(--r-md)" }}>
            <div className="t-tag" style={{ marginBottom: 6, color: "var(--c-bridge)" }}>
              PAUSE + ASK THE HOSTS
            </div>
            <div style={{ display: "flex", gap: 6 }}>
              <input value={question} onChange={e => setQuestion(e.target.value)}
                     onKeyDown={e => { if (e.key === "Enter") handleAsk(); }}
                     placeholder="wait, why does that work?"
                     disabled={interjecting}
                     style={{ flex: 1, padding: "6px 10px",
                               background: "var(--c-bg)", color: "var(--c-ink)",
                               border: "1px solid var(--c-line)", borderRadius: 4,
                               fontFamily: "var(--f-sans)", fontSize: 13 }} />
              <button className="btn" onClick={handleAsk}
                      disabled={interjecting || !question.trim()}>
                {interjecting ? "…" : "Ask →"}
              </button>
            </div>
          </div>
          {log.map((e, i) => (
            <div key={i} style={{ marginTop: 10, fontSize: 12.5, lineHeight: 1.5 }}>
              {e.turns.map((t, j) => (
                <div key={j}>
                  <span style={{ fontFamily: "var(--f-mono)", fontSize: 10.5,
                                  color: t.speaker === "A" ? "var(--c-here)" : "var(--c-bridge)",
                                  marginRight: 6 }}>{t.speaker}</span>
                  {t.text}
                </div>
              ))}
            </div>
          ))}
        </>}
      </div>
    </div>;
  }

  window.PodcastStudio = PodcastStudio;
})();
