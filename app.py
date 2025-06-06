import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page settings
st.set_page_config(layout="wide", page_title="CO₂ Savings Dashboard")

# Sidebar
with st.sidebar:
    st.title("🌱 CO₂ Calculator")
    st.markdown("Upload your HVAC / energy file below:")
    uploaded_file = st.file_uploader("Upload Excel or CSV", type=["xlsx", "csv"])
    st.markdown("------")
    st.info("Example: Energy trends, BMS data")

# Title
st.title("HVAC Efficiency & Carbon Reduction Dashboard")

# Static data for now (you can make this dynamic later)
years = [2024, 2025, 2026]
net_income = [-8000, 12090, 50000]
savings_percent = [8.8, 9.2, 9.5]

# Top KPIs and Net Income Chart
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💰 Payback & Net Income (3-Year Projection)")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=net_income, fill='tozeroy', name="Net Income",
        line=dict(color="deepskyblue")
    ))
    fig.add_vline(x=2025, line_dash="dash", annotation_text="Payback Date", annotation_position="top left")
    fig.update_layout(
        height=350,
        xaxis_title="Year",
        yaxis_title="US Dollars"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.metric(label="Payback Period", value="09 Months")
    st.metric(label="Net Income (3yrs)", value="135k USD")
    st.metric(label="Carbon Reduction", value="73.8 tCO₂e/year")
    st.metric(label="Energy Reduction", value="176k kWh/year")

# Bottom chart
st.subheader("📉 Annual Energy Saving Percentage")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=years, y=savings_percent,
    name="Saving %", line=dict(color="green")
))
fig2.update_layout(height=300, xaxis_title="Year", yaxis_title="Saving %")
st.plotly_chart(fig2, use_container_width=True)

# File preview
if uploaded_file:
    st.subheader("📁 Uploaded File Preview")
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"Failed to read file: {e}")

