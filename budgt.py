import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Budget Dashboard 2014–2025", layout="wide")

# Load Excel data from GitHub repository
@st.cache_data
def load_data():
    return pd.read_excel("Budget 2014-2025.xlsx")

df = load_data()

st.title("📊 India Budget Dashboard (2014–2025)")

# Show Dataset
with st.expander("📁 Show Raw Data"):
    st.dataframe(df)

# Sidebar
st.sidebar.header("🔍 Filters")

year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))
column = st.sidebar.selectbox("Select Column", df.columns[1:])

value = df.loc[df["Year"] == year, column].values[0]
st.metric(label=f"{column} in {year}", value=f"{value:,}")

# Line Chart
fig = px.line(
    df, 
    x="Year", 
    y=column, 
    markers=True, 
    title=f"📈 Trend of {column} (2014–2025)"
)
st.plotly_chart(fig, use_container_width=True)

# Bar Chart
fig2 = px.bar(
    df, 
    x="Year", 
    y=column, 
    title=f"📊 Comparison of {column} Across Years"
)
st.plotly_chart(fig2, use_container_width=True)


