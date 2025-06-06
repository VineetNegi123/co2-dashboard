import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="LIPO Mall CO₂ Dashboard", layout="wide")

# Sidebar for file upload and project info
with st.sidebar:
    st.title("🌇 LIPO Mall – AI HVAC Savings")
    st.write("This dashboard estimates cost savings, energy savings, and CO₂ impact.")
    st.markdown("---")
    st.metric(label="Cooling Load", value="21.9M RTh/year")
    st.metric(label="Tariff", value="$0.14 / kWh")
    st.metric(label="Carbon Factor (ID)", value="0.82 kg CO₂/kWh")
    st.markdown("---")
    st.caption("Developed for proposal use")

# Header
st.title("📊 Energy Optimization Dashboard – LIPO Mall Puri")

# Key data (static for now)
total_cooling_energy = 21900000  # RTh/year
energy_savings = 1040249  # kWh/year
carbon_factor = 0.82  # kg CO2/kWh
tariff = 0.14  # $/kWh
savings_percent = 0.05
initial_cost = 88817
software_fee = 72817
annual_savings = 145634
payback_years = initial_cost / annual_savings

# CO₂ reduction
co2_reduction = energy_savings * carbon_factor

# Impact Equivalents
trees = co2_reduction / 22
flats = co2_reduction / 320
cars = co2_reduction / 200

# Layout with KPIs
col1, col2 = st.columns(2)

with col1:
    st.subheader("⚡️ Annual Energy Savings")
    st.metric("Energy Saved (kWh/year)", f"{energy_savings:,.0f}")
    st.metric("Electricity Cost Saved ($)", f"{annual_savings:,.0f}")
    st.metric("Payback Period (Years)", f"{payback_years:.2f}")

with col2:
    st.subheader("🌍 Environmental Impact")
    st.metric("CO₂ Reduced (kg/year)", f"{co2_reduction:,.0f}")
    st.metric("Trees Planted Equivalent", f"{trees:,.0f}")
    st.metric("Cars Removed", f"{cars:,.0f}")

# Line chart – Net income over time
st.subheader("💸 Cumulative Net Income (10 Years)")
years = list(range(0, 10))
cashflow = [-initial_cost] + [annual_savings - software_fee] * 9
cumulative = [cashflow[0]]
for i in range(1, len(cashflow)):
    cumulative.append(cumulative[-1] + cashflow[i])

fig = go.Figure()
fig.add_trace(go.Bar(x=years, y=cashflow, name='Annual Net Savings', marker_color='green'))
fig.add_trace(go.Scatter(x=years, y=cumulative, name='Cumulative Savings', mode='lines+markers', line=dict(color='blue')))
fig.add_vline(x=payback_years, line_dash="dash", line_color="orange", annotation_text=f"Payback: Year {payback_years:.2f}")
fig.update_layout(title="Cash Flow & Savings Timeline", xaxis_title="Year", yaxis_title="US Dollars", height=400)
st.plotly_chart(fig, use_container_width=True)

# Notes
st.markdown("---")
st.markdown("**📘 Assumptions & References:**")
st.markdown("- Cooling Load: 21.9M RTh/year")
st.markdown("- Savings based on AI optimization ~5% efficiency gain")
st.markdown("- Cost assumptions from Fast Track Proposal")
st.markdown("- Carbon factor: Jakarta = 0.82 kg CO₂/kWh")

st.caption("Made with ❤️ for LIPO Mall AI-HVAC pilot proposal")
