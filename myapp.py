import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ski Resorts EDA",
    page_icon="⛷️",
    layout="wide",
)

# ── Simple CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

[data-testid="metric-container"] {
    background: #1a2744;
    border: 1px solid #2d3f6b;
    border-radius: 10px;
    padding: 14px 18px;
}
[data-testid="metric-container"] label          { color: #8ba3d4 !important; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.06em; }
[data-testid="stMetricValue"]                   { color: #1e293b; font-size: 1.55rem; font-weight: 700; }
[data-testid="stSidebar"]                       { background: #f0f4f8; }
</style>
""", unsafe_allow_html=True)

# ── Plotly theme helper ───────────────────────────────────────────────────────
COLORS   = px.colors.qualitative.Bold
BG       = "#0e1829"
GRID     = "#1e2d4a"
FONT_CLR = "#334155"

def dark_layout(fig, title=""):
    fig.update_layout(
        title=title,
        paper_bgcolor="#f0f4f8",
        plot_bgcolor="#d0dce8",
        font=dict(family="Inter", color=FONT_CLR),
        title_font=dict(size=15, color="#c8d8f8"),
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor=GRID, showline=False, zeroline=False)
    fig.update_yaxes(gridcolor=GRID, showline=False, zeroline=False)
    return fig

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    df = pd.read_csv("./Data/resorts_clean.csv")

    # Normalise yes/no columns
    yes_no_cols = ["Child friendly", "Snowparks", "Nightskiing", "Summer skiing"]
    for col in yes_no_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower().map(
                {"yes": True, "1": True, "true": True,
                 "no": False, "0": False, "false": False}
            )
    return df

df = load()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⛷️ Filters")
    st.markdown("---")
    continents = ["All"] + sorted(df["Continent"].dropna().unique().tolist())
    sel_cont   = st.selectbox("Continent", continents)

    fdf = df if sel_cont == "All" else df[df["Continent"] == sel_cont]

    st.markdown("---")
    st.caption(f"{len(fdf)} resorts selected")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# ⛷️ Ski Resorts — EDA Dashboard")
st.caption("Exploratory data analysis across ski resorts worldwide")
st.markdown("---")

# ── KPI row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Resorts",     len(fdf))
k2.metric("Countries",         fdf["Country"].nunique())
k3.metric("Avg Price (€)",     f"{fdf['Price'].mean():.0f}")
k4.metric("Avg Total Slopes",  f"{fdf['Total slopes'].mean():.0f}")
k5.metric("Summer Skiing",     f"{fdf['Summer skiing'].sum()} resorts")

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# 1. Which continent has the most beginner-friendly resorts?
# ═════════════════════════════════════════════════════════════════════════════
st.subheader("🌍 Beginner-Friendly Resorts by Continent")
st.caption("Resorts with more beginner slopes than intermediate or difficult.")

beg = fdf.copy()
beg["Beginner dominant"] = beg["Beginner slopes"] >= beg[["Intermediate slopes", "Difficult slopes"]].max(axis=1)
beg_count = beg[beg["Beginner dominant"]].groupby("Continent").size().reset_index(name="Count").sort_values("Count", ascending=True)

fig1 = px.bar(beg_count, x="Count", y="Continent", orientation="h",
              color="Count", color_continuous_scale="Blues", text="Count")
fig1.update_traces(textposition="inside", insidetextanchor="middle")
fig1.update_coloraxes(showscale=False)
dark_layout(fig1)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# 2. Price vs Total Slopes correlation
# ═════════════════════════════════════════════════════════════════════════════
st.subheader("💶 Price vs Total Slopes")
st.caption("Does paying more get you more slopes? Each dot is a resort.")

fig2 = px.scatter(
    fdf.dropna(subset=["Price", "Total slopes"]),
    x="Price", y="Total slopes",
    color="Continent", hover_name="Resort",
    hover_data=["Country", "Price", "Total slopes"],
    color_discrete_sequence=COLORS,
    trendline="ols",
)
dark_layout(fig2)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# 3. Heatmap — resorts by country
# ═════════════════════════════════════════════════════════════════════════════
st.subheader("🗺️ Resort Count by Country")
st.caption("Choropleth map — darker = more resorts.")

country_count = fdf.groupby("Country").size().reset_index(name="Resorts")
fig3 = px.choropleth(
    country_count, locations="Country",
    locationmode="country names",
    color="Resorts",
    color_continuous_scale="Blues",
    hover_name="Country",
)
fig3.update_geos(showframe=False, showcoastlines=True,
                 bgcolor=BG, landcolor="#1a2744", oceancolor="#ADD8E6",
                 coastlinecolor="#8ba3d4")
dark_layout(fig3)
fig3.update_layout(geo=dict(bgcolor="#8ba3d4"), height=420)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# 4. Best resorts for each skill level
# ═════════════════════════════════════════════════════════════════════════════
st.subheader("🏆 Top 10 Resorts by Skill Level")

skill = st.radio("Select skill level", ["Beginner", "Intermediate", "Expert"], horizontal=True)

col_map = {"Beginner": "Beginner slopes", "Intermediate": "Intermediate slopes", "Expert": "Difficult slopes"}
col     = col_map[skill]

top10 = fdf[["Resort", "Country", col]].dropna().sort_values(col, ascending=False).head(10)
top10 = top10.sort_values(col, ascending=True)   # ascending for horizontal bar

fig4 = px.bar(top10, x=col, y="Resort", orientation="h",
              color=col, color_continuous_scale="Blues",
              text=col, hover_data=["Country"])
fig4.update_traces(textposition="outside")
fig4.update_coloraxes(showscale=False)
dark_layout(fig4)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# 5. Summer skiing — where and how rare?
# ═════════════════════════════════════════════════════════════════════════════
st.subheader("☀️ Summer Skiing — How Rare Is It?")

c1, c2 = st.columns([1, 2])

with c1:
    total      = len(fdf)
    summer_yes = int(fdf["Summer skiing"].sum())
    summer_no  = total - summer_yes

    fig5a = go.Figure(go.Pie(
        labels=["Summer skiing", "No summer skiing"],
        values=[summer_yes, summer_no],
        hole=0.55,
        marker_colors=["#4a9eff", "#1a2744"],
        textinfo="label+percent",
    ))
    dark_layout(fig5a)
    fig5a.update_layout(showlegend=False, height=300)
    st.plotly_chart(fig5a, use_container_width=True)

with c2:
    summer_by_country = (
        fdf[fdf["Summer skiing"] == True]
        .groupby("Country").size()
        .reset_index(name="Resorts with Summer Skiing")
        .sort_values("Resorts with Summer Skiing", ascending=False)
        .head(10)
    )
    fig5b = px.bar(summer_by_country, x="Country", y="Resorts with Summer Skiing",
                   color="Resorts with Summer Skiing", color_continuous_scale="Blues",
                   text="Resorts with Summer Skiing")
    fig5b.update_traces(textposition="outside")
    fig5b.update_coloraxes(showscale=False)
    dark_layout(fig5b)
    st.plotly_chart(fig5b, use_container_width=True)

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# 6. Snowparks + Nightskiing availability by country
# ═════════════════════════════════════════════════════════════════════════════
st.subheader("🎿 Snowparks & Night Skiing by Country")
st.caption("Top 15 countries — stacked bars show how many resorts offer each amenity.")

amenity_df = (
    fdf.groupby("Country")[["Snowparks", "Nightskiing"]]
    .sum()
    .reset_index()
)
amenity_df.columns = ["Country", "Snowparks", "Nightskiing"]
amenity_df["Total"] = amenity_df["Snowparks"] + amenity_df["Nightskiing"]
amenity_df = amenity_df.sort_values("Total", ascending=False).head(15)

fig6 = go.Figure()
fig6.add_trace(go.Bar(name="Snowparks",  x=amenity_df["Country"], y=amenity_df["Snowparks"],  marker_color="#4a9eff"))
fig6.add_trace(go.Bar(name="Nightskiing", x=amenity_df["Country"], y=amenity_df["Nightskiing"], marker_color="#a78bfa"))
fig6.update_layout(barmode="stack")
dark_layout(fig6)
st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# ── Raw data toggle ───────────────────────────────────────────────────────────
with st.expander("📋 View raw data"):
    st.dataframe(fdf, use_container_width=True)