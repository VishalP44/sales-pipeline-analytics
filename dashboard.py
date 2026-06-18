import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Page Config
st.set_page_config(page_title="Sales Pipeline Analytics", layout="wide", page_icon="📈")

st.title("📈 Sales Pipeline & Revenue Dashboard")
st.markdown("Tracking pipeline health, win rates, and revenue forecasting across a synthetic B2B sales pipeline.")

# Load Data
@st.cache_data
def load_data():
    conn = sqlite3.connect('sales_data.db')
    df = pd.read_sql("SELECT * FROM opportunities", conn)
    conn.close()
    return df

try:
    df = load_data()
except Exception as e:
    st.error("Database not found. Please run `python data_pipeline.py` first to generate the dataset.")
    st.stop()

# Sidebar Filters
st.sidebar.header("Filters")
selected_region = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
selected_product = st.sidebar.multiselect("Select Product", options=df['Product'].unique(), default=df['Product'].unique())

filtered_df = df[(df['Region'].isin(selected_region)) & (df['Product'].isin(selected_product))]

# Top Level KPIs
st.header("Executive Summary")
col1, col2, col3, col4 = st.columns(4)

open_pipeline = filtered_df[~filtered_df['Stage'].isin(['Closed Won', 'Closed Lost'])]
closed_deals = filtered_df[filtered_df['Stage'].isin(['Closed Won', 'Closed Lost'])]

total_pipeline = open_pipeline['Amount'].sum()
expected_revenue = open_pipeline['Expected_Revenue'].sum()
closed_won = filtered_df[filtered_df['Stage'] == 'Closed Won']['Amount'].sum()

# Win Rate calculation
win_rate = (len(closed_deals[closed_deals['Stage'] == 'Closed Won']) / len(closed_deals)) * 100 if len(closed_deals) > 0 else 0

col1.metric("Open Pipeline Amount", f"${total_pipeline:,.0f}")
col2.metric("Expected Revenue (Forecast)", f"${expected_revenue:,.0f}")
col3.metric("Closed Won Revenue", f"${closed_won:,.0f}")
col4.metric("Overall Win Rate", f"{win_rate:.1f}%")

st.divider()

# Layout
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("Pipeline by Stage")
    stage_df = filtered_df.groupby('Stage')['Amount'].sum().reset_index()
    # Sort for funnel order
    stage_order = ['Prospecting', 'Qualification', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
    stage_df['Stage'] = pd.Categorical(stage_df['Stage'], categories=stage_order, ordered=True)
    stage_df = stage_df.sort_values('Stage')
    
    fig_funnel = px.funnel(stage_df, x='Amount', y='Stage', title="Sales Funnel by Amount")
    st.plotly_chart(fig_funnel, use_container_width=True)

with row1_col2:
    st.subheader("Win Rate by Region")
    region_win = closed_deals.groupby('Region').apply(
        lambda x: len(x[x['Stage'] == 'Closed Won']) / len(x) * 100 if len(x) > 0 else 0
    ).reset_index(name='Win Rate (%)')
    
    fig_win_rate = px.bar(region_win, x='Region', y='Win Rate (%)', color='Region', title="Win Rate % Across Regions")
    st.plotly_chart(fig_win_rate, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("Expected Revenue by Product")
    prod_rev = open_pipeline.groupby('Product')['Expected_Revenue'].sum().reset_index()
    
    fig_prod = px.pie(prod_rev, values='Expected_Revenue', names='Product', title="Forecasted Revenue Composition", hole=0.4)
    st.plotly_chart(fig_prod, use_container_width=True)

with row2_col2:
    st.subheader("Average Sales Cycle Duration")
    won_deals = filtered_df[filtered_df['Stage'] == 'Closed Won']
    cycle_df = won_deals.groupby('Region')['Sales_Cycle_Days'].mean().reset_index()
    
    fig_cycle = px.bar(cycle_df, x='Region', y='Sales_Cycle_Days', title="Days to Close (Won Deals)", text_auto='.1f')
    st.plotly_chart(fig_cycle, use_container_width=True)

st.divider()
st.subheader("Detailed Opportunity Data")
st.dataframe(filtered_df[['Opportunity_ID', 'Region', 'Product', 'Stage', 'Amount', 'Expected_Revenue', 'Close_Date']].sort_values(by='Amount', ascending=False).head(100))
