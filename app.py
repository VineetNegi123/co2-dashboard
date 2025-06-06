import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="CO₂ Reduction Calculator", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .stSelectbox {
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Display title
st.title("CO₂ Reduction Calculator")

# Carbon emission factors by country (kg CO2/kWh)
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
st.header("Input Parameters")
col1, col2, col3 = st.columns(3)

with col1:
    energy_savings = st.number_input("Energy Savings (kWh/year)", value=1040249.0)

with col2:
    selected_country = st.selectbox("Select Country", list(country_factors.keys()))
    if selected_country == "Custom":
        carbon_emission_factor = st.number_input("Custom Carbon Emission Factor (kg CO₂/kWh)", value=0.82)
    else:
        carbon_emission_factor = country_factors[selected_country]
        st.info(f"Carbon Emission Factor for {selected_country}: {carbon_emission_factor} kg CO₂/kWh")

with col3:
    electricity_rate = st.number_input("Electricity Rate ($/kWh)", value=0.14)
    savings_percentage = st.number_input("Savings Percentage", value=0.05, format="%.2f")

# Calculations
total_energy_before = energy_savings / savings_percentage
energy_after = total_energy_before - energy_savings
electricity_cost_before = total_energy_before * electricity_rate
electricity_cost_after = energy_after * electricity_rate
annual_co2_reduction = energy_savings * carbon_emission_factor

# Equivalents calculations
trees_planted = annual_co2_reduction / 22
flats_equivalent = annual_co2_reduction / 320
cars_removed = annual_co2_reduction / 200

# Results Section
st.header("Results")

# Metrics Display
col1, col2 = st.columns(2)

with col1:
    st.subheader("Energy Metrics")
    st.metric("Total Energy Before Savings (kWh/year)", f"{total_energy_before:,.2f}")
    st.metric("Energy Usage After Savings (kWh/year)", f"{energy_after:,.2f}")
    st.metric("Electricity Cost Before Savings ($)", f"{electricity_cost_before:,.2f}")
    st.metric("Electricity Cost After Savings ($)", f"{electricity_cost_after:,.2f}")

with col2:
    st.subheader("Environmental Impact")
    st.metric("Annual CO₂ Reduction (kg CO₂/year)", f"{annual_co2_reduction:,.2f}")
    st.metric("Equivalent Trees Planted", f"{trees_planted:,.2f}")
    st.metric("Equivalent Flats", f"{flats_equivalent:,.2f}")
    st.metric("Equivalent Cars Removed", f"{cars_removed:,.2f}")

# Saving Percentage Graph Style (Clean version like screenshot)
saving_years = [2024, 2025, 2026]
saving_values = [8.8, 9.0, 9.2]  # Example data only
energy_trend = [176000, 178000, 180000]  # Corresponding energy reduction data

st.subheader("📉 Saving Percentage Timeline")
colA, colB = st.columns(2)

with colA:
    st.metric("Carbon Reduction", f"{annual_co2_reduction / 1000:.1f} tCO₂e/yr")
    st.metric("Energy Reduction", f"{energy_savings / 1000:.0f}k kWh/yr")

with colB:
    df = pd.DataFrame({
        "Saving %": saving_values,
        "Energy Reduction": energy_trend
    }, index=saving_years)
    st.line_chart(df)

# Footer with information about the factors
st.markdown("---")
st.markdown("""
**Notes:**
- Trees planted equivalent assumes each tree absorbs 22 kg CO₂ per year
- Flats equivalent assumes 320 kg CO₂ per flat per year
- Cars removed equivalent assumes 200 kg CO₂ per car per year
""")
st.markdown("Made with ❤️ using Streamlit")
