import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Engineer · Portfolio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700&family=Syne:wght@400;600;700;800&display=swap');

/* ---- Base ---- */
html, body, [class*="css"] { font-family: 'Syne', sans-serif; }

.stApp {
    background: #080c10;
    color: #e2e8f0;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; padding-bottom: 0 !important; max-width: 100% !important; }

/* ---- Scrollbar ---- */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #080c10; }
::-webkit-scrollbar-thumb { background: #00d4ff; border-radius: 2px; }

/* ---- Noise overlay ---- */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.025'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 9999;
}

/* ---- Nav bar ---- */
.navbar {
    position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
    display: flex; justify-content: space-between; align-items: center;
    padding: 18px 48px;
    background: rgba(8,12,16,0.85);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(30,45,61,0.6);
}
.nav-logo { font-family: 'Space Mono', monospace; font-size: 13px; color: #00d4ff; letter-spacing: 0.12em; }
.nav-links { display: flex; gap: 32px; }
.nav-links a {
    font-family: 'Space Mono', monospace; font-size: 11px; text-transform: uppercase;
    color: #64748b; text-decoration: none; letter-spacing: 0.1em;
    transition: color 0.2s;
}
.nav-links a:hover { color: #00d4ff; }

/* ---- Section wrapper ---- */
.section { padding: 100px 48px; }
.section-alt { padding: 100px 48px; background: #0d1117; }

/* ---- Section header ---- */
.sec-header { display: flex; align-items: center; gap: 16px; margin-bottom: 56px; }
.sec-num { font-family: 'Space Mono', monospace; font-size: 12px; color: #00d4ff; letter-spacing: 0.1em; }
.sec-title { font-size: 38px; font-weight: 800; letter-spacing: -0.02em; color: #e2e8f0; }
.sec-line { flex: 1; height: 1px; background: #1e2d3d; }

/* ---- Hero ---- */
.hero-wrap {
    min-height: 100vh;
    display: flex; flex-direction: column; justify-content: center;
    padding: 120px 48px 80px;
    position: relative; overflow: hidden;
}
.hero-grid {
    position: absolute; inset: 0;
    background-image: linear-gradient(rgba(0,212,255,0.025) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(0,212,255,0.025) 1px, transparent 1px);
    background-size: 60px 60px;
    mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 30%, transparent 100%);
}
.hero-glow {
    position: absolute; width: 600px; height: 600px; border-radius: 50%;
    background: radial-gradient(circle, rgba(0,212,255,0.07) 0%, transparent 70%);
    top: -100px; right: -100px; pointer-events: none;
    animation: pulse 6s ease-in-out infinite;
}
.hero-glow2 {
    position: absolute; width: 400px; height: 400px; border-radius: 50%;
    background: radial-gradient(circle, rgba(124,58,237,0.05) 0%, transparent 70%);
    bottom: 0; left: 100px; pointer-events: none;
    animation: pulse 8s ease-in-out infinite reverse;
}
@keyframes pulse {
    0%,100% { opacity: 0.5; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.1); }
}
.hero-eyebrow {
    font-family: 'Space Mono', monospace; font-size: 12px; color: #00d4ff;
    letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 24px;
    animation: fadeUp 0.8s ease 0.2s both;
}
.hero-eyebrow span { display:inline-block; width:40px; height:1px; background:#00d4ff; vertical-align:middle; margin-right:12px; }
.hero-name {
    font-size: clamp(48px, 8vw, 110px); font-weight: 800; line-height: 0.95;
    letter-spacing: -0.03em; margin-bottom: 8px;
    animation: fadeUp 0.8s ease 0.4s both;
}
.hero-name .line1 { display: block; color: #e2e8f0; }
.hero-name .line2 {
    display: block;
    background: linear-gradient(135deg, #00d4ff 0%, #7c3aed 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-role {
    font-family: 'Space Mono', monospace; font-size: 15px; color: #64748b;
    margin-top: 24px; margin-bottom: 40px;
    animation: fadeUp 0.8s ease 0.6s both;
}
.hero-role .hl { color: #10b981; }
.hero-stats {
    display: flex; gap: 48px; margin-top: 16px;
    animation: fadeUp 0.8s ease 1s both;
}
.stat { }
.stat-num { font-size: 36px; font-weight: 800; color: #00d4ff; line-height: 1; }
.stat-label { font-family: 'Space Mono', monospace; font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 4px; }
@keyframes fadeUp { from { opacity:0; transform:translateY(30px); } to { opacity:1; transform:translateY(0); } }

/* ---- CTA buttons ---- */
.cta-row { display: flex; gap: 16px; margin-bottom: 48px; animation: fadeUp 0.8s ease 0.8s both; }
.btn-p {
    font-family: 'Space Mono', monospace; font-size: 12px; letter-spacing: 0.08em; font-weight: 700;
    padding: 13px 28px; background: #00d4ff; color: #080c10; border: none; cursor: pointer;
    clip-path: polygon(8px 0%, 100% 0%, calc(100% - 8px) 100%, 0% 100%);
    transition: all 0.2s; text-decoration: none; display: inline-block;
}
.btn-p:hover { background: #fff; transform: translateY(-2px); }
.btn-s {
    font-family: 'Space Mono', monospace; font-size: 12px; letter-spacing: 0.08em;
    padding: 12px 28px; border: 1px solid #1e2d3d; color: #64748b; background: transparent; cursor: pointer;
    clip-path: polygon(8px 0%, 100% 0%, calc(100% - 8px) 100%, 0% 100%);
    transition: all 0.2s; text-decoration: none; display: inline-block;
}
.btn-s:hover { border-color: #00d4ff; color: #00d4ff; transform: translateY(-2px); }

/* ---- Stack grid ---- */
.stack-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2px; }
.stack-item {
    background: #080c10; padding: 28px 20px;
    display: flex; flex-direction: column; align-items: center; gap: 12px;
    border: 1px solid transparent;
    transition: all 0.3s; position: relative; overflow: hidden;
}
.stack-item::before {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 2px;
    background: #00d4ff; transform: scaleX(0); transition: transform 0.3s ease;
}
.stack-item:hover { background: #131920; border-color: #1e2d3d; }
.stack-item:hover::before { transform: scaleX(1); }
.stack-icon { font-size: 32px; line-height: 1; }
.stack-name { font-family: 'Space Mono', monospace; font-size: 11px; color: #64748b; text-align: center; }
.stack-item:hover .stack-name { color: #e2e8f0; }

/* ---- Project cards ---- */
.proj-card {
    background: #0d1117; border: 1px solid #1e2d3d; padding: 48px;
    margin-bottom: 2px; display: grid; grid-template-columns: 1fr 1fr; gap: 48px;
    position: relative; overflow: hidden; transition: border-color 0.3s;
}
.proj-card::before {
    content: ''; position: absolute; top:0; left:0; width:4px; height:100%;
    transform: scaleY(0); transform-origin: top; transition: transform 0.4s;
}
.proj-card:hover { border-color: rgba(0,212,255,0.3); }
.proj-card:hover::before { transform: scaleY(1); }
.proj-card.cyan::before { background: #00d4ff; }
.proj-card.purple::before { background: #7c3aed; }
.proj-card.green::before { background: #10b981; }

.proj-num { font-family: 'Space Mono', monospace; font-size: 11px; color: #334155; letter-spacing: 0.1em; margin-bottom: 14px; }
.proj-title { font-size: 24px; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 6px; color: #e2e8f0; line-height: 1.2; }
.proj-sub { font-family: 'Space Mono', monospace; font-size: 11px; margin-bottom: 22px; letter-spacing: 0.05em; }
.proj-sub.cyan { color: #00d4ff; }
.proj-sub.purple { color: #a78bfa; }
.proj-sub.green { color: #10b981; }
.proj-desc { font-size: 14px; color: #64748b; line-height: 1.75; margin-bottom: 28px; }
.proj-desc strong { color: #94a3b8; }
.proj-metric {
    display: inline-flex; align-items: center; gap: 10px;
    padding: 10px 18px; font-family: 'Space Mono', monospace; font-size: 12px; margin-bottom: 22px;
}
.proj-metric.cyan { background: rgba(0,212,255,0.07); border: 1px solid rgba(0,212,255,0.2); color: #00d4ff; }
.proj-metric.purple { background: rgba(124,58,237,0.07); border: 1px solid rgba(124,58,237,0.2); color: #a78bfa; }
.proj-metric.green { background: rgba(16,185,129,0.07); border: 1px solid rgba(16,185,129,0.2); color: #10b981; }
.metric-dot { width:6px; height:6px; border-radius:50%; background:currentColor; animation: blink 2s infinite; display:inline-block; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
.tag-row { display: flex; flex-wrap: wrap; gap: 8px; }
.tag {
    font-family: 'Space Mono', monospace; font-size: 10px; padding: 5px 12px;
    background: #131920; border: 1px solid #1e2d3d; color: #64748b; letter-spacing: 0.05em;
}

/* ---- Pipeline ---- */
.pipeline { display: flex; flex-direction: column; gap: 4px; }
.pipe-step {
    display: flex; align-items: center; gap: 12px;
    padding: 12px 16px; background: #131920; border: 1px solid #1e2d3d;
    font-family: 'Space Mono', monospace; font-size: 11px; color: #64748b;
    transition: all 0.2s;
}
.pipe-step:hover { border-color: #00d4ff; color: #e2e8f0; }
.pipe-arrow { text-align: center; color: #334155; font-size: 14px; padding: 2px 0; }

/* ---- CNN layers ---- */
.cnn-vis { display: flex; flex-direction: column; gap: 8px; }
.cnn-layers-row { display: flex; gap: 4px; align-items: flex-end; }
.cnn-col { display: flex; flex-direction: column; gap: 2px; flex: 1; align-items: stretch; }
.cnn-blk { border: 1px solid rgba(124,58,237,0.25); transition: background 0.2s; }
.cnn-blk:hover { background: rgba(124,58,237,0.2) !important; }
.cnn-lbl { font-family: 'Space Mono', monospace; font-size: 9px; color: #334155; text-align: center; margin-top: 6px; letter-spacing: 0.05em; }
.cnn-acc {
    text-align: center; font-family: 'Space Mono', monospace; font-size: 11px; color: #64748b;
    padding: 12px; background: #131920; border: 1px solid #1e2d3d; margin-top: 8px;
}
.cnn-acc span { color: #00d4ff; font-weight: 700; font-size: 20px; }

/* ---- Contact ---- */
.contact-link {
    display: flex; align-items: center; gap: 20px;
    padding: 20px 24px; background: #080c10; border: 1px solid #1e2d3d;
    text-decoration: none; color: #e2e8f0; margin-bottom: 2px;
    font-family: 'Space Mono', monospace; font-size: 13px;
    transition: all 0.25s;
}
.contact-link:hover { border-color: #00d4ff; color: #00d4ff; padding-left: 36px; }
.cl-arr { margin-left: auto; opacity:0; transition: opacity 0.2s; }
.contact-link:hover .cl-arr { opacity: 1; }

/* ---- Footer ---- */
.footer {
    padding: 28px 48px; border-top: 1px solid #1e2d3d;
    display: flex; justify-content: space-between;
    font-family: 'Space Mono', monospace; font-size: 11px; color: #334155;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# NAV
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="navbar">
  <div class="nav-logo">// ML.ENGINEER</div>
  <div class="nav-links">
    <a href="#stack">Stack</a>
    <a href="#projects">Projects</a>
    <a href="#contact">Contact</a>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-wrap">
  <div class="hero-grid"></div>
  <div class="hero-glow"></div>
  <div class="hero-glow2"></div>

  <div class="hero-eyebrow"><span></span>Available for opportunities</div>

  <h1 class="hero-name">
    <span class="line1">Machine Learning</span>
    <span class="line2">Engineer</span>
  </h1>

  <div class="hero-role">
    Specialist in <span class="hl">RAG Pipelines</span> &amp; <span class="hl">Deep Learning</span>
    &nbsp;·&nbsp; Python · PyTorch · LangChain
  </div>

  <div class="cta-row">
    <a class="btn-p" href="#projects">View Projects</a>
    <a class="btn-s" href="#contact">Get in Touch</a>
  </div>

  <div class="hero-stats">
    <div class="stat"><div class="stat-num">90%+</div><div class="stat-label">RAG Accuracy</div></div>
    <div class="stat"><div class="stat-num">95%+</div><div class="stat-label">CNN Accuracy</div></div>
    <div class="stat"><div class="stat-num">700K</div><div class="stat-label">Training Samples</div></div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TECH STACK
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="stack" class="section-alt">', unsafe_allow_html=True)
st.markdown("""
<div class="sec-header">
  <span class="sec-num">01</span>
  <h2 class="sec-title">Tech Stack</h2>
  <div class="sec-line"></div>
</div>
""", unsafe_allow_html=True)

stack = [
    ("🐍", "Python"),    ("🔥", "PyTorch"),   ("🧠", "TensorFlow"), ("🦜", "LangChain"),
    ("☁️", "AWS"),       ("🐳", "Docker"),    ("⚡", "CUDA"),       ("🗄️", "SQL"),
    ("🚀", "FastAPI"),   ("🤗", "Hugging Face"), ("📊", "NumPy/Pandas"),
]
cols = st.columns(11)
for col, (icon, name) in zip(cols, stack):
    with col:
        st.markdown(f"""
        <div class="stack-item">
          <div class="stack-icon">{icon}</div>
          <div class="stack-name">{name}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PROJECTS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="projects" class="section">', unsafe_allow_html=True)
st.markdown("""
<div class="sec-header">
  <span class="sec-num">02</span>
  <h2 class="sec-title">Projects</h2>
  <div class="sec-line"></div>
</div>
""", unsafe_allow_html=True)

# ── Project 1: RAG ─────────────────────────────────────────────────────────
st.markdown("""
<div class="proj-card cyan">
  <div>
    <div class="proj-num">PROJECT / 001</div>
    <div class="proj-title">Advanced RAG Pipeline</div>
    <div class="proj-sub cyan">Milli Strategiya Sənədləri üzrə</div>
    <p class="proj-desc">
      <strong>Problem:</strong> Hüquqi sənədlər üzərindən dəqiq faktual cavab almaq çətin idi — standart keyword axtarışı semantik məntiqi qaçırırdı.<br><br>
      <strong>Həll:</strong> İki mərhələli retrieval (BM25 + dense), adaptive chunking strategiyaları və cross-encoder reranking ilə hybrid RAG pipeline.<br><br>
      <strong>Nəticə:</strong> Hüquqi sənədlərdə 90%+ faktual dəqiqlik əldə edildi.
    </p>
    <div class="proj-metric cyan"><span class="metric-dot"></span> 90%+ Factual Accuracy on Legal Documents</div>
    <div class="tag-row">
      <span class="tag">LangChain</span><span class="tag">FAISS</span>
      <span class="tag">Cross-Encoder</span><span class="tag">BM25</span><span class="tag">FastAPI</span>
    </div>
  </div>
  <div>
    <div class="pipeline">
      <div class="pipe-step">📄&nbsp; Document Ingestion</div>
      <div class="pipe-arrow">↓</div>
      <div class="pipe-step">✂️&nbsp; Adaptive Chunking</div>
      <div class="pipe-arrow">↓</div>
      <div class="pipe-step">🔍&nbsp; Hybrid Retrieval (BM25 + Dense)</div>
      <div class="pipe-arrow">↓</div>
      <div class="pipe-step">⚖️&nbsp; Cross-Encoder Reranking</div>
      <div class="pipe-arrow">↓</div>
      <div class="pipe-step">💬&nbsp; LLM Generation</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Project 2: CNN ─────────────────────────────────────────────────────────
st.markdown("""
<div class="proj-card purple">
  <div>
    <div class="proj-num">PROJECT / 002</div>
    <div class="proj-title">Handwritten Character Recognition</div>
    <div class="proj-sub purple">EMNIST Dataset · CNN Architecture</div>
    <p class="proj-desc">
      <strong>Problem:</strong> Sadə modellər oxşar simvolları (l, I, 1) qarışdırır; dərin xüsusiyyət çıxarma lazım idi.<br><br>
      <strong>Həll:</strong> 700K+ nümunə üzərində dərin CNN arxitekturası — BatchNorm, Dropout, data augmentation ilə trenlenib.<br><br>
      <strong>Nəticə:</strong> Mürəkkəb xarakter setlərində 95%+ test dəqiqliyi.
    </p>
    <div class="proj-metric purple"><span class="metric-dot"></span> 95%+ Test Accuracy · 47 Classes</div>
    <div class="tag-row">
      <span class="tag">PyTorch</span><span class="tag">CNN</span>
      <span class="tag">EMNIST</span><span class="tag">CUDA</span><span class="tag">Data Augmentation</span>
    </div>
  </div>
  <div>
    <div class="cnn-vis">
      <div class="cnn-layers-row">
        <div class="cnn-col">
          <div class="cnn-blk" style="height:80px;background:rgba(124,58,237,0.05)"></div>
          <div class="cnn-blk" style="height:80px;background:rgba(124,58,237,0.05)"></div>
          <div class="cnn-lbl">Input<br>28×28</div>
        </div>
        <div class="cnn-col">
          <div class="cnn-blk" style="height:64px;background:rgba(124,58,237,0.1)"></div>
          <div class="cnn-blk" style="height:64px;background:rgba(124,58,237,0.1)"></div>
          <div class="cnn-blk" style="height:64px;background:rgba(124,58,237,0.1)"></div>
          <div class="cnn-lbl">Conv1<br>32f</div>
        </div>
        <div class="cnn-col">
          <div class="cnn-blk" style="height:52px;background:rgba(124,58,237,0.15)"></div>
          <div class="cnn-blk" style="height:52px;background:rgba(124,58,237,0.15)"></div>
          <div class="cnn-blk" style="height:52px;background:rgba(124,58,237,0.15)"></div>
          <div class="cnn-blk" style="height:52px;background:rgba(124,58,237,0.15)"></div>
          <div class="cnn-lbl">Conv2<br>64f</div>
        </div>
        <div class="cnn-col">
          <div class="cnn-blk" style="height:38px;background:rgba(124,58,237,0.22)"></div>
          <div class="cnn-blk" style="height:38px;background:rgba(124,58,237,0.22)"></div>
          <div class="cnn-blk" style="height:38px;background:rgba(124,58,237,0.22)"></div>
          <div class="cnn-lbl">FC<br>512</div>
        </div>
        <div class="cnn-col">
          <div class="cnn-blk" style="height:24px;background:rgba(124,58,237,0.45);border-color:rgba(124,58,237,0.8)"></div>
          <div class="cnn-lbl">Out<br>47cls</div>
        </div>
      </div>
      <div class="cnn-acc">Training set: 700K+ samples &nbsp;·&nbsp; Accuracy: <span>95.4%</span></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Project 3: RNN/LSTM ────────────────────────────────────────────────────
left, right = st.columns([1, 1])

with left:
    st.markdown("""
    <div style="background:#0d1117;border:1px solid #1e2d3d;padding:48px 48px 48px 52px;border-left:4px solid #10b981;margin-bottom:2px;">
      <div class="proj-num">PROJECT / 003</div>
      <div class="proj-title">Sentiment Analysis App</div>
      <div class="proj-sub green">RNN vs LSTM · Comparative Study</div>
      <p class="proj-desc">
        <strong>Problem:</strong> Hansı arxitektura sentiment tapşırıqları üçün daha optimaldır — sürət vs dəqiqlik.<br><br>
        <strong>Həll:</strong> Veb interfeys vasitəsilə canlı olaraq RNN və LSTM modelini eyni mətndə müqayisə edən interaktiv tətbiq.<br><br>
        <strong>Nəticə:</strong> LSTM mürəkkəb cümlələrdə RNN-dən 17% daha dəqiq, lakin 1.4× daha yavaş.
      </p>
      <div class="proj-metric green"><span class="metric-dot"></span> LSTM: 91% · RNN: 74% Accuracy</div>
      <div class="tag-row">
        <span class="tag">PyTorch</span><span class="tag">RNN</span>
        <span class="tag">LSTM</span><span class="tag">Streamlit</span><span class="tag">NLP</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    # Plotly bar chart
    fig = go.Figure()
    models = ["RNN", "LSTM"]
    acc_values = [74, 91]
    speed_values = [88, 63]

    # 1. Accuracy Bar
    fig.add_trace(go.Bar(
        name="Accuracy %",
        x=models, 
        y=acc_values,
        marker_color=["rgba(124,58,237,0.6)", "rgba(16,185,129,0.6)"],
        marker_line_color=["#a78bfa", "#10b981"],
        marker_line_width=1,
        text=[f"{val}%" for val in acc_values],
        textposition="inside",
        textfont=dict(family="Space Mono", size=13, color="white"),
    ))

    # 2. Speed Bar
    fig.add_trace(go.Bar(
        name="Speed Score",
        x=models, 
        y=speed_values,
        marker_color=["rgba(124,58,237,0.25)", "rgba(16,185,129,0.25)"],
        marker_line_color=["#a78bfa", "#10b981"],
        marker_line_width=1,
        text=[f"{val}" for val in speed_values],
        textposition="inside",
        textfont=dict(family="Space Mono", size=13, color="white"),
    ))

    fig.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(13,17,23,1)",
        font=dict(family="Space Mono", color="#64748b"),
        legend=dict(
            font=dict(size=11, color="#64748b"),
            bgcolor="rgba(0,0,0,0)",
            bordercolor="#1e2d3d", borderwidth=1,
        ),
        xaxis=dict(
            showgrid=False, zeroline=False,
            tickfont=dict(size=12, color="#94a3b8"),
        ),
        yaxis=dict(
            showgrid=True, gridcolor="#1e2d3d", zeroline=False,
            tickfont=dict(size=11, color="#64748b"),
            range=[0, 105],
        ),
        margin=dict(l=0, r=0, t=20, b=0),
        height=320,
        bargap=0.25,
        bargroupgap=0.08,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CONTACT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="contact" class="section">', unsafe_allow_html=True)
st.markdown("""
<div class="sec-header">
  <span class="sec-num">03</span>
  <h2 class="sec-title">Contact</h2>
  <div class="sec-line"></div>
</div>

<p style="font-size:17px;color:#64748b;line-height:1.75;max-width:560px;margin-bottom:40px;">
  Open to ML engineering roles, research collaborations, and freelance projects. 
  Feel free to reach out through any of the channels below.
</p>

<div>
  <a class="contact-link" href="https://github.com/rafiveyisov" target="_blank">
    ⌨️&nbsp; github.com/rafiveyisov <span class="cl-arr">→</span>
  </a>
  <a class="contact-link" href="https://linkedin.com/in/rafi-veyisov" target="_blank">
    💼&nbsp; linkedin.com/in/rafi-veyisov <span class="cl-arr">→</span>
  </a>
  <a class="contact-link" href="mailto:rfiveyisov@email.com">
    ✉️&nbsp; rfiveyisov@email.com <span class="cl-arr">→</span>
  </a>
</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
  <div>Designed &amp; Built by ML Engineer · 2025</div>
  <div>Python · PyTorch · LangChain · Streamlit</div>
</div>
""", unsafe_allow_html=True)