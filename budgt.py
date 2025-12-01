import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Budget Dashboard 2014–2025", layout="wide")

# Safe loader with error handling
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Budget 2014-2025.xlsx")
        df = df.loc[:, ~df.columns.duplicated()]  # remove duplicate columns
        return df
    except ValueError:
        st.error("❌ Error reading Excel file. Check columns & sheet format.")
        st.stop()

df = load_data()

st.title("📊 India Budget Dashboard (2014–2025)")

# Check Year column exists
if "Year" not in df.columns:
    st.error("❌ The Excel file must contain a 'Year' column.")
    st.write("Available columns:", df.columns.tolist())
    st.stop()

# Remove non-numeric columns from graph options
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

if len(numeric_cols) == 0:
    st.error("❌ No numeric columns found for graphing.")
    st.write("Columns found:", df.columns.tolist())
    st.stop()

# UI
with st.expander("📁 Show Raw Data"):
    st.dataframe(df)

st.sidebar.header("🔍 Filters")
year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))
column = st.sidebar.selectbox("Select Column", numeric_cols)

# Safe metric display
try:
    value = df.loc[df["Year"] == year, column].values[0]
    st.metric(label=f"{column} in {year}", value=f"{value:,}")
except:
    st.warning(f"⚠️ {column} has invalid or missing data for {year}")

# Safe Line Chart
try:
    fig = px.line(df, x="Year", y=column, markers=True,
                  title=f"📈 Trend of {column} (2014–2025)")
    st.plotly_chart(fig, use_container_width=True)
except ValueError:
    st.warning("⚠️ Unable to generate line chart for this column.")

# Safe Bar Chart
try:
    fig2 = px.bar(df, x="Year", y=column,
                  title=f"📊 Comparison of {column} Across Years")
    st.plotly_chart(fig2, use_container_width=True)
except ValueError:
    st.warning("⚠️ Unable to generate bar chart for this column.")



