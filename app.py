import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("kpop_data.csv")

def get_generation(year):
    if year <= 2003:
        return "1st Gen"
    elif year <= 2011:
        return "2nd Gen"
    elif year <= 2017:
        return "3rd Gen"
    elif year <= 2021:
        return "4th Gen"
    else:
        return "5th Gen"

df["generation"] = df["debut_year"].apply(get_generation)

df_filtered = df.copy()
df_filtered["secondary_market_clean"] = df_filtered["secondary_market"].fillna("")

st.sidebar.header("Filter Options")

# 公司多选
selected_companies = st.sidebar.multiselect(
    "Select Company",
    options=sorted(df["company"].unique().tolist()),
    default=sorted(df["company"].unique().tolist())
)

# 主市场多选
selected_markets = st.sidebar.multiselect(
    "Select Main Market",
    options=sorted(df["main_market"].unique().tolist()),
    default=sorted(df["main_market"].unique().tolist())
)

# Secondary Market 多选
selected_secondary = st.sidebar.multiselect(
    "Select Secondary Market",
    options=sorted(df["secondary_market"].dropna().unique().tolist()),
    default=sorted(df["secondary_market"].dropna().unique().tolist())
)

# 类型多选
selected_types = st.sidebar.multiselect(
    "Select Artist Type",
    options=sorted(df["artist_type"].unique().tolist()),
    default=sorted(df["artist_type"].unique().tolist())
)

# 应用筛选
df_filtered = df_filtered[
    (df_filtered["company"].isin(selected_companies)) &
    (df_filtered["main_market"].isin(selected_markets)) &
    (df_filtered["secondary_market_clean"].isin(selected_secondary)) &
    (df_filtered["artist_type"].isin(selected_types))
]


if df_filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

st.title("K-pop Market Expansion Analysis")

st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Groups", len(df_filtered))
col2.metric("Main Markets", df_filtered["main_market"].nunique())
col3.metric("Secondary Markets", df_filtered["secondary_market"].nunique())

st.caption(f"Showing {len(df_filtered)} records")

st.subheader("Market Shift by Generation")

gen_market = df.groupby(["generation", "main_market"]).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(7, 4))
gen_market.plot(kind="bar", stacked=True, ax=ax)

ax.set_xlabel("Generation")
ax.set_ylabel("Number of Groups")
ax.set_title("Market Focus Shift Across Generations")

st.pyplot(fig)

st.markdown("### 🔍 Key Insight")
st.write("""
Newer generations show a stronger tendency to target global markets, while earlier generations remained more concentrated in Korea and Japan.
""")

st.markdown("")

st.subheader("Global Market Growth")

df["is_global"] = df["main_market"].apply(lambda x: 1 if x == "Global" else 0)

global_trend = df.groupby("generation")["is_global"].mean()

fig2, ax2 = plt.subplots(figsize=(7, 4))
global_trend.plot(kind="line", marker="o", ax=ax2)

ax2.set_ylabel("Proportion of Global-focused Groups")
ax2.set_title("Rise of Global-first Strategy")

st.pyplot(fig2)

st.markdown("### 🔍 Key Insight")
st.write("""
The proportion of global-focused groups rises in newer generations, suggesting a shift from regional expansion to global-first strategies.
""")
st.markdown("")

st.subheader("Secondary Market Distribution")

secondary_counts = df["secondary_market"].value_counts()

fig3, ax3 = plt.subplots(figsize=(7, 4))
secondary_counts.plot(kind="bar", ax=ax3)

ax3.set_title("Secondary Market Distribution")
ax3.set_ylabel("Number of Groups")

st.pyplot(fig3)

st.markdown("### 🔍 Key Insight")
st.write("""
Japan and Southeast Asia appear frequently as secondary markets, indicating their importance as expansion destinations beyond core domestic audiences.
""")
st.markdown("")

st.subheader("Weighted Market Influence")

market_score = {}

for _, row in df.iterrows():
    main = row["main_market"]
    sec = row["secondary_market"]

    market_score[main] = market_score.get(main, 0) + 1
    market_score[sec] = market_score.get(sec, 0) + 0.5

market_df = pd.DataFrame.from_dict(market_score, orient="index", columns=["score"])
market_df = market_df.sort_values(by="score", ascending=False)

fig4, ax4 = plt.subplots(figsize=(7, 4))
market_df.plot(kind="bar", ax=ax4)

ax4.set_title("Overall Market Influence (Weighted)")
ax4.set_ylabel("Score")

st.pyplot(fig4)

st.markdown("### 🔍 Key Insight")
st.write("""
When primary and secondary markets are considered together, Korea remains central, while Japan, Global, and Southeast Asia show strong influence in overall expansion patterns.
""")
st.markdown("")

st.subheader("Top Market Expansion Paths")

flow_df = (
    df.groupby(["main_market", "secondary_market"])
      .size()
      .reset_index(name="count")
)

flow_df["path"] = flow_df["main_market"] + " → " + flow_df["secondary_market"]
flow_df = flow_df.sort_values("count", ascending=True).tail(10)

fig5, ax5 = plt.subplots(figsize=(7, 4))
ax5.barh(flow_df["path"], flow_df["count"])

ax5.set_xlabel("Number of Groups")
ax5.set_ylabel("Expansion Path")
ax5.set_title("Top Market Expansion Paths")

st.pyplot(fig5)

st.markdown("### 🔍 Key Insight")
st.write("""
The most common expansion paths reveal that K-pop groups often move from Korea into Japan, Global markets, or Southeast Asia, reflecting structured international growth strategies.
""")
st.markdown("")

st.subheader("Prediction")

st.write("""
Groups debuting after 2020 are more likely to adopt a global-first strategy rather than expanding region by region.
""")
st.markdown("")

st.subheader("Data Notes")

st.write("""
This dataset provides full coverage of major K-pop companies (SM, JYP, YG, HYBE), while groups from smaller companies are selectively sampled to reflect broader industry trends.

Primary and secondary markets are defined based on popularity, fanbase, and market visibility rather than company operational headquarters.
""")
