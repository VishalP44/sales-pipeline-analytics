# Sales Pipeline Analytics & Revenue Forecasting

An end-to-end analytics project that models a B2B sales pipeline (CRM/Salesforce-style opportunity data) and surfaces pipeline health, win rates, and revenue forecasts through an interactive Streamlit dashboard.

## Business Problem

Sales operations teams need real-time visibility into the health of their pipeline to plan revenue and allocate resources effectively. Three questions drive that visibility:
- How much revenue is sitting in open pipeline, and how much of it can we realistically expect to close?
- Which regions and products are converting well, and which are underperforming?
- How long does it take to close a deal, and does that vary by region?

This project builds a small but complete pipeline to answer those questions: synthetic CRM data in, SQL-based KPI modeling, and a dashboard out.

## Approach

1. **Data generation (`data_pipeline.py`)** — Generates 1,500 synthetic B2B opportunity records (region, product, stage, deal amount, probability, dates) with a fixed random seed for reproducibility, computes `Expected_Revenue` (amount weighted by stage probability) and `Sales_Cycle_Days` for closed deals, and loads the result into a local SQLite database.
2. **Data modeling (`sales_analysis.sql`)** — Standalone SQL queries for the core KPIs: pipeline by stage, win rate by region, revenue forecast by product, and average sales cycle by region. Useful for inspecting the metrics directly in any SQLite client.
3. **Dashboard (`dashboard.py`)** — A Streamlit app that reads from the SQLite database and renders the same KPIs interactively, with region/product filters, a sales funnel, win-rate comparison, revenue mix, and a sortable opportunity table.

## Tech Stack

Python, pandas, NumPy, SQLite, SQL, Streamlit, Plotly

## Key Results (from the generated dataset)

- **Overall win rate: 63.9%** across 1,500 opportunities
- **Open pipeline: ~$222M**, with **~$93M in risk-weighted expected revenue**
- **Closed-won revenue: ~$101M**
- **Average sales cycle: 53.4 days** for won deals
- Win rate varies by region — **NA leads at 69.1%**, **EMEA at 66.2%**, **LATAM at 62.6%**, **APAC trails at 57.5%** — highlighting where deal qualification or sales execution may need attention

(Exact figures will vary slightly if you regenerate the dataset with a different seed or record count.)

## How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate the synthetic dataset (writes sales_data.db)
python data_pipeline.py

# 3. Launch the dashboard
streamlit run dashboard.py
```

The SQL queries in `sales_analysis.sql` can be run directly against `sales_data.db` with any SQLite client to inspect the underlying KPIs.

## Notes

All data is synthetically generated for demonstration purposes and does not represent any real company's CRM data.
