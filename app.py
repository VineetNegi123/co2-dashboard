import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="CO₂ Reduction Calculator", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1300px;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("💡 CO₂ Reduction & Energy Efficiency Dashboard")

# Carbon emission factors by country (kg CO₂/kWh)
country_factors = {
    "Indonesia": 0.87,
    "Singapore": 0.408,
    "Malaysia": 0.585,
    "Thailand": 0.513,
    "Vietnam": 0.618,
    "Philippines": 0.65,
    "China": 0.555,
    "Japan": 0.474,
    "South Korea": 0.405,
    "India": 0.82,
    "Australia": 0.79,
    "United States": 0.42,
    "United Kingdom": 0.233,
    "Germany": 0.338,
    "Custom": None
}

# Input Section
st.header("🔧 Input Parameters")
col1, col2, col3 = st.columns(3)

with col1:
    energy_savings = st.number_input("Estimated Energy Savings (kWh/year)", value=1040249.0)

with col2:
    selected_country = st.selectbox("Select Country", list(country_factors.keys()))
    if selected_country == "Custom":
        carbon_emission_factor = st.number_input("Custom Carbon Emission Factor (kg CO₂/kWh)", value=0.82)
    else:
        carbon_emission_factor = country_factors[selected_country]
        st.info(f"Using carbon factor for {selected_country}: {carbon_emission_factor} kg CO₂/kWh")

with col3:
    electricity_rate = st.number_input("Electricity Rate ($/kWh)", value=0.14)
    savings_percentage = st.number_input("Savings Percentage (%)", value=8.8, format="%.2f") / 100

# Calculations
total_energy_before = energy_savings / savings_percentage if savings_percentage > 0 else 0
energy_after = total_energy_before - energy_savings
electricity_cost_before = total_energy_before * electricity_rate
electricity_cost_after = energy_after * electricity_rate
annual_co2_reduction = energy_savings * carbon_emission_factor

# Display KPIs like screenshot
st.markdown("### 📊 Key Indicators")
kpi1, kpi2 = st.columns(2)

with kpi1:
    st.metric("Carbon Reduction", f"{annual_co2_reduction / 1000:.1f} tCO₂e/yr")

with kpi2:
    st.metric("Energy Reduction", f"{energy_savings / 1000:.0f}k kWh/yr")

# Graph section
st.markdown("### 📉 Saving Percentage Trend")
years = [2024, 2025, 2026]
savings = [savings_percentage * 100] * 3  # constant based on user input
energy_trend = [energy_savings] * 3

fig = go.Figure()
fig.add_trace(go.Scatter(x=years, y=energy_trend, name='Energy Reduction', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=years, y=savings, name='Saving %', yaxis='y2', line=dict(color='purple', dash='dot')))

fig.update_layout(
    height=400,
    xaxis=dict(title='Year'),
    yaxis=dict(title='Energy Reduction (kWh)', side='left'),
    yaxis2=dict(title='Saving %', overlaying='y', side='right', showgrid=False),
    legend=dict(x=0.01, y=1.15, orientation='h'),
    margin=dict(l=40, r=40, t=40, b=40),
    template='simple_white'
)
st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
**Notes:**
- Carbon factor depends on selected country or custom input
- Graph assumes constant energy saving trend across 3 years
- Energy reduction is recalculated based on input savings percentage
""")
st.caption("Crafted for client-ready insights • Powered by Streamlit")
