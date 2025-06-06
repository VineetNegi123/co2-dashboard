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
    .metric-box {
        background-color: #f9f9f9;
        padding: 30px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        font-size: 28px;
        font-weight: bold;
    }
    .metric-label {
        font-size: 16px;
        color: #666;
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
    savings_percentage = st.number_input("Savings Percentage", value=8.8, format="%.2f") / 100

# Calculations
total_energy_before = energy_savings / savings_percentage if savings_percentage > 0 else 0
energy_after = total_energy_before - energy_savings
electricity_cost_before = total_energy_before * electricity_rate
electricity_cost_after = energy_after * electricity_rate
annual_co2_reduction = energy_savings * carbon_emission_factor

# Monthly breakdown
typical_month_weights = [8.5, 7.2, 8.4, 7.9, 8.5, 8.2, 8.6, 8.4, 8.1, 8.6, 8.2, 9.4]  # Weighted for real distribution
weight_sum = sum(typical_month_weights)
monthly_energy = [(energy_savings * w / weight_sum) for w in typical_month_weights]

# ROI Calculation Section
initial_investment = st.number_input("Initial Investment ($)", value=16000.0)
software_fee = st.number_input("Annual Software Fee ($)", value=72817.0)
years = 10
annual_savings = energy_savings * electricity_rate
cumulative_savings = []
net_cash_flow = []
total_costs = [initial_investment + software_fee] + [software_fee] * (years - 1)
for i in range(years):
    net = annual_savings - total_costs[i]
    net_cash_flow.append(net if i == 0 else net_cash_flow[-1] + net)
    cumulative_savings.append(net_cash_flow[-1])

# KPIs
st.markdown("### 📊 Overview")
metrics_col, chart_col = st.columns([1, 3])

with metrics_col:
    st.markdown(f"""
    <div class=\"metric-box\">{annual_co2_reduction / 1000:.1f}<div class=\"metric-label\">tCO₂e/yr<br>Carbon Reduction</div></div>
    <br>
    <div class=\"metric-box\">{energy_savings / 1000:,.0f}k<div class=\"metric-label\">kWh/yr<br>Energy Reduction</div></div>
    """, unsafe_allow_html=True)

with chart_col:
    st.markdown("#### 📉 Monthly Energy Saving Trend (2025)")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[f"2025-{m:02d}" for m in range(1, 13)],
        y=monthly_energy,
        name='Monthly Energy Reduction (kWh)',
        fill='tozeroy',
        line=dict(color='rgba(0, 98, 255, 1)', width=3),
        mode='lines+markers+text',
        text=[f"{int(val/1000)}k" for val in monthly_energy],
        textposition="top center"
    ))

    fig.update_layout(
        height=420,
        xaxis=dict(title='', showgrid=False, tickfont=dict(size=14)),
        yaxis=dict(title='', showgrid=True, zeroline=False, gridcolor='lightgrey', tickfont=dict(size=14)),
        margin=dict(l=10, r=10, t=30, b=30),
        showlegend=False,
        plot_bgcolor='white'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 📈 10-Year Cash Flow Forecast")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=list(range(years)), y=[annual_savings]*years, name="Annual Savings", marker_color="green"))
    fig2.add_trace(go.Bar(x=list(range(years)), y=total_costs, name="Total Costs", marker_color="red"))
    fig2.add_trace(go.Scatter(x=list(range(years)), y=cumulative_savings, mode='lines+markers', name="Cumulative Net Savings", line=dict(color='blue')))

    fig2.update_layout(
        barmode='group',
        height=400,
        xaxis_title='Year',
        yaxis_title='Cash Flow ($)',
        plot_bgcolor='white',
        showlegend=True
    )
    st.plotly_chart(fig2, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
**Notes:**
- Monthly energy values follow realistic cooling load weighting
- Cash flow graph includes real inputs for investment & software cost
- Update savings and rate to apply per-project view
""")
st.caption("Crafted for client-ready insights • Powered by Streamlit")
