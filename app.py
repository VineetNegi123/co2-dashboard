import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="CO₂ Reduction Dashboard", layout="wide")

# Title
st.title("CO₂ Savings Overview")

# Sidebar (optional info or project notes)
with st.sidebar:
    st.header("Project Info")
    st.write("AI HVAC proposal for LIPO Mall Puri")
    st.markdown("---")
    st.write("Energy savings and carbon reduction highlights")

# Input values (hardcoded from your Excel)
energy_savings = 1040249  # kWh/year
carbon_reduction = 73800  # kg CO2/year

# Convert to nicer display format
energy_savings_display = f"{energy_savings/1000:.0f}k kWh/year"
carbon_reduction_display = f"{carbon_reduction/1000:.1f} tCO₂e/year"

# Top metrics display
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Energy Reduction", value=energy_savings_display)

with col2:
    st.metric(label="Carbon Reduction", value=carbon_reduction_display)

# Savings percent line chart (mocked for now)
st.subheader("📉 Annual Saving Percentage")
saving_years = [2024, 2025, 2026]
saving_values = [8.8, 9.1, 9.3]

st.line_chart(pd.DataFrame({"Saving %": saving_values}, index=saving_years))

# Footer
st.markdown("---")
st.caption("Visualization generated for proposal use • Based on LIPO Mall HVAC optimization potential")

