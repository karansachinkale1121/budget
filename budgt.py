import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Budget Dashboard 2014-2025",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .big-title {
            font-size: 36px !important;
            font-weight: 700 !important;
            color: #2E86C1;
        }
        .subheader {
            font-size: 22px !important;
            font-weight: 600 !important;
            margin-top: 20px !important;
        }
        .metric-card {
            padding: 20px;
            border-radius: 12px;
            background-color: #f7f9fb;
            text-align: center;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-title'>📊 Union Budget Dashboard (2014 – 2025)</div>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_excel("Budget 2014-2025.xlsx")

df = load_data()

st.sidebar.header("🔎 Filter Your View")

year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))
ministries = sorted(df["Ministry Name"].unique())
selected_ministry = st.sidebar.selectbox("Select Ministry", ["All"] + ministries)

filtered_df = df[df["Year"] == year]
if selected_ministry != "All":
    filtered_df = filtered_df[filtered_df["Ministry Name"] == selected_ministry]

st.markdown("<div class='subheader'>📘 Filtered Budget Data</div>", unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True)

st.markdown("<div class='subheader'>📊 Plan vs Non-Plan Comparison</div>", unsafe_allow_html=True)

if not filtered_df.empty:
    viz_df = filtered_df.melt(
        id_vars=["Ministry Name"],
        value_vars=["Total (Plan)", "Total (Non-Plan)", "Total Plan & Non-Plan"],
        var_name="Category",
        value_name="Amount"
    )

    fig = px.bar(
        viz_df,
        x="Ministry Name",
        y="Amount",
        color="Category",
        title=f"Budget Breakdown for {year}",
        barmode="group",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

trend_ministry = st.selectbox("Select Ministry for Trend", ministries)

trend_df = df[df["Ministry Name"] == trend_ministry]

fig2 = px.line(
    trend_df,
    x="Year",
    y="Total Plan & Non-Plan",
    markers=True,
    title=f"Budget Trend for {trend_ministry}",
    template="plotly_white"
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("<div class='subheader'>📌 Summary Statistics</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric("Highest Allocation", f"{df['Total Plan & Non-Plan'].max():,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric("Lowest Allocation", f"{df['Total Plan & Non-Plan'].min():,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric("Average Allocation", f"{df['Total Plan & Non-Plan'].mean():,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
