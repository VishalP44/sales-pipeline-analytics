# Sales Pipeline Analytics & Forecasting

## Business Problem
In B2B sales operations (such as at NVIDIA), tracking the health of the sales pipeline, understanding win rates, and accurately forecasting revenue are critical for business planning. Sales leaders need visibility into:
- Current pipeline health across different stages.
- Win/Loss ratios across different regions and products.
- Revenue forecasts for upcoming quarters based on opportunity probabilities.

This project provides an end-to-end data solution: extracting raw CRM data, transforming it for analysis, modeling it via SQL, and serving actionable insights through a Streamlit dashboard.

## Methodology
1. **Data Ingestion & Transformation (`data_pipeline.py`)**: Simulates extraction from a CRM (like Salesforce), cleanses the data (handling missing values, data types), and loads it into a relational database (SQLite, serving as our local data warehouse akin to Databricks/Snowflake).
2. **Data Modeling (`sales_analysis.sql`)**: Contains the core SQL transformations to compute business KPIs like Win Rate, Expected Revenue, and Sales Cycle Duration.
3. **Data Visualization (`dashboard.py`)**: A Streamlit application that connects to our database and provides interactive filtering and visualization of the pipeline metrics.

## Key Insights Delivered
- **Win Rates by Region**: Identifies which geographical areas are performing best.
- **Pipeline Funnel**: Visualizes drop-off rates between sales stages (e.g., Prospecting -> Negotiation).
- **Revenue Forecasting**: Calculates expected revenue by weighting opportunity amounts by their historical or assigned probability.

## How to Run
1. **Set up the environment**:
   Make sure you have the required packages installed:
   ```bash
   pip install pandas sqlite3 streamlit plotly
   ```

2. **Run the data pipeline**:
   This will generate a realistic B2B dataset (mirroring Kaggle/Salesforce data) and process it into a SQLite database.
   ```bash
   python data_pipeline.py
   ```

3. **Launch the Streamlit dashboard**:
   ```bash
   streamlit run dashboard.py
   ```
