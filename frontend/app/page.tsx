// @ts-nocheck
"use client";
import { useState, useEffect, useRef, useCallback } from "react";

/* ─────────────────────────────────────────────
   DESIGN SYSTEM
───────────────────────────────────────────── */
const C = {
  bg: "#09090b",
  surface: "#111113",
  surfaceHover: "#18181b",
  border: "#27272a",
  borderLight: "#3f3f46",
  text: "#fafafa",
  textMuted: "#a1a1aa",
  textDim: "#52525b",
  accent: "#0ea5e9",       // IBM blue
  accentGlow: "rgba(14,165,233,0.25)",
  accentSoft: "rgba(14,165,233,0.08)",
  green: "#22c55e",
  greenGlow: "rgba(34,197,94,0.2)",
  amber: "#f59e0b",
  purple: "#a78bfa",
  purpleGlow: "rgba(167,139,250,0.2)",
  red: "#f87171",
};

const FONT_DISPLAY = "'Instrument Serif', 'Georgia', serif";
const FONT_BODY = "'Geist', 'DM Mono', monospace";
const FONT_MONO = "'Geist Mono', 'JetBrains Mono', 'Fira Code', monospace";

/* ─────────────────────────────────────────────
   DATA
───────────────────────────────────────────── */
const PIPELINE_STAGES = [
  { id: "validation",   label: "Validation",    icon: "◈", color: C.green,  glow: C.greenGlow,  desc: "Market fit & PMF analysis" },
  { id: "architecture", label: "Architecture",  icon: "⬡", color: C.accent, glow: C.accentGlow, desc: "System design & stack selection" },
  { id: "codegen",      label: "Code Gen",      icon: "⌬", color: C.purple, glow: C.purpleGlow, desc: "Scaffold & implementation" },
  { id: "security",     label: "Security",      icon: "⬟", color: C.amber,  glow: "rgba(245,158,11,0.2)", desc: "OWASP audit & hardening" },
  { id: "github",       label: "GitHub PR",     icon: "⤴", color: C.red,    glow: "rgba(248,113,113,0.2)", desc: "Commit, branch & open PR" },
];

const IBM_STACK = [
  { name: "IBM Bob", tag: "Orchestrator", desc: "Multi-agent workflow coordinator that sequences AI tasks, manages state, and routes outputs between agents.", color: C.accent },
  { name: "Granite AI", tag: "Foundation Model", desc: "IBM's enterprise-grade LLM powering code generation, documentation, and structured data synthesis.", color: C.purple },
  { name: "watsonx.ai", tag: "AI Platform", desc: "Model lifecycle management, fine-tuning pipeline, and observability dashboard for all inference calls.", color: C.green },
  { name: "Orchestration", tag: "Workflow Engine", desc: "Directed acyclic graph execution engine that parallelizes independent agents and resolves dependencies.", color: C.amber },
];

const TERMINAL_SEQUENCE = [
  { t: 0,    kind: "sys",     text: "IBM Bob Orchestrator v2.4.1 initialized" },
  { t: 400,  kind: "info",    text: "Loading AI agent registry..." },
  { t: 900,  kind: "success", text: "Agents loaded: validation, architect, codegen, security, shipper" },
  { t: 1400, kind: "info",    text: "Connecting watsonx.ai inference endpoints..." },
  { t: 1900, kind: "success", text: "Granite-34B-Code model endpoint READY" },
  { t: 2400, kind: "divider", text: "" },
  { t: 2600, kind: "info",    text: "[STAGE 1] Dispatching validation agent..." },
  { t: 3100, kind: "log",     text: "  → Scanning market signals & competitor landscape" },
  { t: 3600, kind: "log",     text: "  → Running PMF scoring model (87 indicators)" },
  { t: 4100, kind: "log",     text: "  → Analyzing TAM/SAM/SOM segmentation" },
  { t: 4600, kind: "success", text: "  ✓ PMF Score: 87/100 | TAM: $4.2B | Verdict: GO" },
  { t: 5100, kind: "divider", text: "" },
  { t: 5300, kind: "info",    text: "[STAGE 2] Dispatching architecture agent..." },
  { t: 5800, kind: "log",     text: "  → Evaluating stack constraints & scale requirements" },
  { t: 6300, kind: "log",     text: "  → Generating system topology graph" },
  { t: 6800, kind: "log",     text: "  → Selecting: Next.js · PostgreSQL · Redis · S3" },
  { t: 7300, kind: "success", text: "  ✓ Architecture blueprint finalized (12 services)" },
  { t: 7800, kind: "divider", text: "" },
  { t: 8000, kind: "info",    text: "[STAGE 3] Dispatching codegen agent (Granite-34B)..." },
  { t: 8500, kind: "log",     text: "  → Scaffolding project structure (47 files)" },
  { t: 9000, kind: "log",     text: "  → Generating API routes, DB schema, UI components" },
  { t: 9500, kind: "log",     text: "  → Writing tests & documentation" },
  { t:10000, kind: "success", text: "  ✓ 4,821 lines generated | 94% test coverage" },
  { t:10500, kind: "divider", text: "" },
  { t:10700, kind: "info",    text: "[STAGE 4] Dispatching security agent..." },
  { t:11200, kind: "log",     text: "  → Running OWASP Top-10 audit" },
  { t:11700, kind: "log",     text: "  → Static analysis: SQL injection, XSS, CSRF" },
  { t:12200, kind: "warn",    text: "  ⚠ 2 medium issues detected → auto-patching" },
  { t:12700, kind: "success", text: "  ✓ Security audit passed | 0 critical | 0 high" },
  { t:13200, kind: "divider", text: "" },
  { t:13400, kind: "info",    text: "[STAGE 5] Dispatching GitHub shipper agent..." },
  { t:13900, kind: "log",     text: "  → Initializing git repo & committing scaffold" },
  { t:14400, kind: "log",     text: "  → Running CI/CD preflight checks" },
  { t:14900, kind: "success", text: "  ✓ PR #1 opened — 'feat: initial scaffold'" },
  { t:15400, kind: "divider", text: "" },
  { t:15600, kind: "sys",     text: "◈ All stages complete. Startup foundation ready." },
  { t:16000, kind: "cursor",  text: "$ _" },
];

const STAGE_UNLOCK_AT_LINE = { validation: 6, architecture: 12, codegen: 18, security: 23, github: 29 };
const STAGE_DONE_AT_LINE = { validation: 11, architecture: 17, codegen: 22, security: 27, github: 32 };
const GITHUB_PULLS_URL = "https://github.com/Anan28eng/ibm-proj/pulls";

/* ─────────────────────────────────────────────
   HOOKS
───────────────────────────────────────────── */
function useInView(ref, threshold = 0.15) {
  const [visible, setVisible] = useState(false);
  useEffect(() => {
    const obs = new IntersectionObserver(([e]) => { if (e.isIntersecting) setVisible(true); }, { threshold });
    if (ref.current) obs.observe(ref.current);
    return () => obs.disconnect();
  }, []);
  return visible;
}

function useTypewriter(text, speed = 35, started = true) {
  const [out, setOut] = useState("");
  useEffect(() => {
    if (!started) { setOut(""); return; }
    setOut(""); let i = 0;
    const id = setInterval(() => { i++; setOut(text.slice(0, i)); if (i >= text.length) clearInterval(id); }, speed);
    return () => clearInterval(id);
  }, [text, started]);
  return out;
}

/* ─────────────────────────────────────────────
   GLOBAL STYLES
───────────────────────────────────────────── */
const GlobalStyle = () => (
  <style>{`
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap');
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body { background: ${C.bg}; color: ${C.text}; font-family: ${FONT_BODY}; -webkit-font-smoothing: antialiased; }
    ::selection { background: ${C.accentGlow}; color: ${C.text}; }
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: ${C.border}; border-radius: 2px; }
    input, textarea, button { font-family: inherit; }

    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
    @keyframes spin { to { transform: rotate(360deg); } }
    @keyframes pulse-glow { 0%,100%{box-shadow:0 0 12px ${C.accentGlow}} 50%{box-shadow:0 0 28px ${C.accentGlow}, 0 0 60px ${C.accentGlow}} }
    @keyframes ping { 0%{transform:scale(1);opacity:.8} 100%{transform:scale(2.4);opacity:0} }
    @keyframes fadeUp { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
    @keyframes fadeIn { from{opacity:0} to{opacity:1} }
    @keyframes slideRight { from{width:0} to{width:100%} }
    @keyframes scanline { 0%{top:-100%} 100%{top:200%} }
    @keyframes flicker { 0%,100%{opacity:1} 92%{opacity:1} 93%{opacity:0.7} 94%{opacity:1} }
    @keyframes nodeAppear { from{transform:scale(0.6);opacity:0} to{transform:scale(1);opacity:1} }
    @keyframes connectorFill { from{stroke-dashoffset:100} to{stroke-dashoffset:0} }
    @keyframes gradientShift { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
    @keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
  `}</style>
);

/* ─────────────────────────────────────────────
   ATOMS
───────────────────────────────────────────── */
const Tag = ({ children, color = C.accent }) => (
  <span style={{
    display: "inline-flex", alignItems: "center", gap: 5,
    padding: "3px 10px", borderRadius: 100,
    border: `1px solid ${color}44`,
    background: `${color}10`,
    color: color, fontSize: 10, fontWeight: 600, letterSpacing: "0.1em",
    textTransform: "uppercase", fontFamily: FONT_MONO,
  }}>{children}</span>
);

const Dot = ({ color = C.green, animate = false }) => (
  <span style={{ position: "relative", display: "inline-block", width: 7, height: 7 }}>
    {animate && <span style={{ position: "absolute", inset: 0, borderRadius: "50%", background: color, animation: "ping 1.5s ease-out infinite" }} />}
    <span style={{ position: "absolute", inset: 0, borderRadius: "50%", background: color }} />
  </span>
);

