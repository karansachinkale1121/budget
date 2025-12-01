import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Budget Dashboard", layout="wide")

# Load the Excel file located in the same GitHub repo
@st.cache_data
def load_data():
    return pd.read_excel("Budget 2014-2025.xlsx")

df = load_data()

st.title("📊 India Budget Dashboard (2014–2025)")

# Show dataset
with st.expander("📁 View Raw Dataset"):
    st.dataframe(df)

# Sidebar filters
st.sidebar.header("🔍 Filters")

year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))
column = st.sidebar.selectbox("Select Column to Visualize", df.columns[1:])

# Filter data
filtered_value = df[df["Year"] == year][column].values[0]

st.metric(label=f"{column} in {year}", value=f"{filtered_value:,}")

# Plot Trend Line
fig = px.line(
    df,
    x="Year",
    y=column,
    markers=True,
    title=f"📈 Trend of {column} Over the Years"
)

st.plotly_chart(fig, use_container_width=True)

# Bar Chart
fig2 = px.bar(
    df,
    x="Year",
    y=column,
    title=f"📊 Year-wise Comparison: {column}"
)

st.plotly_chart(fig2, use_container_width=True)

st.success("App loaded successfully using Excel file from the repository!")
