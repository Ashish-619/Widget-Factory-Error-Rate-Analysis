import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Widget Factory · Error Rate Analysis",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS — pure white theme ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

  html, body,
  [class*="css"],
  .stApp,
  .main,
  section[data-testid="stSidebar"],
  div[data-testid="stAppViewContainer"],
  div[data-testid="stHeader"],
  div[data-testid="block-container"] {
      background-color: #FFFFFF !important;
      font-family: 'Inter', sans-serif !important;
      color: #1a1a2e !important;
  }

  .hero {
      background: linear-gradient(135deg, #f0f4ff 0%, #e8f0fe 100%);
      border: 1px solid #d0dcf8;
      border-radius: 16px;
      padding: 2.4rem 3rem;
      margin-bottom: 2rem;
  }
  .hero-badge {
      display: inline-block;
      background: #2563eb;
      color: #fff;
      font-size: 0.68rem;
      font-weight: 600;
      letter-spacing: 1.8px;
      text-transform: uppercase;
      padding: 4px 12px;
      border-radius: 20px;
      margin-bottom: 1rem;
  }
  .hero h1 {
      font-family: 'Playfair Display', serif;
      font-size: 2.4rem;
      color: #1a1a2e;
      margin: 0 0 0.5rem;
      line-height: 1.2;
  }
  .hero p { color: #4a5568; font-size: 0.97rem; margin: 0; font-weight: 400; line-height: 1.6; }

  .kpi-row { display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap; }
  .kpi-card {
      flex: 1; min-width: 150px;
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 1.2rem 1.4rem;
      box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  }
  .kpi-card .klabel { font-size: 0.68rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 6px; font-weight: 600; }
  .kpi-card .kval   { font-size: 1.9rem; font-weight: 700; line-height: 1; }
  .kpi-card .ksub   { font-size: 0.72rem; color: #94a3b8; margin-top: 5px; }
  .c-blue  { color: #2563eb; }
  .c-red   { color: #dc2626; }
  .c-amber { color: #d97706; }
  .c-green { color: #16a34a; }

  .sec-wrap { margin: 2.5rem 0 1rem; }
  .sec-num {
      display: inline-block; background: #2563eb; color: #fff;
      font-size: 0.7rem; font-weight: 700; padding: 2px 9px;
      border-radius: 20px; margin-bottom: 6px; letter-spacing: 0.5px;
  }
  .sec-title { font-family: 'Playfair Display', serif; font-size: 1.35rem; color: #1a1a2e; margin: 0 0 4px; }
  .sec-sub   { color: #64748b; font-size: 0.84rem; margin: 0; }
  .hdivider  { border: none; border-top: 1px solid #e2e8f0; margin: 0.5rem 0 1.5rem; }

  .callout { border-radius: 10px; padding: 1rem 1.25rem; margin: 1rem 0; font-size: 0.88rem; line-height: 1.65; color: #1e293b; }
  .callout strong { font-weight: 600; }
  .callout.info   { background: #eff6ff; border-left: 4px solid #2563eb; }
  .callout.warn   { background: #fffbeb; border-left: 4px solid #d97706; }
  .callout.good   { background: #f0fdf4; border-left: 4px solid #16a34a; }
  .callout.alert  { background: #fef2f2; border-left: 4px solid #dc2626; }
  .callout.purple { background: #faf5ff; border-left: 4px solid #7c3aed; }

  .verdict {
      background: #f0fdf4; border: 1px solid #bbf7d0;
      border-radius: 14px; padding: 1.8rem 2rem; margin-top: 1.5rem;
  }
  .verdict h3 { font-family: 'Playfair Display', serif; font-size: 1.2rem; color: #15803d; margin: 0 0 1rem; }
  .verdict ul { margin: 0; padding-left: 1.2rem; color: #1e293b; line-height: 2.1; }
  .verdict li strong { color: #15803d; }

  .mgr-row { display: flex; gap: 1rem; margin-top: 1.5rem; }
  .mgr-card { flex: 1; background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.2rem 1.4rem; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
  .mgr-card .mtop  { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
  .mgr-card .mname { font-family: 'Playfair Display', serif; font-size: 1.15rem; margin: 0 0 6px; color: #1a1a2e; }
  .mgr-card p      { font-size: 0.85rem; color: #4a5568; margin: 0; line-height: 1.6; }

  .footer { text-align: center; color: #000; font-size: 1rem; margin-top: 3rem; padding: 1.5rem 0; border-top: 1px solid #e2e8f0; }

  div[data-testid="stVerticalBlock"],
  div[data-testid="stHorizontalBlock"],
  div[data-testid="column"] { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ── Chart helpers ─────────────────────────────────────────────────────────────
MANAGER_COLORS = {"Al": "#dc2626", "Bob": "#2563eb", "Carl": "#d97706"}
WHITE = "#ffffff"
GRID  = "#f1f5f9"
AXIS  = "#64748b"
TITLE = "#1a1a2e"

CHART_BASE = dict(
    paper_bgcolor=WHITE, plot_bgcolor=WHITE,
    font=dict(family="Inter, sans-serif", color=AXIS, size=12),
    margin=dict(l=40, r=20, t=45, b=40),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11, color=TITLE)),
    title_font=dict(size=14, color=TITLE, family="Inter, sans-serif"),
)

def clean_axes(fig, y_range=None):
    yax = dict(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color=AXIS))
    if y_range:
        yax["range"] = y_range
    fig.update_xaxes(showgrid=False, tickfont=dict(color=AXIS))
    fig.update_yaxes(**yax)

# ── Data ──────────────────────────────────────────────────────────────────────
data = {
    "Manager": ["Al", "Bob", "Carl"],
    "US_Pass": [394, 140, 246], "US_Fail": [24, 5, 12],
    "OV_Pass": [50, 846, 201],  "OV_Fail": [6, 80, 20],
}
df = pd.DataFrame(data)
df["US_Total"]        = df["US_Pass"] + df["US_Fail"]
df["OV_Total"]        = df["OV_Pass"] + df["OV_Fail"]
df["Total"]           = df["US_Total"] + df["OV_Total"]
df["Total_Fail"]      = df["US_Fail"]  + df["OV_Fail"]
df["US_Err_Pct"]      = (df["US_Fail"]    / df["US_Total"] * 100).round(2)
df["OV_Err_Pct"]      = (df["OV_Fail"]    / df["OV_Total"] * 100).round(2)
df["Overall_Err_Pct"] = (df["Total_Fail"] / df["Total"]    * 100).round(2)
df["OV_Mix_Pct"]      = (df["OV_Total"]   / df["Total"]    * 100).round(1)
df["Std_Err_Pct"]     = ((df["US_Err_Pct"] * 0.5) + (df["OV_Err_Pct"] * 0.5)).round(2)

avg_us  = round(df["US_Fail"].sum() / df["US_Total"].sum() * 100, 2)
avg_ov  = round(df["OV_Fail"].sum() / df["OV_Total"].sum() * 100, 2)
premium = round(avg_ov - avg_us, 2)

# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <h1>Widget Factory — Error Rate Audit</h1>
  <p>A data-driven investigation into shift performance, job mix bias, and a classic statistical paradox —
  prepared for Manufacturing Director Don.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="kpi-row">
  <div class="kpi-card">
    <div class="klabel">Total jobs audited</div>
    <div class="kval c-blue">2,024</div>
    <div class="ksub">All 3 shifts · 1 month</div>
  </div>
  <div class="kpi-card">
    <div class="klabel">Al · overall error rate</div>
    <div class="kval c-red">6.33%</div>
    <div class="ksub">30 errors / 474 jobs</div>
  </div>
  <div class="kpi-card">
    <div class="klabel">Bob · overall error rate</div>
    <div class="kval c-amber">7.94%</div>
    <div class="ksub">85 errors / 1,071 jobs</div>
  </div>
  <div class="kpi-card">
    <div class="klabel">Carl · overall error rate</div>
    <div class="kval c-amber">6.68%</div>
    <div class="ksub">32 errors / 479 jobs</div>
  </div>
  <div class="kpi-card">
    <div class="klabel">Overseas error premium</div>
    <div class="kval c-red">+4.9 pp</div>
    <div class="ksub">vs US jobs (all managers)</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-wrap">
  <div class="sec-num">01</div>
  <p class="sec-title">Error Rates by Job Type</p>
  <p class="sec-sub">The only fair comparison — each manager evaluated on the same category of work.</p>
</div><hr class="hdivider">
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    fig = go.Figure()
    for m in df["Manager"]:
        r = df[df["Manager"]==m].iloc[0]
        fig.add_trace(go.Bar(
            name=m, x=["US Jobs","Overseas Jobs"],
            y=[r["US_Err_Pct"], r["OV_Err_Pct"]],
            marker_color=MANAGER_COLORS[m], marker_line=dict(width=0),
            text=[f"{r['US_Err_Pct']}%", f"{r['OV_Err_Pct']}%"],
            textposition="outside", textfont=dict(size=11, color=TITLE),
        ))
    fig.update_layout(**CHART_BASE, title="Error % by Job Type & Manager", barmode="group", height=370)
    clean_axes(fig, [0,14]); fig.update_yaxes(title_text="Error rate (%)")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    cats = ["US Error %","Overseas Error %","Overall Error %","Std. Error %"]
    fill_c = {"Al":"rgba(220,38,38,0.08)","Bob":"rgba(37,99,235,0.08)","Carl":"rgba(217,119,6,0.08)"}
    fig2 = go.Figure()
    for m in df["Manager"]:
        r = df[df["Manager"]==m].iloc[0]
        vals = [r["US_Err_Pct"],r["OV_Err_Pct"],r["Overall_Err_Pct"],r["Std_Err_Pct"]]
        fig2.add_trace(go.Scatterpolar(
            r=vals+[vals[0]], theta=cats+[cats[0]], fill="toself", name=m,
            line=dict(color=MANAGER_COLORS[m], width=2), fillcolor=fill_c[m],
        ))
    fig2.update_layout(
        **CHART_BASE, title="Performance Radar (lower = better)", height=370,
        polar=dict(
            bgcolor=WHITE,
            radialaxis=dict(visible=True, range=[0,12], gridcolor="#e2e8f0", color=AXIS, tickfont=dict(color=AXIS)),
            angularaxis=dict(gridcolor="#e2e8f0", color=AXIS, tickfont=dict(color=TITLE)),
        ),
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("""<div class="callout alert">
  <strong>Key finding:</strong> Bob beats Al in <em>both</em> US jobs (3.45% vs 5.74%) and overseas jobs (8.64% vs 10.71%).
  Al claims the lowest error rate — but only because he handles very few overseas jobs, which are harder for everyone.
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-wrap">
  <div class="sec-num">02</div>
  <p class="sec-title">The Statistical Illusion — Simpson's Paradox</p>
  <p class="sec-sub">Why the overall error rate gives the wrong answer entirely.</p>
</div><hr class="hdivider">
""", unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(name="US Jobs", x=df["Manager"], y=df["US_Total"],
        marker_color="#3b82f6", marker_line=dict(width=0),
        text=df["US_Total"], textposition="inside", textfont=dict(color="white",size=11)))
    fig3.add_trace(go.Bar(name="Overseas Jobs", x=df["Manager"], y=df["OV_Total"],
        marker_color="#a78bfa", marker_line=dict(width=0),
        text=df["OV_Total"], textposition="inside", textfont=dict(color="white",size=11)))
    fig3.update_layout(**CHART_BASE, title="Volume & Job Mix per Manager", barmode="stack", height=350)
    clean_axes(fig3); fig3.update_yaxes(title_text="Number of jobs")
    st.plotly_chart(fig3, use_container_width=True)

    with col4:
        fig4 = go.Figure(go.Bar(
            x=df["Manager"], y=df["OV_Mix_Pct"],
            marker_color=[MANAGER_COLORS[m] for m in df["Manager"]], marker_line=dict(width=0),
            text=[f"{v}%" for v in df["OV_Mix_Pct"]], textposition="outside",
            textfont=dict(size=12,color=TITLE),
        ))
        fig4.update_layout(**CHART_BASE, title="Overseas job share per manager", showlegend=False, height=350)
        clean_axes(fig4,[0,100]); fig4.update_yaxes(title_text="Overseas share (%)")
        st.plotly_chart(fig4, use_container_width=True)

st.markdown("""<div class="callout purple">
      <strong style="color:#7c3aed;font-size:1rem;">⚠ Simpson's Paradox</strong><br>
      A statistical phenomenon where a trend in grouped data <strong>completely reverses</strong>
      when split into subgroups. <br>
      Al's overall rate (6.33%) <em>looks</em> better than Bob's (7.94%) — yet Bob outperforms Al
      on every single job type. <br>
      The reason: <strong>job mix bias</strong>. Bob handles 86.5% overseas jobs (harder);
      Al handles only 11.8% (easier). The overall rate confuses skill with job difficulty.
    </div>""", unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-wrap">
  <div class="sec-num">03</div>
  <p class="sec-title">Standardised Error Rate</p>
  <p class="sec-sub">Apply a 50/50 US/Overseas job mix to every manager, then compare fairly.</p>
</div><hr class="hdivider">
""", unsafe_allow_html=True)

col5, col6 = st.columns(2)
with col5:
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(name="Raw overall rate", x=df["Manager"], y=df["Overall_Err_Pct"],
        marker_color="#93c5fd", marker_line=dict(width=0), opacity=0.8,
        text=[f"{v}%" for v in df["Overall_Err_Pct"]], textposition="outside",
        textfont=dict(color=AXIS,size=11)))
    fig5.add_trace(go.Bar(name="Standardised rate (50/50)", x=df["Manager"], y=df["Std_Err_Pct"],
        marker_color=[MANAGER_COLORS[m] for m in df["Manager"]], marker_line=dict(width=0),
        text=[f"{v}%" for v in df["Std_Err_Pct"]], textposition="outside",
        textfont=dict(color=TITLE,size=11)))
    fig5.update_layout(**CHART_BASE, title="Raw vs Standardised Error Rate", barmode="group", height=370)
    clean_axes(fig5,[0,11]); fig5.update_yaxes(title_text="Error rate (%)")
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    fig6 = go.Figure(go.Waterfall(
        orientation="v",
        x=["Al — raw rank #1","Bias correction","Al — true rank #3"],
        y=[6.33, 1.90, 0], measure=["absolute","relative","total"],
        text=["6.33%","+1.90 pp","8.23%"], textposition="outside",
        textfont=dict(color=TITLE,size=12),
        connector=dict(line=dict(color="#e2e8f0",width=1.5)),
        increasing=dict(marker=dict(color="#fca5a5",line=dict(width=0))),
        decreasing=dict(marker=dict(color="#86efac",line=dict(width=0))),
        totals=dict(marker=dict(color="#dc2626",line=dict(width=0))),
    ))
    fig6.update_layout(**CHART_BASE, title="Al's misleading advantage — unwound", showlegend=False, height=370)
    clean_axes(fig6,[0,11]); fig6.update_yaxes(title_text="Error rate (%)")
    st.plotly_chart(fig6, use_container_width=True)

tbl = df[["Manager","US_Err_Pct","OV_Err_Pct","Overall_Err_Pct","Std_Err_Pct","Total","OV_Mix_Pct"]].copy()
tbl.columns = ["Manager","US Error %","Overseas Error %","Raw Overall %","Standardised %","Total Jobs","Overseas Mix %"]
st.dataframe(
    tbl.style
        .highlight_min(subset=["US Error %","Overseas Error %","Raw Overall %","Standardised %"], color="#dcfce7")
        .highlight_max(subset=["US Error %","Overseas Error %","Raw Overall %","Standardised %"], color="#fee2e2")
        .format({"US Error %":"{:.2f}%","Overseas Error %":"{:.2f}%",
                 "Raw Overall %":"{:.2f}%","Standardised %":"{:.2f}%","Overseas Mix %":"{:.1f}%"}),
    use_container_width=True, hide_index=True,
)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-wrap">
  <div class="sec-num">04</div>
  <p class="sec-title">Volume & Capacity Analysis</p>
  <p class="sec-sub">Who is actually carrying the factory's workload?</p>
</div><hr class="hdivider">
""", unsafe_allow_html=True)

col7, col8 = st.columns(2)
with col7:
    treemap_data = []
    for _, r in df.iterrows():
        treemap_data.append({"Manager":r["Manager"],"Job Type":"US Jobs","Count":r["US_Total"]})
        treemap_data.append({"Manager":r["Manager"],"Job Type":"Overseas Jobs","Count":r["OV_Total"]})
    tf = pd.DataFrame(treemap_data)
    fig7 = px.treemap(tf, path=["Manager","Job Type"], values="Count",
        color="Manager", color_discrete_map=MANAGER_COLORS, title="Job volume distribution")
    fig7.update_layout(**CHART_BASE, height=330)
    fig7.update_traces(textfont=dict(size=13,color="white"))
    st.plotly_chart(fig7, use_container_width=True)

with col8:
    fig8 = make_subplots(rows=1,cols=3,specs=[[{"type":"pie"}]*3],subplot_titles=["Al","Bob","Carl"])
    for i, m in enumerate(df["Manager"]):
        r = df[df["Manager"]==m].iloc[0]
        fig8.add_trace(go.Pie(
            labels=["Pass","Fail"],
            values=[r["Total"]-r["Total_Fail"], r["Total_Fail"]],
            marker=dict(colors=["#22c55e","#ef4444"],line=dict(color="white",width=2)),
            hole=0.58, textinfo="percent", showlegend=(i==0), name=m,
        ), row=1, col=i+1)
    fig8.update_layout(**CHART_BASE, title="Pass / Fail split per manager", height=310)
    st.plotly_chart(fig8, use_container_width=True)

st.markdown("""<div class="callout good">
  <strong>Bob carries 52.9% of total factory volume</strong> — more than Al and Carl combined —
  while maintaining the best error rates in every job category.
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="sec-wrap">
  <div class="sec-num">05</div>
  <p class="sec-title">System Issue — The Overseas Error Premium</p>
  <p class="sec-sub">The biggest problem in this factory isn't any manager — it's the overseas production process itself.</p>
</div><hr class="hdivider">
""", unsafe_allow_html=True)

fig9 = go.Figure()
fig9.add_trace(go.Bar(
    x=["US Jobs (avg)","Overseas Jobs (avg)"], y=[avg_us, avg_ov],
    marker_color=["#3b82f6","#ef4444"], marker_line=dict(width=0),
    text=[f"{avg_us:.2f}%",f"{avg_ov:.2f}%"], textposition="outside",
    textfont=dict(size=15,color=TITLE), width=[0.35,0.35],
))
fig9.add_annotation(
    x=0.5, y=(avg_us+avg_ov)/2, xref="paper", yref="y",
    text=f"<b>+{premium:.2f} pp gap</b><br>for overseas jobs",
    showarrow=False, font=dict(color="#d97706",size=12,family="Inter"),
    bgcolor="#fffbeb", bordercolor="#fcd34d", borderwidth=1, borderpad=8,
)
fig9.update_layout(**CHART_BASE, title="Factory-wide average error rate: US vs Overseas", showlegend=False, height=340)
clean_axes(fig9,[0,12]); fig9.update_yaxes(title_text="Error rate (%)")
st.plotly_chart(fig9, use_container_width=True)

st.markdown(f"""<div class="callout warn">
  <strong>Overseas jobs carry a {premium:.2f} percentage-point error premium factory-wide</strong> — consistent across
  all three managers. This is a systemic process signal, not a people problem.
  Possible root causes: more complex specs, different materials, tooling gaps, or insufficient training.
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — Verdict
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-wrap">
  <div class="sec-num">06</div>
  <p class="sec-title">Findings & Recommendations</p>
  <p class="sec-sub">What Don should do — backed by the data.</p>
</div><hr class="hdivider">
""", unsafe_allow_html=True)

st.markdown("""
<div class="verdict">
  <h3>✔ Our Recommendation to Don</h3>
  <ul>
    <li><strong>Do not fire Bob.</strong> Bob is the factory's best manager when evaluated fairly — he beats Al and Carl on both US and overseas jobs and handles more than half the total workload.</li>
    <li><strong>Al's claim is statistically deceptive.</strong> Al's lower overall rate is entirely explained by avoiding overseas jobs. On a like-for-like basis, Al has the worst error rate of the three.</li>
    <li><strong>Stop using raw overall error rate for HR decisions.</strong> It is confounded by job mix. Always compare within job type or use standardised rates.</li>
    <li><strong>Investigate the overseas error premium (~5 pp higher for everyone).</strong> Fixing this root cause could halve total factory errors — far more impactful than any personnel change.</li>
    <li><strong>Rebalance job assignments.</strong> Bob is over-indexed on overseas work. Distributing overseas jobs more evenly would be fairer and create comparable performance baselines.</li>
  </ul>
</div>
<div class="mgr-row">
  <div class="mgr-card" style="border-top:3px solid #dc2626;">
    <div class="mtop" style="color:#dc2626;">Al</div>
    <div class="mname">Misleading claim</div>
    <p>Best raw rate is an artefact of easy job allocation. True standardised rate: <strong>8.23%</strong> — worst of the three.</p>
  </div>
  <div class="mgr-card" style="border-top:3px solid #16a34a;">
    <div class="mtop" style="color:#16a34a;">Bob</div>
    <div class="mname">Top performer</div>
    <p>Lowest error rate in both categories. Carries 53% of volume. Standardised rate: <strong>6.05%</strong> — best of the three.</p>
  </div>
  <div class="mgr-card" style="border-top:3px solid #d97706;">
    <div class="mtop" style="color:#d97706;">Carl</div>
    <div class="mname">Solid & balanced</div>
    <p>Middle performer across all metrics. Standardised rate: <strong>6.85%</strong>. Most evenly distributed job mix.</p>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
  Widget Factory Error Rate Audit &nbsp;·&nbsp;
  Analysis done by Ashish Vaidya
</div>
""", unsafe_allow_html=True)