const Divider = ({ style = {} }) => (
  <div style={{ height: 1, background: `linear-gradient(90deg, transparent, ${C.border}, transparent)`, ...style }} />
);

/* ─────────────────────────────────────────────
   NOISE OVERLAY (atmospheric texture)
───────────────────────────────────────────── */
const Noise = () => (
  <div style={{
    position: "fixed", inset: 0, pointerEvents: "none", zIndex: 9999,
    opacity: 0.025,
    backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
  }} />
);

/* ─────────────────────────────────────────────
   LANDING → HERO
───────────────────────────────────────────── */
function Hero({ onStart }) {
  const headline = "Your AI Co-founder\nfor Startup Execution.";
  const typed = useTypewriter(headline, 32);
  const lines = typed.split("\n");
  const [hovered, setHovered] = useState(false);

  return (
    <section style={{ minHeight: "100vh", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: "100px 24px", position: "relative", overflow: "hidden" }}>

      {/* Grid bg */}
      <div style={{ position: "absolute", inset: 0, backgroundImage: `linear-gradient(${C.border}44 1px, transparent 1px), linear-gradient(90deg, ${C.border}44 1px, transparent 1px)`, backgroundSize: "64px 64px", opacity: 0.4 }} />

      {/* Radial glow */}
      <div style={{ position: "absolute", width: 800, height: 500, background: `radial-gradient(ellipse, ${C.accentGlow} 0%, transparent 65%)`, top: "20%", left: "50%", transform: "translateX(-50%)", pointerEvents: "none" }} />
      <div style={{ position: "absolute", width: 400, height: 300, background: `radial-gradient(ellipse, ${C.purpleGlow} 0%, transparent 65%)`, bottom: "15%", right: "20%", pointerEvents: "none" }} />

      {/* Floating terminal snippets */}
      <FloatingCards />

      <div style={{ position: "relative", textAlign: "center", maxWidth: 820, animation: "fadeUp 0.8s ease" }}>

        {/* IBM badge */}
        <div style={{ display: "inline-flex", alignItems: "center", gap: 8, padding: "6px 14px", border: `1px solid ${C.border}`, borderRadius: 100, background: C.surface, marginBottom: 44 }}>
          <Dot color={C.accent} animate />
          <span style={{ fontSize: 11, fontWeight: 600, letterSpacing: "0.1em", color: C.textMuted, textTransform: "uppercase", fontFamily: FONT_MONO }}>Powered by IBM Bob Orchestrator</span>
        </div>

        <h1 style={{
          fontFamily: FONT_DISPLAY, fontWeight: 400, lineHeight: 1.05,
          fontSize: "clamp(52px, 8vw, 96px)",
          letterSpacing: "-0.03em", color: C.text,
          margin: "0 0 32px", minHeight: "2.2em",
        }}>
          {lines[0]}<br />
          <span style={{ fontStyle: "italic", background: `linear-gradient(135deg, ${C.accent}, ${C.purple})`, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", backgroundClip: "text" }}>
            {lines[1]}
          </span>
        </h1>

        <p style={{ fontSize: "clamp(15px, 2vw, 18px)", color: C.textMuted, lineHeight: 1.75, maxWidth: 600, margin: "0 auto 56px", fontFamily: FONT_BODY }}>
          Validate, architect, generate, secure, and ship startup-ready software using IBM Bob-powered orchestration.
        </p>

        {/* CTA cluster */}
        <div style={{ display: "flex", gap: 12, justifyContent: "center", flexWrap: "wrap" }}>
          <button
            onClick={onStart}
            onMouseEnter={() => setHovered(true)}
            onMouseLeave={() => setHovered(false)}
            style={{
              padding: "14px 32px", borderRadius: 10,
              background: hovered ? `linear-gradient(135deg, ${C.accent}, ${C.purple})` : C.accent,
              border: "none", color: "#000", fontWeight: 700, fontSize: 14,
              cursor: "pointer", letterSpacing: "0.02em",
              boxShadow: hovered ? `0 0 40px ${C.accentGlow}, 0 0 80px ${C.accentGlow}` : `0 0 20px ${C.accentGlow}`,
              transition: "all 0.3s cubic-bezier(.4,0,.2,1)",
              transform: hovered ? "translateY(-2px)" : "none",
            }}>
            Start Building →
          </button>
          <button style={{
            padding: "14px 32px", borderRadius: 10,
            background: "transparent", border: `1px solid ${C.border}`,
            color: C.textMuted, fontWeight: 500, fontSize: 14, cursor: "pointer",
            transition: "all 0.2s",
          }}
            onMouseEnter={e => { e.target.style.borderColor = C.borderLight; e.target.style.color = C.text; }}
            onMouseLeave={e => { e.target.style.borderColor = C.border; e.target.style.color = C.textMuted; }}
          >
            Watch Demo
          </button>
        </div>

        {/* Metrics strip */}
        <div style={{ display: "flex", gap: 40, justifyContent: "center", marginTop: 72, flexWrap: "wrap" }}>
          {[["47", "Files generated"], ["4.8K", "Lines of code"], ["< 3min", "Full scaffold"], ["94%", "Test coverage"]].map(([num, lab]) => (
            <div key={lab} style={{ textAlign: "center" }}>
              <div style={{ fontFamily: FONT_MONO, fontSize: 24, fontWeight: 700, color: C.text, letterSpacing: "-0.02em" }}>{num}</div>
              <div style={{ fontSize: 11, color: C.textDim, letterSpacing: "0.06em", textTransform: "uppercase", marginTop: 4 }}>{lab}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Scroll indicator */}
      <div style={{ position: "absolute", bottom: 40, left: "50%", transform: "translateX(-50%)", display: "flex", flexDirection: "column", alignItems: "center", gap: 8, opacity: 0.4 }}>
        <span style={{ fontSize: 10, letterSpacing: "0.12em", textTransform: "uppercase", color: C.textDim }}>Scroll</span>
        <div style={{ width: 1, height: 32, background: `linear-gradient(${C.borderLight}, transparent)` }} />
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────
   FLOATING TERMINAL CARDS
───────────────────────────────────────────── */
function FloatingCards() {
  const cards = [
    { x: "5%", y: "18%", delay: "0s", lines: ["[IBM Bob] Orchestrator ready", "[INFO] 5 agents loaded", "[SUCCESS] watsonx.ai connected"] },
    { x: "78%", y: "22%", delay: "0.6s", lines: ["[GRANITE] Model: 34B-Code", "[INFO] Inference endpoint OK", "[LOG] Context window: 128K"] },
    { x: "82%", y: "64%", delay: "1.2s", lines: ["[PR] #1 feat: initial scaffold", "[CI] All checks passing ✓", "[MERGE] Ready for review"] },
  ];
  return (
    <>
      {cards.map((c, i) => (
        <div key={i} style={{
          position: "absolute", left: c.x, top: c.y,
          background: C.surface, border: `1px solid ${C.border}`,
          borderRadius: 10, padding: "12px 16px",
          fontFamily: FONT_MONO, fontSize: 11, lineHeight: 1.8,
          color: C.textMuted, minWidth: 240,
          boxShadow: `0 8px 32px rgba(0,0,0,0.4)`,
          animation: `float 4s ease-in-out ${c.delay} infinite`,
          backdropFilter: "blur(12px)",
          opacity: 0.85,
          display: "none",
        }}
          className={`floating-card-${i}`}
        >
          {c.lines.map((l, j) => (
            <div key={j} style={{ color: l.startsWith("[SUCCESS]") || l.includes("✓") ? C.green : l.startsWith("[PR]") || l.startsWith("[MERGE]") ? C.accent : C.textMuted }}>{l}</div>
          ))}
        </div>
      ))}
      <style>{`
        @media (min-width: 1100px) { .floating-card-0, .floating-card-1, .floating-card-2 { display: block; } }
      `}</style>
    </>
  );
}

/* ─────────────────────────────────────────────
   PIPELINE VISUALIZATION (landing)
───────────────────────────────────────────── */
function PipelineViz() {
  const ref = useRef();
  const visible = useInView(ref, 0.2);
  const [step, setStep] = useState(-1);

  useEffect(() => {
    if (!visible) return;
    let i = 0;
    const tick = () => { setStep(i); i++; if (i < PIPELINE_STAGES.length) setTimeout(tick, 500); };
    setTimeout(tick, 200);
  }, [visible]);

  return (
    <section ref={ref} style={{ padding: "160px 24px", position: "relative" }}>
      <Divider />
      <div style={{ maxWidth: 960, margin: "0 auto", paddingTop: 80 }}>

        <SectionLabel label="Orchestration Pipeline" />
        <h2 style={{ fontFamily: FONT_DISPLAY, fontWeight: 400, fontSize: "clamp(36px, 5vw, 60px)", lineHeight: 1.08, letterSpacing: "-0.03em", color: C.text, margin: "16px 0 80px" }}>
          Six stages.<br /><em style={{ fontStyle: "italic", color: C.accent }}>One command.</em>
        </h2>

        {/* Horizontal pipeline */}
        <div style={{ display: "flex", alignItems: "center", gap: 0, overflowX: "auto", paddingBottom: 24 }}>
          {/* Idea node */}
          <PipeNode
            label="Idea"
            icon="◇"
            color={C.textMuted}
            glow="rgba(161,161,170,0.15)"
            active={step >= 0}
            done={step > 0}
            isIdea
          />

          {PIPELINE_STAGES.map((s, i) => (
            <div key={s.id} style={{ display: "flex", alignItems: "center", flex: 1, minWidth: 0 }}>
              {/* Connector */}
              <div style={{ flex: 1, height: 1, background: C.border, position: "relative", minWidth: 20 }}>
                <div style={{
                  position: "absolute", inset: 0,
                  background: `linear-gradient(90deg, ${i === 0 ? C.textMuted : PIPELINE_STAGES[i-1].color}, ${s.color})`,
                  transformOrigin: "left",
                  transition: "transform 0.6s cubic-bezier(.4,0,.2,1)",
                  transform: `scaleX(${step >= i ? 1 : 0})`,
                }} />
              </div>
              <PipeNode
                label={s.label}
                icon={s.icon}
                color={s.color}
                glow={s.glow}
                active={step === i}
                done={step > i}
              />
            </div>
          ))}
        </div>

        {/* Stage descriptions */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: 20, marginTop: 48 }}>
          {PIPELINE_STAGES.map((s, i) => (
            <div key={s.id} style={{
              padding: "20px", border: `1px solid ${step >= i ? s.color + "44" : C.border}`,
              borderRadius: 10, background: step >= i ? `${s.color}06` : "transparent",
              transition: "all 0.5s ease",
              opacity: step >= i ? 1 : 0.35,
            }}>
              <div style={{ fontSize: 18, color: step >= i ? s.color : C.textDim, marginBottom: 8 }}>{s.icon}</div>
              <div style={{ fontSize: 13, fontWeight: 600, color: C.text, marginBottom: 4 }}>{s.label}</div>
              <div style={{ fontSize: 12, color: C.textMuted, lineHeight: 1.6 }}>{s.desc}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function PipeNode({ label, icon, color, glow, active, done, isIdea }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10, flexShrink: 0 }}>
      <div style={{ position: "relative" }}>
        {active && <div style={{ position: "absolute", inset: -10, borderRadius: "50%", background: glow, animation: "ping 1.5s ease-out infinite" }} />}
        <div style={{
          width: isIdea ? 48 : 56, height: isIdea ? 48 : 56,
          borderRadius: "50%",
          border: `1.5px solid ${done || active ? color : C.border}`,
          background: done ? `${color}18` : active ? `${color}0d` : C.surface,
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: isIdea ? 16 : 20, color: done || active ? color : C.textDim,
          boxShadow: active ? `0 0 24px ${color}66` : done ? `0 0 12px ${color}33` : "none",
          transition: "all 0.4s cubic-bezier(.4,0,.2,1)",
          animation: done || active ? "nodeAppear 0.4s ease" : "none",
        }}>
          {done ? "✓" : icon}
        </div>
      </div>
      <span style={{ fontSize: 11, color: done || active ? C.text : C.textDim, fontWeight: 500, letterSpacing: "0.05em", whiteSpace: "nowrap", transition: "color 0.4s" }}>{label}</span>
    </div>
  );
}

/* ─────────────────────────────────────────────
   FEATURE SECTIONS
───────────────────────────────────────────── */
function FeatureSections() {
  const sections = [
    {
      num: "01", tag: "Startup Intelligence", color: C.green,
      title: "Market validation\nbefore a line of code.",
      body: "IBM Bob dispatches the validation agent to scan thousands of market signals — competitor activity, search trends, VC deal flow — and returns a structured PMF score with actionable go/no-go verdict.",
      items: ["TAM/SAM/SOM analysis", "Competitor landscape mapping", "PMF scoring (87 indicators)", "Go-to-market recommendation"],
    },
    {
      num: "02", tag: "Architecture Planning", color: C.accent,
      title: "Opinionated stacks\nfor your exact problem.",
      body: "The architecture agent generates a complete system topology — services, databases, message queues, CDN, auth — with trade-off rationale and estimated infrastructure cost.",
      items: ["Technology stack selection", "System topology diagram", "API contract generation", "Infrastructure cost estimate"],
    },
    {
      num: "03", tag: "Code Generation", color: C.purple,
      title: "Production code,\nnot prototypes.",
      body: "Granite-34B-Code generates 47+ files of production-grade code: typed API routes, database schemas, UI components, authentication flows, and comprehensive test suites.",
      items: ["Full-stack scaffold (47 files)", "Database schema & migrations", "Auth system with RBAC", "94% test coverage target"],
    },
    {
      num: "04", tag: "Automated Shipping", color: C.amber,
      title: "Commit, branch, PR.\nFully automated.",
      body: "The shipper agent initializes a git repository, creates a feature branch, runs lint & CI preflight checks, and opens a GitHub pull request with a structured description ready for human review.",
      items: ["Git init & first commit", "Automated branch strategy", "CI/CD preflight checks", "PR with full description"],
    },
  ];

  return (
    <section style={{ padding: "0 24px 160px" }}>
      <div style={{ maxWidth: 960, margin: "0 auto" }}>
        {sections.map((s, i) => {
          const ref = useRef();
          const vis = useInView(ref, 0.2);
          return (
            <div key={s.num} ref={ref} style={{
              display: "grid", gridTemplateColumns: "1fr 1fr", gap: 80,
              alignItems: "center", padding: "80px 0",
              borderBottom: i < sections.length - 1 ? `1px solid ${C.border}` : "none",
              opacity: vis ? 1 : 0, transform: vis ? "translateY(0)" : "translateY(32px)",
              transition: "all 0.7s cubic-bezier(.4,0,.2,1)",
            }}>
              <div style={{ order: i % 2 === 0 ? 0 : 1 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 24 }}>
                  <span style={{ fontFamily: FONT_MONO, fontSize: 11, color: C.textDim }}>{s.num}</span>
                  <Tag color={s.color}>{s.tag}</Tag>
                </div>
                <h3 style={{ fontFamily: FONT_DISPLAY, fontSize: "clamp(28px, 3.5vw, 40px)", fontWeight: 400, lineHeight: 1.12, letterSpacing: "-0.025em", color: C.text, marginBottom: 20, whiteSpace: "pre-line" }}>{s.title}</h3>
                <p style={{ fontSize: 15, color: C.textMuted, lineHeight: 1.8, marginBottom: 28 }}>{s.body}</p>
                <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                  {s.items.map(it => (
                    <div key={it} style={{ display: "flex", alignItems: "center", gap: 10, fontSize: 13, color: C.textMuted }}>
                      <span style={{ color: s.color, fontSize: 10 }}>◈</span> {it}
                    </div>
                  ))}
                </div>
              </div>
              <FeatureCard section={s} />
            </div>
          );
        })}
      </div>
    </section>
  );
}

function FeatureCard({ section: s }) {
  const cards = {
    "01": <ValidationCard color={s.color} />,
    "02": <ArchCard color={s.color} />,
    "03": <CodeCard color={s.color} />,
    "04": <PRCard color={s.color} />,
  };
  return (
    <div style={{ border: `1px solid ${C.border}`, borderRadius: 14, overflow: "hidden", background: C.surface, boxShadow: "0 16px 48px rgba(0,0,0,0.3)" }}>
      {cards[s.num]}
    </div>
  );
}

function ValidationCard({ color }) {
  return (
    <div style={{ padding: 24, fontFamily: FONT_MONO }}>
      <div style={{ fontSize: 11, color: C.textDim, marginBottom: 16 }}>// validation_report.json</div>
      {[{ k: "pmf_score", v: "87 / 100", bar: 87, c: C.green }, { k: "tam", v: "$4.2B", bar: 70, c: C.accent }, { k: "competition", v: "moderate", bar: 50, c: C.amber }, { k: "verdict", v: "GO →", bar: 100, c: color }].map(r => (
        <div key={r.k} style={{ marginBottom: 14 }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 5 }}>
            <span style={{ fontSize: 11, color: C.textDim }}>{r.k}</span>
            <span style={{ fontSize: 11, color: r.c, fontWeight: 600 }}>{r.v}</span>
          </div>
          <div style={{ height: 3, background: C.border, borderRadius: 2 }}>
            <div style={{ height: "100%", width: `${r.bar}%`, background: r.c, borderRadius: 2 }} />
          </div>
        </div>
      ))}
    </div>
  );
}

function ArchCard({ color }) {
  return (
    <div style={{ padding: 24, fontFamily: FONT_MONO, fontSize: 12 }}>
      <div style={{ fontSize: 11, color: C.textDim, marginBottom: 16 }}>// architecture.yaml</div>
      {[["frontend", "Next.js 14 + Tailwind"], ["api", "tRPC + REST gateway"], ["database", "PostgreSQL + Redis"], ["auth", "NextAuth + RBAC"], ["infra", "Vercel + AWS S3"], ["payments", "Stripe metered"]].map(([k, v]) => (
        <div key={k} style={{ display: "flex", gap: 16, marginBottom: 10 }}>
          <span style={{ color: color, minWidth: 80 }}>{k}:</span>
          <span style={{ color: C.textMuted }}>{v}</span>
        </div>
      ))}
    </div>
  );
}

function CodeCard({ color }) {
  return (
    <div style={{ padding: 24, fontFamily: FONT_MONO, fontSize: 11, lineHeight: 1.9 }}>
      <div style={{ color: C.textDim, marginBottom: 12 }}>// app/api/metrics/route.ts</div>
      <div style={{ color: "#94a3b8" }}><span style={{ color: "#7dd3fc" }}>import</span> {"{"} db {"}"} <span style={{ color: "#7dd3fc" }}>from</span> <span style={{ color: "#86efac" }}>"@/lib/db"</span></div>
      <div style={{ color: "#94a3b8" }}><span style={{ color: "#7dd3fc" }}>import</span> {"{"} auth {"}"} <span style={{ color: "#7dd3fc" }}>from</span> <span style={{ color: "#86efac" }}>"@/lib/auth"</span></div>
      <div style={{ height: 8 }} />
      <div style={{ color: "#94a3b8" }}><span style={{ color: "#7dd3fc" }}>export async function</span> <span style={{ color: color }}>GET</span>(req) {"{"}</div>
      <div style={{ color: "#94a3b8", paddingLeft: 16 }}><span style={{ color: "#7dd3fc" }}>const</span> session = <span style={{ color: "#7dd3fc" }}>await</span> <span style={{ color: "#fbbf24" }}>auth</span>()</div>
      <div style={{ color: "#94a3b8", paddingLeft: 16 }}><span style={{ color: "#7dd3fc" }}>if</span> (!session) <span style={{ color: "#7dd3fc" }}>return</span> <span style={{ color: "#f87171" }}>Response</span>.<span style={{ color: "#fbbf24" }}>json</span>({"{"}<span style={{ color: "#86efac" }}>"error"</span>: <span style={{ color: "#86efac" }}>"401"</span>{"}"})</div>
      <div style={{ color: "#94a3b8", paddingLeft: 16 }}><span style={{ color: "#7dd3fc" }}>const</span> data = <span style={{ color: "#7dd3fc" }}>await</span> db.metric.<span style={{ color: "#fbbf24" }}>findMany</span>({"{"}...{"}"})</div>
      <div style={{ color: "#94a3b8", paddingLeft: 16 }}><span style={{ color: "#7dd3fc" }}>return</span> <span style={{ color: "#f87171" }}>Response</span>.<span style={{ color: "#fbbf24" }}>json</span>({"{"} data {"}"})</div>
      <div style={{ color: "#94a3b8" }}>{"}"}</div>
    </div>
  );
}

function PRCard({ color }) {
  return (
    <div style={{ fontFamily: FONT_MONO }}>
      <div style={{ padding: "14px 20px", borderBottom: `1px solid ${C.border}`, display: "flex", gap: 10, alignItems: "center" }}>
        <span style={{ fontSize: 12, color: C.text, fontWeight: 600 }}>PR #1</span>
        <Tag color={C.green}>Open</Tag>
        <span style={{ fontSize: 11, color: C.textMuted }}>feat: initial scaffold</span>
      </div>
      <div style={{ padding: "16px 20px" }}>
        <div style={{ fontSize: 11, color: C.textDim, marginBottom: 12 }}>Opened by <span style={{ color: color }}>ai-cofounder[bot]</span> · main ← feat/scaffold</div>
        <div style={{ background: "#0d1117", border: `1px solid ${C.border}`, borderRadius: 6, padding: 12, fontSize: 11, lineHeight: 1.8 }}>
          <div style={{ color: C.green }}>+ 47 files changed</div>
          <div style={{ color: C.green }}>+ 4,821 insertions</div>
          <div style={{ color: C.textMuted }}>✓ CI passing · lint clean · tests: 94%</div>
        </div>
      </div>
    </div>
  );
}

/* ─────────────────────────────────────────────
   IBM SECTION
───────────────────────────────────────────── */
function IBMSection() {
  const ref = useRef();
  const vis = useInView(ref, 0.15);

  return (
    <section ref={ref} style={{ padding: "160px 24px", borderTop: `1px solid ${C.border}` }}>
      <div style={{ maxWidth: 960, margin: "0 auto" }}>
        <SectionLabel label="IBM Integration" />
        <h2 style={{ fontFamily: FONT_DISPLAY, fontWeight: 400, fontSize: "clamp(36px, 5vw, 60px)", lineHeight: 1.08, letterSpacing: "-0.03em", color: C.text, margin: "16px 0 20px" }}>
          Enterprise AI,<br /><em style={{ fontStyle: "italic", color: C.accent }}>natively integrated.</em>
        </h2>
        <p style={{ fontSize: 16, color: C.textMuted, lineHeight: 1.75, maxWidth: 560, marginBottom: 72 }}>
          Every inference call, orchestration decision, and model evaluation runs through IBM's production-grade AI infrastructure.
        </p>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 20 }}>
          {IBM_STACK.map((item, i) => (
            <div key={item.name} style={{
              padding: 24, border: `1px solid ${C.border}`,
              borderRadius: 12, background: C.surface,
              opacity: vis ? 1 : 0, transform: vis ? "translateY(0)" : "translateY(24px)",
              transition: `all 0.6s cubic-bezier(.4,0,.2,1) ${i * 0.1}s`,
              cursor: "default",
            }}
              onMouseEnter={e => { e.currentTarget.style.borderColor = item.color + "66"; e.currentTarget.style.boxShadow = `0 0 24px ${item.color}22`; }}
              onMouseLeave={e => { e.currentTarget.style.borderColor = C.border; e.currentTarget.style.boxShadow = "none"; }}
            >
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 16 }}>
                <span style={{ fontSize: 15, fontWeight: 700, color: item.color }}>{item.name}</span>
                <Tag color={item.color}>{item.tag}</Tag>
              </div>
              <p style={{ fontSize: 13, color: C.textMuted, lineHeight: 1.7 }}>{item.desc}</p>
            </div>
          ))}
        </div>

        {/* Orchestration flow visual */}
        <div style={{ marginTop: 60, padding: 32, border: `1px solid ${C.border}`, borderRadius: 14, background: C.surface, fontFamily: FONT_MONO, fontSize: 12 }}>
          <div style={{ color: C.textDim, marginBottom: 20, fontSize: 11 }}>// orchestration_graph.yaml</div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr auto 1fr auto 1fr", gap: 16, alignItems: "center" }}>
            {[["IBM Bob", C.accent, "Orchestrator"], ["→", C.textDim, ""], ["Granite AI", C.purple, "34B-Code"], ["→", C.textDim, ""], ["watsonx.ai", C.green, "Platform"]].map(([name, color, sub], i) => (
              name === "→" ? (
                <div key={i} style={{ textAlign: "center", color, fontSize: 20 }}>→</div>
              ) : (
                <div key={i} style={{ padding: 16, border: `1px solid ${color}44`, borderRadius: 8, background: `${color}08`, textAlign: "center" }}>
                  <div style={{ color, fontWeight: 700, marginBottom: 4 }}>{name}</div>
                  <div style={{ color: C.textDim, fontSize: 10 }}>{sub}</div>
                </div>
              )
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function SectionLabel({ label }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 0 }}>
      <div style={{ width: 16, height: 1, background: C.accent }} />
      <span style={{ fontSize: 10, fontWeight: 600, letterSpacing: "0.14em", color: C.accent, textTransform: "uppercase", fontFamily: FONT_MONO }}>{label}</span>
    </div>
  );
}

/* ─────────────────────────────────────────────
   CINEMATIC LOADING SCREEN
───────────────────────────────────────────── */
function LoadingScreen({ onDone }) {
  const [lineIdx, setLineIdx] = useState(0);
  const [progress, setProgress] = useState(0);

  const loadLines = [
    { text: "Initializing IBM Bob Orchestrator...", color: C.accent, delay: 0 },
    { text: "Loading AI agent registry...", color: C.textMuted, delay: 600 },
    { text: "Connecting Granite-34B-Code model...", color: C.textMuted, delay: 1200 },
    { text: "Establishing watsonx.ai endpoints...", color: C.textMuted, delay: 1800 },
    { text: "Hydrating workflow pipeline...", color: C.textMuted, delay: 2400 },
    { text: "All systems operational.", color: C.green, delay: 3000 },
    { text: "Launching mission control...", color: C.accent, delay: 3600 },
  ];

  useEffect(() => {
    const timers = [];
    loadLines.forEach((l, i) => {
      timers.push(setTimeout(() => setLineIdx(i + 1), l.delay));
    });
    timers.push(setTimeout(() => setProgress(100), 100));
    timers.push(setTimeout(onDone, 4200));
    return () => timers.forEach(clearTimeout);
  }, []);

  return (
    <div style={{
      position: "fixed", inset: 0, background: C.bg, zIndex: 1000,
      display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
      fontFamily: FONT_MONO, animation: "fadeIn 0.3s ease",
    }}>
      {/* Scanline effect */}
      <div style={{ position: "absolute", inset: 0, overflow: "hidden", pointerEvents: "none", opacity: 0.03 }}>
        <div style={{ position: "absolute", left: 0, right: 0, height: "30%", background: `linear-gradient(transparent, ${C.accent}, transparent)`, animation: "scanline 3s linear infinite" }} />
      </div>

      <div style={{ textAlign: "center", maxWidth: 480, width: "100%", padding: "0 24px" }}>
        {/* Logo */}
        <div style={{ marginBottom: 60 }}>
          <div style={{ fontSize: 13, fontWeight: 700, letterSpacing: "0.15em", color: C.accent, marginBottom: 4 }}>AI CO-FOUNDER</div>
          <div style={{ fontSize: 10, color: C.textDim, letterSpacing: "0.2em" }}>MISSION CONTROL</div>
        </div>

        {/* Center glow orb */}
        <div style={{ position: "relative", width: 80, height: 80, margin: "0 auto 48px" }}>
          <div style={{ position: "absolute", inset: -20, borderRadius: "50%", background: `radial-gradient(circle, ${C.accentGlow} 0%, transparent 70%)`, animation: "pulse-glow 2s ease-in-out infinite" }} />
          <div style={{ width: "100%", height: "100%", borderRadius: "50%", border: `1px solid ${C.accent}66`, display: "flex", alignItems: "center", justifyContent: "center", animation: "spin 8s linear infinite" }}>
            <div style={{ width: 60, height: 60, borderRadius: "50%", border: `1px solid ${C.accent}44`, display: "flex", alignItems: "center", justifyContent: "center", animation: "spin 4s linear infinite reverse" }}>
              <div style={{ width: 8, height: 8, borderRadius: "50%", background: C.accent, boxShadow: `0 0 16px ${C.accent}` }} />
            </div>
          </div>
        </div>

        {/* Log lines */}
        <div style={{ textAlign: "left", marginBottom: 40, minHeight: 160 }}>
          {loadLines.slice(0, lineIdx).map((l, i) => (
            <div key={i} style={{ fontSize: 12, color: l.color, lineHeight: 2, animation: "fadeUp 0.3s ease" }}>
              <span style={{ color: C.textDim, marginRight: 8 }}>[{String(i).padStart(2, "0")}]</span>{l.text}
            </div>
          ))}
          {lineIdx < loadLines.length && (
            <div style={{ display: "inline-block", width: 8, height: 14, background: C.accent, animation: "blink 0.8s step-end infinite", verticalAlign: "text-bottom" }} />
          )}
        </div>

        {/* Progress bar */}
        <div style={{ height: 1, background: C.border, borderRadius: 1, overflow: "hidden" }}>
          <div style={{
            height: "100%", background: `linear-gradient(90deg, ${C.accent}, ${C.purple})`,
            width: `${Math.min((lineIdx / loadLines.length) * 100, 98)}%`,
            transition: "width 0.5s ease",
            boxShadow: `0 0 8px ${C.accent}`,
          }} />
        </div>
        <div style={{ fontSize: 10, color: C.textDim, marginTop: 8, textAlign: "right" }}>
          {Math.round(Math.min((lineIdx / loadLines.length) * 100, 98))}%
        </div>
      </div>
    </div>
  );
}

/* ─────────────────────────────────────────────
   DASHBOARD
───────────────────────────────────────────── */
function Dashboard({ idea }) {
  const [termLines, setTermLines] = useState([]);
  const [stageState, setStageState] = useState({}); // id -> "active"|"done"
  const [activeTab, setActiveTab] = useState("validation");
  const [unlockedTabs, setUnlockedTabs] = useState(new Set());
  const [globalProgress, setGlobalProgress] = useState(0);
  const termRef = useRef();
  const [ideaVal, setIdeaVal] = useState(idea || "");
  const [running, setRunning] = useState(!!idea);
  const [prUrl, setPrUrl] = useState(GITHUB_PULLS_URL);
  const [backendError, setBackendError] = useState("");
  const [backendResponse, setBackendResponse] = useState(null);

  const runOrchestration = useCallback(async () => {
    if (!ideaVal.trim()) return;
    setRunning(true);
    setTermLines([]);
    setStageState({});
    setUnlockedTabs(new Set());
    setGlobalProgress(0);
    setBackendError("");
    setPrUrl(GITHUB_PULLS_URL);

    const totalTime = TERMINAL_SEQUENCE[TERMINAL_SEQUENCE.length - 1].t;

    // Call backend API
    try {
      const backendRes = await fetch("http://localhost:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idea: ideaVal, live_mode: false })
      });
      
      if (backendRes.ok) {
        const data = await backendRes.json();
        setBackendResponse(data);
        
        // Confirm GitHub stage produced PR metadata (live pipeline)
        if (data.data?.stages?.github?.pull_request_info?.title) {
          setPrUrl(GITHUB_PULLS_URL);
        }
      } else {
        setBackendError("Backend API returned an error");
        console.error("Backend error:", backendRes.status);
      }
    } catch (e) {
      setBackendError("Could not connect to backend. Running in simulation mode.");
      console.error("Backend connection error:", e);
    }

    TERMINAL_SEQUENCE.forEach((line, i) => {
      setTimeout(() => {
        setTermLines(prev => [...prev, line]);
        setGlobalProgress(Math.round((line.t / totalTime) * 100));

        // Unlock tabs based on line index
        if (i >= 6)  { setStageState(p => ({ ...p, validation: i < 11 ? "active" : "done" })); setUnlockedTabs(p => new Set([...p, "validation"])); }
        if (i >= 12) { setStageState(p => ({ ...p, architecture: i < 17 ? "active" : "done" })); setUnlockedTabs(p => new Set([...p, "architecture"])); }
        if (i >= 18) { setStageState(p => ({ ...p, codegen: i < 22 ? "active" : "done" })); setUnlockedTabs(p => new Set([...p, "codegen"])); }
        if (i >= 23) { setStageState(p => ({ ...p, security: i < 27 ? "active" : "done" })); setUnlockedTabs(p => new Set([...p, "security"])); }
        if (i >= 28) { setStageState(p => ({ ...p, github: i < 32 ? "active" : "done" })); setUnlockedTabs(p => new Set([...p, "github"])); }

        // Auto-switch active tab
        if (i === 6)  setActiveTab("validation");
        if (i === 12) setActiveTab("architecture");
        if (i === 18) setActiveTab("codegen");
        if (i === 23) setActiveTab("security");
        if (i === 28) setActiveTab("github");

        if (termRef.current) termRef.current.scrollTop = termRef.current.scrollHeight;
      }, line.t);
    });
  }, [ideaVal]);

  useEffect(() => { if (idea) { setTimeout(runOrchestration, 100); } }, []);

  const TABS = [
    { id: "validation", label: "Validation", color: C.green },
    { id: "architecture", label: "Architecture", color: C.accent },
    { id: "codegen", label: "Code", color: C.purple },
    { id: "security", label: "Security", color: C.amber },
    { id: "github", label: "GitHub PR", color: C.red },
  ];

  const stageForTab = { validation: 0, architecture: 1, codegen: 2, security: 3, github: 4 };

  return (
    <div style={{ height: "100vh", display: "flex", flexDirection: "column", background: C.bg, overflow: "hidden" }}>

      {/* TOP HEADER */}
      <header style={{
        height: 52, borderBottom: `1px solid ${C.border}`,
        display: "flex", alignItems: "center", padding: "0 20px", gap: 16,
        background: C.surface, flexShrink: 0,
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <div style={{ width: 20, height: 20, borderRadius: 5, background: `linear-gradient(135deg, ${C.accent}, ${C.purple})`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 10, fontWeight: 700, color: "#000" }}>A</div>
          <span style={{ fontSize: 13, fontWeight: 700, letterSpacing: "0.02em", color: C.text }}>AI Co-founder</span>
        </div>

        <div style={{ width: 1, height: 20, background: C.border }} />

        {/* IBM Bob indicator */}
        <div style={{ display: "flex", alignItems: "center", gap: 6, padding: "4px 10px", border: `1px solid ${C.border}`, borderRadius: 6, background: `${C.accent}0a` }}>
          <Dot color={C.accent} animate />
          <span style={{ fontSize: 11, color: C.accent, fontFamily: FONT_MONO, fontWeight: 600 }}>IBM Bob ACTIVE</span>
        </div>

        <div style={{ flex: 1 }} />

        {/* Progress */}
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{ width: 120, height: 3, background: C.border, borderRadius: 2 }}>
            <div style={{ height: "100%", width: `${globalProgress}%`, background: `linear-gradient(90deg, ${C.accent}, ${C.purple})`, borderRadius: 2, transition: "width 0.4s ease", boxShadow: globalProgress > 0 ? `0 0 8px ${C.accent}` : "none" }} />
          </div>
          <span style={{ fontSize: 11, color: C.textMuted, fontFamily: FONT_MONO, minWidth: 36 }}>{globalProgress}%</span>
        </div>

        {/* Status pill */}
        <div style={{ display: "flex", alignItems: "center", gap: 6, padding: "4px 10px", border: `1px solid ${globalProgress === 100 ? C.green + "66" : C.border}`, borderRadius: 6 }}>
          <Dot color={globalProgress === 100 ? C.green : C.amber} animate={globalProgress < 100 && running} />
          <span style={{ fontSize: 11, color: globalProgress === 100 ? C.green : C.amber, fontFamily: FONT_MONO }}>
            {globalProgress === 0 ? "IDLE" : globalProgress === 100 ? "COMPLETE" : "ORCHESTRATING"}
          </span>
        </div>
      </header>

      {/* MAIN BODY */}
      <div style={{ flex: 1, display: "grid", gridTemplateColumns: "200px 1fr 320px", overflow: "hidden" }}>

        {/* SIDEBAR */}
        <aside style={{ borderRight: `1px solid ${C.border}`, background: C.surface, display: "flex", flexDirection: "column", overflow: "hidden" }}>
          {/* Pipeline stages */}
          <div style={{ padding: "16px 0 8px" }}>
            <div style={{ padding: "0 16px 10px", fontSize: 9, fontWeight: 700, letterSpacing: "0.14em", color: C.textDim, textTransform: "uppercase", fontFamily: FONT_MONO }}>Pipeline</div>
            {PIPELINE_STAGES.map((s, i) => {
              const state = stageState[s.id];
              return (
                <div key={s.id} style={{
                  display: "flex", alignItems: "center", gap: 10, padding: "9px 16px",
                  background: state === "active" ? `${s.color}0a` : "transparent",
                  borderLeft: `2px solid ${state === "done" ? s.color : state === "active" ? s.color : "transparent"}`,
                  transition: "all 0.3s",
                }}>
                  <div style={{
                    width: 24, height: 24, borderRadius: "50%",
                    border: `1px solid ${state ? s.color : C.border}`,
                    background: state === "done" ? `${s.color}22` : "transparent",
                    display: "flex", alignItems: "center", justifyContent: "center",
                    fontSize: 10, color: state ? s.color : C.textDim,
                    flexShrink: 0, fontFamily: FONT_MONO,
                    boxShadow: state === "active" ? `0 0 10px ${s.color}55` : "none",
                    transition: "all 0.4s",
                  }}>
                    {state === "done" ? "✓" : s.icon}
                  </div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontSize: 12, color: state ? C.text : C.textDim, fontWeight: state ? 600 : 400, transition: "color 0.3s", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{s.label}</div>
                    <div style={{ fontSize: 10, color: state === "done" ? C.green : state === "active" ? s.color : C.textDim, fontFamily: FONT_MONO }}>
                      {state === "done" ? "done" : state === "active" ? "running" : "pending"}
                    </div>
                  </div>
                  {state === "active" && <div style={{ width: 12, height: 12, borderRadius: "50%", border: `1.5px solid ${s.color}`, borderTopColor: "transparent", animation: "spin 0.7s linear infinite", flexShrink: 0 }} />}
                </div>
              );
            })}
          </div>

          <Divider style={{ margin: "8px 0" }} />

          {/* Nav items */}
          <div style={{ padding: "8px 0" }}>
            <div style={{ padding: "0 16px 10px", fontSize: 9, fontWeight: 700, letterSpacing: "0.14em", color: C.textDim, textTransform: "uppercase", fontFamily: FONT_MONO }}>Project</div>
            {["Overview", "Files", "Agents", "Settings"].map(item => (
              <div key={item} style={{ padding: "8px 16px", fontSize: 12, color: C.textDim, cursor: "pointer", transition: "color 0.2s" }}
                onMouseEnter={e => e.currentTarget.style.color = C.text}
                onMouseLeave={e => e.currentTarget.style.color = C.textDim}
              >{item}</div>
            ))}
          </div>

          {/* IBM status at bottom */}
          <div style={{ marginTop: "auto", padding: 14, borderTop: `1px solid ${C.border}` }}>
            <div style={{ fontSize: 9, color: C.textDim, letterSpacing: "0.1em", textTransform: "uppercase", fontFamily: FONT_MONO, marginBottom: 8 }}>IBM Stack</div>
            {[{ label: "Bob", color: C.accent }, { label: "Granite", color: C.purple }, { label: "watsonx", color: C.green }].map(x => (
              <div key={x.label} style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 5 }}>
                <Dot color={x.color} animate={running && globalProgress < 100} />
                <span style={{ fontSize: 11, color: C.textMuted, fontFamily: FONT_MONO }}>{x.label}</span>
              </div>
            ))}
          </div>
        </aside>

        {/* CENTER — idea input + pipeline */}
        <main style={{ display: "flex", flexDirection: "column", overflow: "hidden" }}>
          {/* Idea input bar */}
          <div style={{ padding: "20px 24px", borderBottom: `1px solid ${C.border}`, background: C.surface, flexShrink: 0 }}>
            <div style={{ fontSize: 10, color: C.textDim, letterSpacing: "0.12em", textTransform: "uppercase", fontFamily: FONT_MONO, marginBottom: 10 }}>Startup Idea</div>
            {backendError && (
              <div style={{ padding: "8px 12px", borderRadius: 6, background: `${C.amber}1a`, border: `1px solid ${C.amber}44`, marginBottom: 10, fontSize: 12, color: C.amber, fontFamily: FONT_MONO }}>
                ⚠ {backendError}
              </div>
            )}
            <div style={{ display: "flex", gap: 10 }}>
              <input
                value={ideaVal}
                onChange={e => setIdeaVal(e.target.value)}
                onKeyDown={e => e.key === "Enter" && runOrchestration()}
                placeholder="Describe your startup idea..."
                disabled={running && globalProgress < 100}
                style={{
                  flex: 1, background: C.bg, border: `1px solid ${C.border}`, borderRadius: 8,
                  padding: "10px 14px", fontSize: 13, color: C.text, outline: "none",
                  fontFamily: FONT_BODY,
                  opacity: running && globalProgress < 100 ? 0.6 : 1,
                }}
                onFocus={e => e.target.style.borderColor = C.accent + "66"}
                onBlur={e => e.target.style.borderColor = C.border}
              />
              <button
                onClick={runOrchestration}
                disabled={running && globalProgress < 100}
                style={{
                  padding: "10px 20px", borderRadius: 8,
                  background: running && globalProgress < 100 ? C.border : C.accent,
                  border: "none", color: running && globalProgress < 100 ? C.textDim : "#000",
                  fontWeight: 700, fontSize: 12, cursor: running && globalProgress < 100 ? "default" : "pointer",
                  letterSpacing: "0.04em", transition: "all 0.2s", whiteSpace: "nowrap",
                }}>
                {running && globalProgress < 100 ? "Running..." : "Orchestrate →"}
              </button>
            </div>
          </div>

          {/* Pipeline visualization center */}
          <div style={{ padding: "28px 24px", borderBottom: `1px solid ${C.border}`, flexShrink: 0 }}>
            <div style={{ fontSize: 10, color: C.textDim, letterSpacing: "0.12em", textTransform: "uppercase", fontFamily: FONT_MONO, marginBottom: 20 }}>Orchestration Pipeline</div>
            <div style={{ display: "flex", alignItems: "center" }}>
              {/* idea node */}
              <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 6, flexShrink: 0 }}>
                <div style={{ width: 36, height: 36, borderRadius: "50%", border: `1px solid ${C.borderLight}`, background: C.surfaceHover, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 13, color: C.textMuted }}>◇</div>
                <span style={{ fontSize: 9, color: C.textDim, letterSpacing: "0.06em" }}>IDEA</span>
              </div>

              {PIPELINE_STAGES.map((s, i) => {
                const state = stageState[s.id];
                return (
                  <div key={s.id} style={{ display: "flex", alignItems: "center", flex: 1 }}>
                    <div style={{ flex: 1, height: 1, background: C.border, position: "relative", overflow: "hidden" }}>
                      <div style={{
                        position: "absolute", inset: 0,
                        background: state ? s.color : "transparent",
                        transition: "background 0.5s",
                      }} />
                    </div>
                    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 6, flexShrink: 0 }}>
                      <div style={{ position: "relative" }}>
                        {state === "active" && <div style={{ position: "absolute", inset: -8, borderRadius: "50%", background: `radial-gradient(circle, ${s.glow}, transparent)`, animation: "ping 1.5s ease-out infinite" }} />}
                        <div style={{
                          width: 40, height: 40, borderRadius: "50%",
                          border: `1.5px solid ${state ? s.color : C.border}`,
                          background: state === "done" ? `${s.color}20` : state === "active" ? `${s.color}0d` : C.surface,
                          display: "flex", alignItems: "center", justifyContent: "center",
                          fontSize: 14, color: state ? s.color : C.textDim,
                          boxShadow: state === "active" ? `0 0 20px ${s.color}66` : state === "done" ? `0 0 10px ${s.color}33` : "none",
                          transition: "all 0.4s", fontFamily: FONT_MONO, fontWeight: 700,
                        }}>
                          {state === "done" ? "✓" : state === "active" ? <div style={{ width: 14, height: 14, borderRadius: "50%", border: `1.5px solid ${s.color}`, borderTopColor: "transparent", animation: "spin 0.7s linear infinite" }} /> : s.icon}
                        </div>
                      </div>
                      <span style={{ fontSize: 9, color: state ? C.text : C.textDim, letterSpacing: "0.06em", whiteSpace: "nowrap", transition: "color 0.3s" }}>{s.label.toUpperCase()}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Output tabs */}
          <div style={{ borderBottom: `1px solid ${C.border}`, display: "flex", flexShrink: 0 }}>
            {TABS.map(t => {
              const unlocked = unlockedTabs.has(t.id);
              const active = activeTab === t.id;
              return (
                <button key={t.id}
                  onClick={() => unlocked && setActiveTab(t.id)}
                  style={{
                    padding: "10px 16px", border: "none",
                    background: active ? `${t.color}0d` : "transparent",
                    borderBottom: active ? `2px solid ${t.color}` : "2px solid transparent",
                    color: !unlocked ? C.textDim : active ? t.color : C.textMuted,
                    fontSize: 12, fontWeight: active ? 600 : 400,
                    cursor: unlocked ? "pointer" : "default",
                    letterSpacing: "0.02em", transition: "all 0.2s",
                    opacity: unlocked ? 1 : 0.4,
                    fontFamily: FONT_BODY,
                  }}>
                  {t.label}
                  {!unlocked && <span style={{ marginLeft: 4, fontSize: 9, color: C.textDim }}>○</span>}
                  {unlocked && stageState[t.id] === "active" && <span style={{ marginLeft: 6, display: "inline-block", width: 5, height: 5, borderRadius: "50%", background: t.color, animation: "blink 1s ease-in-out infinite", verticalAlign: "middle" }} />}
                </button>
              );
            })}
          </div>

          {/* Tab content */}
          <div style={{ flex: 1, overflowY: "auto", padding: 24 }}>
            <TabContent
  tab={activeTab}
  unlocked={unlockedTabs.has(activeTab)}
  idea={ideaVal}
  prUrl={prUrl}
  running={running}
/>
          </div>
        </main>

        {/* RIGHT TERMINAL */}
        <div style={{ borderLeft: `1px solid ${C.border}`, display: "flex", flexDirection: "column", overflow: "hidden" }}>
          <div style={{ padding: "14px 16px", borderBottom: `1px solid ${C.border}`, display: "flex", alignItems: "center", gap: 8, flexShrink: 0 }}>
            <div style={{ width: 8, height: 8, borderRadius: "50%", background: C.red }} />
            <div style={{ width: 8, height: 8, borderRadius: "50%", background: C.amber }} />
            <div style={{ width: 8, height: 8, borderRadius: "50%", background: C.green }} />
            <span style={{ marginLeft: 8, fontSize: 11, color: C.textDim, fontFamily: FONT_MONO }}>ibm-bob — orchestrator</span>
          </div>
          <div ref={termRef} style={{
            flex: 1, overflowY: "auto", padding: "16px",
            background: "#050507",
            fontFamily: FONT_MONO, fontSize: 11, lineHeight: 1.9,
          }}>
            {termLines.map((line, i) => {
              if (line.kind === "divider") return <div key={i} style={{ height: 1, background: C.border, margin: "8px 0", opacity: 0.5 }} />;
              if (line.kind === "cursor") return (
                <div key={i} style={{ color: C.text }}>
                  {line.text.slice(0, -1)}<span style={{ animation: "blink 1s step-end infinite", background: C.text, display: "inline-block", width: 7, height: 13, verticalAlign: "text-bottom" }} />
                </div>
              );
              const color = line.kind === "success" ? C.green : line.kind === "info" ? C.accent : line.kind === "sys" ? C.purple : line.kind === "warn" ? C.amber : C.textMuted;
              const prefix = line.kind === "sys" ? "" : line.kind === "success" ? "" : line.kind === "warn" ? "" : "";
              return (
                <div key={i} style={{ color, animation: "fadeUp 0.2s ease" }}>{line.text}</div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

/* ─────────────────────────────────────────────
   TAB CONTENT
───────────────────────────────────────────── */
function TabContent({ tab, unlocked, idea, prUrl, running }: { tab: string; unlocked: boolean; idea: string; prUrl?: string; running: boolean }) {
  if (!unlocked) return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100%", gap: 12, opacity: 0.5 }}>
      <div style={{ fontSize: 24, color: C.textDim }}>○</div>
      <div style={{ fontSize: 13, color: C.textDim, fontFamily: FONT_MONO }}>Awaiting stage completion...</div>
    </div>
  );

  const content: Record<string, React.ReactElement> = {
    validation: <ValidationOutput idea={idea} />,
    architecture: <ArchOutput />,
    codegen: <CodeOutput />,
    security: <SecurityOutput />,
    github: <GitHubOutput idea={idea} prUrl={prUrl} running={running} />,
  };

  return <div style={{ animation: "fadeUp 0.4s ease" }}>{content[tab]}</div>;
}

function OutputSection({ title, children }) {
  return (
    <div style={{ marginBottom: 28 }}>
      <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: "0.12em", color: C.textDim, textTransform: "uppercase", fontFamily: FONT_MONO, marginBottom: 14 }}>{title}</div>
      {children}
    </div>
  );
}

function ValidationOutput({ idea }) {
  return (
    <div>
      <OutputSection title="PMF Analysis">
        {[{ k: "PMF Score", v: "87 / 100", bar: 87, c: C.green }, { k: "TAM", v: "$4.2B", bar: 72, c: C.accent }, { k: "SAM", v: "$640M", bar: 45, c: C.accent }, { k: "Competition", v: "Moderate", bar: 50, c: C.amber }, { k: "Urgency", v: "High", bar: 80, c: C.purple }].map(r => (
          <div key={r.k} style={{ marginBottom: 14 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6, fontSize: 12, fontFamily: FONT_MONO }}>
              <span style={{ color: C.textMuted }}>{r.k}</span><span style={{ color: r.c, fontWeight: 700 }}>{r.v}</span>
            </div>
            <div style={{ height: 3, background: C.border, borderRadius: 2 }}>
              <div style={{ height: "100%", width: `${r.bar}%`, background: r.c, borderRadius: 2, transition: "width 1s ease" }} />
            </div>
          </div>
        ))}
      </OutputSection>
      <OutputSection title="Verdict">
        <div style={{ padding: 16, border: `1px solid ${C.green}44`, borderRadius: 8, background: `${C.green}08` }}>
          <div style={{ fontSize: 13, color: C.green, fontWeight: 700, marginBottom: 6 }}>✓ GO — Strong market signal</div>
          <div style={{ fontSize: 12, color: C.textMuted, lineHeight: 1.7 }}>Recommend B2B SaaS with usage-based pricing. Target mid-market engineering teams. Estimated 18-month runway to Series A at current burn assumptions.</div>
        </div>
      </OutputSection>
    </div>
  );
}

function ArchOutput() {
  return (
    <div>
      <OutputSection title="Stack Selection">
        <div style={{ fontFamily: FONT_MONO, fontSize: 12 }}>
          {[["frontend", "Next.js 14 · Tailwind · shadcn/ui", C.accent], ["api_layer", "tRPC + REST + GraphQL gateway", C.accent], ["database", "PostgreSQL 16 · Prisma ORM", C.purple], ["cache", "Redis Cluster · Edge KV", C.purple], ["auth", "NextAuth v5 · RBAC · MFA", C.green], ["storage", "AWS S3 · CloudFront CDN", C.green], ["payments", "Stripe · metered billing", C.amber], ["infra", "Vercel · Terraform · Docker", C.amber]].map(([k, v, c]) => (
            <div key={k} style={{ display: "flex", gap: 16, marginBottom: 10, padding: "6px 10px", borderRadius: 6, background: C.surfaceHover }}>
              <span style={{ color: c, minWidth: 90, flexShrink: 0 }}>{k}:</span>
              <span style={{ color: C.textMuted }}>{v}</span>
            </div>
          ))}
        </div>
      </OutputSection>
      <OutputSection title="Services (12)">
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, fontSize: 11, fontFamily: FONT_MONO }}>
          {["auth-service", "user-service", "billing-service", "analytics-service", "notification-service", "file-service", "search-service", "webhook-service", "audit-service", "gateway-service", "worker-service", "admin-service"].map(s => (
            <div key={s} style={{ padding: "6px 10px", border: `1px solid ${C.border}`, borderRadius: 5, color: C.textMuted }}>◈ {s}</div>
          ))}
        </div>
      </OutputSection>
    </div>
  );
}

function CodeOutput() {
  return (
    <div>
      <OutputSection title="File Tree (47 files)">
        <div style={{ fontFamily: FONT_MONO, fontSize: 11, lineHeight: 2, color: C.textMuted }}>
          {["app/", "  api/", "    metrics/route.ts", "    auth/route.ts", "    stripe/webhook.ts", "  dashboard/page.tsx", "  layout.tsx", "components/", "  ui/", "  charts/", "lib/", "  db.ts", "  auth.ts", "  stripe.ts", "prisma/", "  schema.prisma", "  migrations/", "__tests__/", "  api.test.ts", "  ...38 more files"].map((line, i) => (
            <div key={i} style={{ color: line.endsWith("/") ? C.accent : line.startsWith("  ") ? C.textMuted : C.text }}>{line}</div>
          ))}
        </div>
      </OutputSection>
      <OutputSection title="Sample — app/api/metrics/route.ts">
        <div style={{ background: "#050507", border: `1px solid ${C.border}`, borderRadius: 8, padding: 16, fontFamily: FONT_MONO, fontSize: 11, lineHeight: 1.9 }}>
          <div><span style={{ color: "#7dd3fc" }}>import</span> <span style={{ color: C.text }}>{"{ db }"}</span> <span style={{ color: "#7dd3fc" }}>from</span> <span style={{ color: "#86efac" }}>"@/lib/db"</span></div>
          <div><span style={{ color: "#7dd3fc" }}>import</span> <span style={{ color: C.text }}>{"{ auth }"}</span> <span style={{ color: "#7dd3fc" }}>from</span> <span style={{ color: "#86efac" }}>"@/lib/auth"</span></div>
          <br />
          <div><span style={{ color: "#7dd3fc" }}>export async function</span> <span style={{ color: C.accent }}>GET</span><span style={{ color: C.text }}>(req: Request) {"{"}</span></div>
          <div style={{ paddingLeft: 20 }}><span style={{ color: "#7dd3fc" }}>const</span> <span style={{ color: C.text }}>session = </span><span style={{ color: "#7dd3fc" }}>await</span> <span style={{ color: C.amber }}>auth</span><span style={{ color: C.text }}>()</span></div>
          <div style={{ paddingLeft: 20 }}><span style={{ color: "#7dd3fc" }}>if</span> <span style={{ color: C.text }}>(!session) </span><span style={{ color: "#7dd3fc" }}>return</span> <span style={{ color: C.red }}>new Response</span><span style={{ color: C.text }}>(</span><span style={{ color: "#86efac" }}>"Unauthorized"</span><span style={{ color: C.text }}>, {"{ status: 401 }"})</span></div>
          <div style={{ paddingLeft: 20 }}><span style={{ color: "#7dd3fc" }}>const</span> <span style={{ color: C.text }}>data = </span><span style={{ color: "#7dd3fc" }}>await</span> <span style={{ color: C.text }}>db.metric.</span><span style={{ color: C.amber }}>findMany</span><span style={{ color: C.text }}>({"{"}where: {"{ orgId: session.orgId }"}{"}"}</span><span style={{ color: C.text }}>)</span></div>
          <div style={{ paddingLeft: 20 }}><span style={{ color: "#7dd3fc" }}>return</span> <span style={{ color: C.red }}>Response</span><span style={{ color: C.text }}>.</span><span style={{ color: C.amber }}>json</span><span style={{ color: C.text }}>({"{"}data{"}"})</span></div>
          <div><span style={{ color: C.text }}>{"}"}</span></div>
        </div>
      </OutputSection>
    </div>
  );
}

function SecurityOutput() {
  return (
    <div>
      <OutputSection title="OWASP Top-10 Results">
        {[{ name: "A01 Broken Access Control", status: "pass", sev: null }, { name: "A02 Cryptographic Failures", status: "pass", sev: null }, { name: "A03 Injection", status: "pass", sev: null }, { name: "A04 Insecure Design", status: "patched", sev: "MEDIUM" }, { name: "A05 Security Misconfiguration", status: "patched", sev: "MEDIUM" }, { name: "A06 Vulnerable Components", status: "pass", sev: null }, { name: "A07 Auth Failures", status: "pass", sev: null }, { name: "A08 Software Integrity Failures", status: "pass", sev: null }, { name: "A09 Logging Failures", status: "pass", sev: null }, { name: "A10 SSRF", status: "pass", sev: null }].map(r => (
          <div key={r.name} style={{ display: "flex", alignItems: "center", gap: 10, padding: "7px 0", borderBottom: `1px solid ${C.border}33`, fontSize: 12, fontFamily: FONT_MONO }}>
            <span style={{ color: r.status === "pass" ? C.green : C.amber, minWidth: 60 }}>{r.status === "pass" ? "✓ PASS" : "⚠ FIXED"}</span>
            <span style={{ color: C.textMuted, flex: 1 }}>{r.name}</span>
            {r.sev && <Tag color={C.amber}>{r.sev}</Tag>}
          </div>
        ))}
      </OutputSection>
      <OutputSection title="Summary">
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: 10 }}>
          {[{ label: "Critical", val: 0, c: C.red }, { label: "High", val: 0, c: C.amber }, { label: "Medium", val: 2, c: C.amber, note: "patched" }, { label: "Low", val: 0, c: C.green }].map(r => (
            <div key={r.label} style={{ padding: 12, border: `1px solid ${C.border}`, borderRadius: 8, textAlign: "center" }}>
              <div style={{ fontSize: 22, fontWeight: 700, color: r.val === 0 ? C.textDim : r.c, fontFamily: FONT_MONO }}>{r.val}</div>
              <div style={{ fontSize: 10, color: C.textDim, marginTop: 4 }}>{r.label}</div>
              {r.note && <div style={{ fontSize: 9, color: C.amber, marginTop: 2 }}>({r.note})</div>}
            </div>
          ))}
        </div>
      </OutputSection>
    </div>
  );
}

