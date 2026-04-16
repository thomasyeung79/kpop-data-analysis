import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 页面标题
st.set_page_config(page_title="SM Entertainment Analysis", layout="wide")

st.title("SM Entertainment Data Analysis")
st.write("A simple data analysis project about SM Entertainment groups.")

# 读取数据
df = pd.read_csv("sm_groups.csv", sep=",")

# 显示原始数据
st.subheader("Raw Data")
st.dataframe(df)

# Production Center 分析
st.subheader("Distribution by Production Center")
counts = df.groupby("production_center")["group_name"].count().sort_values(ascending=False)

fig1, ax1 = plt.subplots(figsize=(10, 6))
counts.plot(kind="bar", ax=ax1)
ax1.set_title("Distribution of SM Artists by Production Center")
ax1.set_xlabel("Production Center")
ax1.set_ylabel("Number of Groups")
ax1.grid(axis="y", linestyle="--", alpha=0.7)

for i, v in enumerate(counts):
    ax1.text(i, v + 0.05, str(v), ha="center")

st.pyplot(fig1)

# Generation 分析