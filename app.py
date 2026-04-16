import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# 页面设置
# -------------------------
st.set_page_config(page_title="SM Analysis Dashboard", layout="wide")

st.title("SM Entertainment Data Analysis Dashboard")
st.caption("An interactive dashboard analysing SM groups by production center, generation, and group size.")

# -------------------------
# 读取数据
# -------------------------
df = pd.read_csv("sm_groups.csv")

# -------------------------
# Sidebar 筛选
# -------------------------
st.sidebar.header("Filter Options")

selected_center = st.sidebar.multiselect(
    "Select Production Center",
    options=sorted(df["production_center"].unique()),
    default=sorted(df["production_center"].unique())
)

selected_gen = st.sidebar.multiselect(
    "Select Generation",
    options=sorted(df["generation"].unique()),
    default=sorted(df["generation"].unique())
)

filtered_df = df[
    (df["production_center"].isin(selected_center)) &
    (df["generation"].isin(selected_gen))
]

# -------------------------
# 顶部统计卡片
# -------------------------
total_groups = len(filtered_df)
avg_members = round(filtered_df["member_count"].mean(), 2) if total_groups > 0 else 0
total_centers = filtered_df["production_center"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Groups", total_groups)
col2.metric("Average Members", avg_members)
col3.metric("Production Centers", total_centers)

st.divider()

# -------------------------
# 数据表
# -------------------------
with st.expander("View Filtered Data"):
    st.dataframe(filtered_df, use_container_width=True)

# -------------------------
# Tabs
# -------------------------
tab1, tab2 = st.tabs(["Structure Analysis", "Generation Analysis"])

# -------------------------
# Tab 1: 结构分析
# -------------------------
with tab1:
    st.subheader("Distribution by Production Center")

    counts = (
        filtered_df.groupby("production_center")["group_name"]
        .count()
        .sort_values(ascending=False)
    )

    fig1, ax1 = plt.subplots(figsize=(8, 5))
    counts.plot(kind="bar", ax=ax1)
    ax1.set_title("Distribution of Groups by Production Center")
    ax1.set_xlabel("Production Center")
    ax1.set_ylabel("Number of Groups")
    ax1.grid(axis="y", linestyle="--", alpha=0.7)

    for i, v in enumerate(counts):
        ax1.text(i, v + 0.05, str(v), ha="center")

    st.pyplot(fig1)

    st.subheader("Average Group Size by Production Center")

    avg_members_center = (
        filtered_df.groupby("production_center")["member_count"]
        .mean()
        .sort_values(ascending=False)
    )

    fig2, ax2 = plt.subplots(figsize=(8, 5))
    avg_members_center.plot(kind="bar", ax=ax2)
    ax2.set_title("Average Group Size by Production Center")
    ax2.set_xlabel("Production Center")
    ax2.set_ylabel("Average Members")
    ax2.grid(axis="y", linestyle="--", alpha=0.7)

    for i, v in enumerate(avg_members_center):
        ax2.text(i, v + 0.05, f"{v:.1f}", ha="center")

    st.pyplot(fig2)

# -------------------------
# Tab 2: 世代分析
# -------------------------
with tab2:
    st.subheader("Distribution by Generation")

    gen_counts = (
        filtered_df.groupby("generation")["group_name"]
        .count()
        .sort_values()
    )

    fig3, ax3 = plt.subplots(figsize=(8, 5))
    gen_counts.plot(kind="bar", ax=ax3)
    ax3.set_title("Distribution of Groups by Generation")
    ax3.set_xlabel("Generation")
    ax3.set_ylabel("Number of Groups")
    ax3.grid(axis="y", linestyle="--", alpha=0.7)

    for i, v in enumerate(gen_counts):
        ax3.text(i, v + 0.05, str(v), ha="center")

    st.pyplot(fig3)

    st.subheader("Average Group Size by Generation")

    avg_members_gen = (
        filtered_df.groupby("generation")["member_count"]
        .mean()
        .sort_values()
    )

    fig4, ax4 = plt.subplots(figsize=(8, 5))
    avg_members_gen.plot(kind="bar", ax=ax4)
    ax4.set_title("Average Group Size by Generation")
    ax4.set_xlabel("Generation")
    ax4.set_ylabel("Average Members")
    ax4.grid(axis="y", linestyle="--", alpha=0.7)

    for i, v in enumerate(avg_members_gen):
        ax4.text(i, v + 0.05, f"{v:.1f}", ha="center")

    st.pyplot(fig4)