function GitHubOutput({ idea, prUrl, running }: { idea: string; prUrl?: string; running: boolean }) {
  return (
    <div>
      <OutputSection title="Pull Request">
        <div style={{ border: `1px solid ${C.border}`, borderRadius: 10, overflow: "hidden" }}>
          <div style={{ padding: "14px 18px", borderBottom: `1px solid ${C.border}`, background: C.surfaceHover, display: "flex", gap: 10, alignItems: "center", flexWrap: "wrap" }}>
            <span style={{ fontSize: 13, fontWeight: 700, color: C.text, fontFamily: FONT_MONO }}>PR #1</span>
            <Tag color={C.green}>Open</Tag>
            <span style={{ fontSize: 12, color: C.textMuted }}>feat: initial scaffold — production-ready SaaS foundation</span>
          </div>
          <div style={{ padding: "16px 18px", fontFamily: FONT_MONO, fontSize: 12 }}>
            <div style={{ color: C.textDim, marginBottom: 10 }}>Opened by <span style={{ color: C.accent }}>ai-cofounder[bot]</span> · <span style={{ color: C.textMuted }}>main ← feat/initial-scaffold</span></div>
            <div style={{ background: "#050507", border: `1px solid ${C.border}`, borderRadius: 6, padding: 14, lineHeight: 1.9 }}>
              <div style={{ color: C.textMuted, marginBottom: 8 }}>## Summary</div>
              <div style={{ color: C.textMuted }}>Auto-generated scaffold from idea: <span style={{ color: C.text }}>"{idea || "SaaS platform"}"</span></div>
              <div style={{ height: 8 }} />
              <div style={{ color: C.textMuted }}>## Changes</div>
              <div style={{ color: C.green }}>+ 47 files changed, 4,821 insertions(+)</div>
              <div style={{ color: C.textMuted }}>✓ CI: passing  ·  lint: clean  ·  tests: 94%</div>
              <div style={{ color: C.textMuted }}>✓ Security: 0 critical, 0 high (2 medium auto-patched)</div>
            </div>
            <div style={{ marginTop: 16 }}>
              <button
                onClick={() => {
                  if (prUrl) {
                    window.open(prUrl, '_blank');
                  } else {
                    alert("PR URL not available. Please ensure the orchestration completed successfully.");
                  }
                }}
                disabled={!prUrl || !running}
                style={{
                  padding: "10px 20px",
                  borderRadius: 8,
                  background: prUrl && running ? C.accent : C.textDim,
                  border: "none",
                  color: "#000",
                  fontWeight: 700,
                  fontSize: 12,
                  cursor: prUrl && running ? "pointer" : "default",
                  letterSpacing: "0.04em",
                  transition: "all 0.2s",
                  fontFamily: FONT_BODY,
                  boxShadow: prUrl ? `0 0 20px ${C.accentGlow}` : "none",
                  opacity: prUrl ? 1 : 0.5,
                }}
                onMouseEnter={e => {
                  if (prUrl && running) {
                    (e.target as HTMLButtonElement).style.transform = "translateY(-2px)";
                    (e.target as HTMLButtonElement).style.boxShadow = `0 0 30px ${C.accentGlow}`;
                  }
                }}
                onMouseLeave={e => {
                  if (prUrl && running) {
                    (e.target as HTMLButtonElement).style.transform = "translateY(0)";
                    (e.target as HTMLButtonElement).style.boxShadow = `0 0 20px ${C.accentGlow}`;
                  }
                }}
              >
                Open PR →
              </button>
            </div>
          </div>
        </div>
      </OutputSection>
      <OutputSection title="CI Checks">
        {[["Build", C.green, "✓ Passed · 42s"], ["Lint", C.green, "✓ 0 errors · 0 warnings"], ["Tests", C.green, "✓ 94% coverage · 118 passed"], ["Security Scan", C.green, "✓ 0 critical findings"], ["Type Check", C.green, "✓ No type errors"]].map(([name, c, detail]) => (
          <div key={name} style={{ display: "flex", alignItems: "center", gap: 10, padding: "8px 0", borderBottom: `1px solid ${C.border}33`, fontSize: 12, fontFamily: FONT_MONO }}>
            <span style={{ color: c }}>●</span>
            <span style={{ color: C.text, minWidth: 120 }}>{name}</span>
            <span style={{ color: C.textMuted }}>{detail}</span>
          </div>
        ))}
      </OutputSection>
    </div>
  );
}

