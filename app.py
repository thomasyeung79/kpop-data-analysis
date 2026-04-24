import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="K-pop Industry Analysis", layout="wide")

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

BIG4 = ["SM", "JYP", "YG", "HYBE"]

df["company_group"] = df["company"].apply(
    lambda x: x if x in BIG4 else "Others"
)

df["secondary_market"] = df["secondary_market"].fillna("N/A")


st.title("🎤 K-pop Industry Analysis Dashboard")
st.caption(
    "A data dashboard analysing K-pop artists by company, generation, market, gender, and artist type."
)

mode = st.radio(
    "Select Mode",
    ["Dashboard", "Story Mode"],
    horizontal=True
)


st.sidebar.header("Filter Options")

selected_type = st.sidebar.multiselect(
    "Artist Type",
    options=sorted(df["artist_type"].unique()),
    default=sorted(df["artist_type"].unique())
)

selected_gender = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["gender"].unique()),
    default=sorted(df["gender"].unique())
)

selected_market = st.sidebar.multiselect(
    "Main Market",
    options=sorted(df["main_market"].unique()),
    default=sorted(df["main_market"].unique())
)

selected_generation = st.sidebar.multiselect(
    "Generation",
    options=["1st Gen", "2nd Gen", "3rd Gen", "4th Gen", "5th Gen"],
    default=["1st Gen", "2nd Gen", "3rd Gen", "4th Gen", "5th Gen"]
)

base_df = df[
    (df["artist_type"].isin(selected_type)) &
    (df["gender"].isin(selected_gender)) &
    (df["main_market"].isin(selected_market)) &
    (df["generation"].isin(selected_generation))
]

if base_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()


def show_dashboard(data, title):
    if data.empty:
        st.warning("No data available in this section.")
        return

    st.subheader(title)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Artists", len(data))
    col2.metric("Companies", data["company"].nunique())
    col3.metric("Main Markets", data["main_market"].nunique())
    col4.metric("Generations", data["generation"].nunique())

    st.markdown("### 📋 Artist Dataset")
    st.dataframe(
        data.sort_values(["company", "debut_year", "artist_name"]),
        use_container_width=True,
        height=260
    )

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### 🏢 Company Distribution")
        company_counts = data["company"].value_counts()

        fig, ax = plt.subplots(figsize=(6, 4))
        company_counts.plot(kind="bar", ax=ax)
        ax.set_xlabel("Company")
        ax.set_ylabel("Number of Artists")
        ax.set_title("Artists by Company")
        st.pyplot(fig)

    with col_b:
        st.markdown("### 👥 Artist Type")
        type_counts = data["artist_type"].value_counts()

        fig, ax = plt.subplots(figsize=(6, 4))
        type_counts.plot(kind="bar", ax=ax)
        ax.set_xlabel("Artist Type")
        ax.set_ylabel("Count")
        ax.set_title("Group vs Solo")
        st.pyplot(fig)

    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown("### 📅 Debut Year Trend")
        debut_trend = data["debut_year"].value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(6, 4))
        debut_trend.plot(kind="line", marker="o", ax=ax)
        ax.set_xlabel("Debut Year")
        ax.set_ylabel("Number of Artists")
        ax.set_title("Debut Trend Over Time")
        st.pyplot(fig)

    with col_d:
        st.markdown("### 🌍 Main Market Distribution")
        market_counts = data["main_market"].value_counts()

        fig, ax = plt.subplots(figsize=(6, 4))
        market_counts.plot(kind="bar", ax=ax)
        ax.set_xlabel("Main Market")
        ax.set_ylabel("Count")
        ax.set_title("Main Market Focus")
        st.pyplot(fig)

    st.markdown("---")

    st.markdown("### 🔍 Key Insights")

    top_company = data["company"].value_counts().idxmax()
    top_market = data["main_market"].value_counts().idxmax()
    top_generation = data["generation"].value_counts().idxmax()

    st.write(f"""
- **{top_company}** has the largest number of artists in this view.
- The most common main market is **{top_market}**.
- The most represented generation is **{top_generation}**.
- This suggests that company strategy, debut timing, and market focus are closely connected in the K-pop industry.
""")


def generate_ai_style_insight(data):
    if data.empty:
        return "No data available for insight generation."

    top_company = data["company_group"].value_counts().idxmax()
    top_market = data["main_market"].value_counts().idxmax()
    top_generation = data["generation"].value_counts().idxmax()

    group_count = len(data[data["artist_type"] == "group"])
    solo_count = len(data[data["artist_type"] == "solo"])

    insight = f"""
Based on the current dataset, **{top_company}** shows the strongest presence among major K-pop companies.

The data also suggests that **{top_market}** is the most important main market, while **{top_generation}** artists are the most represented generation.

From an artist-structure perspective, the dataset contains **{group_count} groups** and **{solo_count} solo artists**, showing that group-based branding is still the dominant model in the K-pop industry.

Overall, this indicates that K-pop companies continue to rely on group identity while expanding into international markets through selected solo acts and market-specific strategies.
"""
    return insight


