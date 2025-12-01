import subprocess
import sys

# Auto-install modules if missing
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try imports → If fail → Install → Import again
try:
    import pandas as pd
except:
    install("pandas")
    import pandas as pd

try:
    import plotly.express as px
except:
    install("plotly")
    import plotly.express as px

try:
    import streamlit as st
except:
    install("streamlit")
    import streamlit as st

try:
    import openpyxl
except:
    install("openpyxl")
    import openpyxl

st.set_page_config(page_title="Budget Dashboard", layout="wide")

# Load dataset from GitHub repo
@st.cache_data
def load_data():
    return pd.read_excel("Budget 2014-2025.xlsx")

df = load_data()

st.title("📊 India Budget Dashboard (2014–2025)")

# Show raw dataset
with st.expander("📁 View Raw Dataset"):
    st.dataframe(df)

# Sidebar Filters
st.sidebar.header("🔍 Filters")
year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))
column = st.sidebar.selectbox("Select Column", df.columns[1:])

value = df[df["Year"] == year][column].values[0]
st.metric(label=f"{column} in {year}", value=f"{value:,}")

# Trend Line
fig = px.line(df, x="Year", y=column, markers=True,
              title=f"📈 Trend of {column} Over the Years")
st.plotly_chart(fig, use_container_width=True)

# Bar Chart
fig2 = px.bar(df, x="Year", y=column,
              title=f"📊 Year-wise Comparison: {column}")
st.plotly_chart(fig2, use_container_width=True)

st.success("App loaded successfully with auto-install modules 🎉")

