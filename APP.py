import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Student Performance Analysis",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS (UI IMPROVEMENT)
# -----------------------------
st.markdown("""
<style>
.metric-box {
    background-color: #f0f2f6;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}
.title-text {
    font-size: 36px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.markdown("<div class='title-text'>🎓 Student Performance Analysis Dashboard</div>", unsafe_allow_html=True)
st.write("Analyze student academic performance using interactive filters and visual analytics.")

# --------------------
# Load Data
# --------------------
def load_data():
    return pd.read_csv("final_student_data_after_eda.xls")

df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Filter Students")

gender = st.sidebar.multiselect(
    "Gender",
    df["gender"].unique(),
    default=df["gender"].unique()
)

testprep = st.sidebar.multiselect(
    "Test Preparation",
    df["testprep"].unique(),
    default=df["testprep"].unique()
)

lunch = st.sidebar.multiselect(
    "Lunch Type",
    df["lunchtype"].unique(),
    default=df["lunchtype"].unique()
)

filtered_df = df[
    (df["gender"].isin(gender)) &
    (df["testprep"].isin(testprep)) &
    (df["lunchtype"].isin(lunch))
]

# -----------------------------
# KPI METRICS
# -----------------------------
st.markdown("## 📌 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("👩‍🎓 Total Students", filtered_df.shape[0])
col2.metric("📘 Avg Math", round(filtered_df["mathscore"].mean(), 2))
col3.metric("📗 Avg Reading", round(filtered_df["readingscore"].mean(), 2))
col4.metric("✍ Avg Writing", round(filtered_df["writingscore"].mean(), 2))
col5.metric("🏆 Avg Total", round(filtered_df["total_score"].mean(), 2))

# -----------------------------
# PASS / FAIL ANALYSIS
# -----------------------------
st.markdown("## ✅ Pass / ❌ Fail Analysis")

filtered_df["result"] = filtered_df["total_score"].apply(
    lambda x: "Pass" if x >= 150 else "Fail"
)

result_counts = filtered_df["result"].value_counts()

fig, ax = plt.subplots()
ax.pie(result_counts, labels=result_counts.index, autopct="%1.1f%%", startangle=90)
ax.set_title("Pass vs Fail Distribution")
st.pyplot(fig)

# -----------------------------
# SCORE DISTRIBUTION
# -----------------------------
st.markdown("## 📊 Score Distributions")

scores = ["mathscore", "readingscore", "writingscore"]

for score in scores:
    fig, ax = plt.subplots()
    ax.hist(filtered_df[score], bins=30)
    ax.set_title(f"{score.capitalize()} Distribution")
    ax.set_xlabel(score.capitalize())
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

# -----------------------------
# GENDER ANALYSIS
# -----------------------------
st.markdown("## 👨‍👩‍👧 Gender-wise Performance")

gender_avg = filtered_df.groupby("gender")[scores].mean()

fig, ax = plt.subplots()
gender_avg.plot(kind="bar", ax=ax)
ax.set_ylabel("Average Score")
ax.set_title("Average Scores by Gender")
st.pyplot(fig)

# -----------------------------
# TEST PREPARATION IMPACT
# -----------------------------
st.markdown("## 📚 Impact of Test Preparation")

testprep_avg = filtered_df.groupby("testprep")[scores].mean()

fig, ax = plt.subplots()
testprep_avg.plot(kind="bar", ax=ax)
ax.set_ylabel("Average Score")
ax.set_title("Test Preparation vs Performance")
st.pyplot(fig)

# -----------------------------
# LUNCH TYPE ANALYSIS
# -----------------------------
st.markdown("## 🍱 Lunch Type vs Performance")

lunch_avg = filtered_df.groupby("lunchtype")[scores].mean()

fig, ax = plt.subplots()
lunch_avg.plot(kind="bar", ax=ax)
ax.set_ylabel("Average Score")
ax.set_title("Lunch Type Impact")
st.pyplot(fig)

# -----------------------------
# TOPPERS
# -----------------------------
st.markdown("## 🏆 Top 10 Students")

top_students = filtered_df.sort_values(by="total_score", ascending=False).head(10)
st.dataframe(top_students)

# -----------------------------
# DATA PREVIEW
# -----------------------------
st.markdown("## 📋 Filtered Dataset Preview")
st.dataframe(filtered_df.head(25))

# -----------------------------
# DOWNLOAD BUTTON
# -----------------------------
st.markdown("## ⬇ Download Data")

csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_student_data.csv",
    mime="text/csv"
)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("🎓 **Student Performance Analysis Project** | Built with ❤️ using **Streamlit & Data Science**")