if mode == "Dashboard":

    tabs = st.tabs(["All", "SM", "JYP", "YG", "HYBE", "Others"])

    with tabs[0]:
        show_dashboard(base_df, "🌐 Overall Industry View")

    with tabs[1]:
        show_dashboard(
            base_df[base_df["company_group"] == "SM"],
            "🏢 SM Entertainment"
        )

    with tabs[2]:
        show_dashboard(
            base_df[base_df["company_group"] == "JYP"],
            "🏢 JYP Entertainment"
        )

    with tabs[3]:
        show_dashboard(
            base_df[base_df["company_group"] == "YG"],
            "🏢 YG Entertainment"
        )

    with tabs[4]:
        show_dashboard(
            base_df[base_df["company_group"] == "HYBE"],
            "🏢 HYBE"
        )

    with tabs[5]:
        show_dashboard(
            base_df[base_df["company_group"] == "Others"],
            "🏢 Other Companies"
        )

    st.markdown("---")

    st.subheader("🏢 Company Comparison")

    compare_df = base_df.copy()
    compare_df = compare_df[
        compare_df["company_group"].isin(["SM", "JYP", "YG", "HYBE"])
    ]

    if compare_df.empty:
        st.warning("No data available for comparison.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📊 Artist Count by Company")
            company_counts = compare_df["company_group"].value_counts()

            fig, ax = plt.subplots()
            company_counts.plot(kind="bar", ax=ax)
            ax.set_xlabel("Company")
            ax.set_ylabel("Number of Artists")
            st.pyplot(fig)

        with col2:
            st.markdown("### 👥 Group vs Solo by Company")

            pivot = pd.crosstab(
                compare_df["company_group"],
                compare_df["artist_type"]
            )

            fig, ax = plt.subplots()
            pivot.plot(kind="bar", stacked=True, ax=ax)
            ax.set_xlabel("Company")
            ax.set_ylabel("Count")
            st.pyplot(fig)

        st.markdown("---")

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("### 📅 Generation Distribution")

            gen_pivot = pd.crosstab(
                compare_df["company_group"],
                compare_df["generation"]
            )

            fig, ax = plt.subplots()
            gen_pivot.plot(kind="bar", stacked=True, ax=ax)
            ax.set_xlabel("Company")
            ax.set_ylabel("Count")
            st.pyplot(fig)

        with col4:
            st.markdown("### 🌍 Market Focus")

            market_pivot = pd.crosstab(
                compare_df["company_group"],
                compare_df["main_market"]
            )

            fig, ax = plt.subplots()
            market_pivot.plot(kind="bar", stacked=True, ax=ax)
            ax.set_xlabel("Company")
            ax.set_ylabel("Count")
            st.pyplot(fig)

        st.markdown("---")

        st.subheader("🚀 Market Expansion Path")

        market_flow = (
            compare_df.groupby(["company_group", "main_market"])
            .size()
            .unstack()
            .fillna(0)
        )

        fig, ax = plt.subplots()
        market_flow.plot(kind="bar", stacked=True, ax=ax)

        ax.set_xlabel("Company")
        ax.set_ylabel("Artist Count")
        st.pyplot(fig)

    st.markdown("---")

    st.subheader("🤖 AI-Style Insight Generator")

    if st.button("🤖 Generate Industry Insight"):
        insight_text = generate_ai_style_insight(base_df)
        st.info(insight_text)

    st.markdown("---")

    st.subheader("🎯 Customize Analysis")

    selected_market_single = st.selectbox(
        "Select Main Market",
        options=sorted(base_df["main_market"].unique())
    )

    filtered_df = base_df[base_df["main_market"] == selected_market_single]

    st.write(f"Showing data for market: {selected_market_single}")

    st.dataframe(filtered_df, use_container_width=True)

    st.markdown("---")

    st.subheader("📈 Strategy Recommendation")

    top_market = base_df["main_market"].value_counts().idxmax()

    recommendation = f"""
Based on current data, companies should prioritize expansion into **{top_market}** market.

Focusing on this region could increase global influence and audience reach.
"""

    st.success(recommendation)

    st.markdown("---")

    st.subheader("📌 Data Notes")
    st.write("""
This dataset focuses on officially recognised and currently relevant K-pop artists and related solo acts.

Company classification is based on current or officially recognised affiliation where possible.  
For analysis purposes, SM, JYP, YG, and HYBE are treated as major company groups, while other companies are grouped under Others in the dashboard view.
""")


elif mode == "Story Mode":

    st.subheader("📖 K-pop Industry Story Mode")

    total_artists = len(base_df)
    total_companies = base_df["company"].nunique()
    top_company_group = base_df["company_group"].value_counts().idxmax()
    top_market = base_df["main_market"].value_counts().idxmax()
    top_generation = base_df["generation"].value_counts().idxmax()

    group_count = len(base_df[base_df["artist_type"] == "group"])
    solo_count = len(base_df[base_df["artist_type"] == "solo"])

    st.markdown(f"""
### 1. Industry Overview

This dataset contains **{total_artists} artists** across **{total_companies} companies**.

The dataset includes both groups and solo artists:
- Groups: **{group_count}**
- Solo artists: **{solo_count}**

This structure reflects the dual nature of the K-pop industry: group-based branding remains central, while solo careers are also becoming increasingly important.

---

### 2. Company Structure

The strongest company group in the current filtered dataset is **{top_company_group}**.

SM, JYP, YG, and HYBE are treated as major company groups, while other agencies are grouped as **Others** for broader industry comparison.

This allows the dashboard to compare both major company strategies and the wider K-pop ecosystem.

---

### 3. Market Direction

The most common main market is **{top_market}**.

This suggests that market focus is not only shaped by artist identity, but also by company strategy, language, and international expansion plans.

---

### 4. Generation Trend

The most represented generation is **{top_generation}**.

This helps show how different eras of K-pop are represented in the dataset and how market strategies have shifted across generations.

---

### 5. Key Conclusion

K-pop companies still rely heavily on group identity, but solo artists and market-specific strategies are becoming more important.

The industry is moving from a Korea-centered model toward a more diversified global strategy.
""")

    st.markdown("---")

    st.subheader("🤖 Story Insight")

    st.info(generate_ai_style_insight(base_df))