/* ─────────────────────────────────────────────
   FINAL CTA
───────────────────────────────────────────── */
function FinalCTA({ onStart }) {
  return (
    <section style={{ padding: "180px 24px", borderTop: `1px solid ${C.border}`, textAlign: "center", position: "relative", overflow: "hidden" }}>
      <div style={{ position: "absolute", width: 800, height: 500, background: `radial-gradient(ellipse, ${C.accentGlow} 0%, transparent 60%)`, top: "50%", left: "50%", transform: "translate(-50%,-50%)", pointerEvents: "none" }} />
      <div style={{ position: "relative", maxWidth: 640, margin: "0 auto" }}>
        <h2 style={{ fontFamily: FONT_DISPLAY, fontSize: "clamp(48px, 7vw, 80px)", fontWeight: 400, lineHeight: 1.06, letterSpacing: "-0.03em", color: C.text, margin: "0 0 24px" }}>
          Stop planning.<br />
          <em style={{ fontStyle: "italic", background: `linear-gradient(135deg, ${C.accent}, ${C.purple})`, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", backgroundClip: "text" }}>Start executing.</em>
        </h2>
        <p style={{ fontSize: 17, color: C.textMuted, lineHeight: 1.75, marginBottom: 48 }}>Your AI co-founder is ready. One idea is all it takes.</p>
        <button onClick={onStart} style={{
          padding: "16px 44px", borderRadius: 12, background: C.accent,
          border: "none", color: "#000", fontWeight: 700, fontSize: 15, cursor: "pointer",
          letterSpacing: "0.02em", boxShadow: `0 0 48px ${C.accentGlow}`,
          transition: "all 0.3s",
        }}
          onMouseEnter={e => { e.target.style.transform = "translateY(-2px)"; e.target.style.boxShadow = `0 0 80px ${C.accentGlow}`; }}
          onMouseLeave={e => { e.target.style.transform = "translateY(0)"; e.target.style.boxShadow = `0 0 48px ${C.accentGlow}`; }}
        >
          Launch Mission Control →
        </button>
        <div style={{ marginTop: 20, fontSize: 12, color: C.textDim }}>No credit card · First startup free · IBM infrastructure</div>
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────
   FOOTER
───────────────────────────────────────────── */
function Footer() {
  return (
    <footer style={{ borderTop: `1px solid ${C.border}`, padding: "40px 24px", display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: 16 }}>
      <div style={{ fontSize: 12, color: C.textDim, fontFamily: FONT_MONO }}>AI Co-founder © 2025 — Powered by IBM Bob · Granite AI · watsonx.ai</div>
      <div style={{ display: "flex", gap: 24 }}>
        {["Docs", "API", "Status", "Privacy"].map(l => (
          <span key={l} style={{ fontSize: 12, color: C.textDim, cursor: "pointer", transition: "color 0.2s" }}
            onMouseEnter={e => e.target.style.color = C.text}
            onMouseLeave={e => e.target.style.color = C.textDim}
          >{l}</span>
        ))}
      </div>
    </footer>
  );
}

/* ─────────────────────────────────────────────
   ROOT APP
───────────────────────────────────────────── */
export default function App() {
  const [view, setView] = useState("landing"); // landing | loading | dashboard
  const [idea, setIdea] = useState("");

  const handleStart = (val = "") => {
    setIdea(val || "SaaS analytics platform for engineering teams");
    setView("loading");
  };

  return (
    <>
      <GlobalStyle />
      <Noise />

      {view === "loading" && (
        <LoadingScreen onDone={() => setView("dashboard")} />
      )}

      {view === "dashboard" && (
        <Dashboard idea={idea} />
      )}

      {view === "landing" && (
        <div style={{ background: C.bg, minHeight: "100vh" }}>
          <Hero onStart={() => handleStart()} />
          <PipelineViz />
          <FeatureSections />
          <IBMSection />
          <FinalCTA onStart={() => handleStart()} />
          <Footer />
        </div>
      )}
    </>
  );
}

