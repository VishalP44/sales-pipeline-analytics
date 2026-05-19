-- 1. Pipeline Health: Total Amount and Expected Revenue by Stage
SELECT 
    Stage,
    COUNT(Opportunity_ID) as Opportunity_Count,
    SUM(Amount) as Total_Pipeline_Amount,
    SUM(Expected_Revenue) as Total_Expected_Revenue
FROM opportunities
GROUP BY Stage
ORDER BY Total_Pipeline_Amount DESC;

-- 2. Win Rate by Region
WITH RegionStats AS (
    SELECT 
        Region,
        SUM(CASE WHEN Stage = 'Closed Won' THEN 1 ELSE 0 END) as Won_Deals,
        SUM(CASE WHEN Stage IN ('Closed Won', 'Closed Lost') THEN 1 ELSE 0 END) as Total_Closed_Deals
    FROM opportunities
    GROUP BY Region
)
SELECT 
    Region,
    Won_Deals,
    Total_Closed_Deals,
    ROUND(CAST(Won_Deals AS FLOAT) / Total_Closed_Deals * 100, 2) as Win_Rate_Percentage
FROM RegionStats
ORDER BY Win_Rate_Percentage DESC;

-- 3. Revenue Forecasting: Expected Revenue by Product for Open Pipeline
SELECT 
    Product,
    SUM(Expected_Revenue) as Forecasted_Revenue,
    SUM(Amount) as Total_Open_Amount
FROM opportunities
WHERE Stage NOT IN ('Closed Won', 'Closed Lost')
GROUP BY Product
ORDER BY Forecasted_Revenue DESC;

-- 4. Sales Cycle Length: Average Sales Cycle Duration by Region (for Won Deals)
SELECT 
    Region,
    ROUND(AVG(Sales_Cycle_Days), 1) as Avg_Sales_Cycle_Days
FROM opportunities
WHERE Stage = 'Closed Won'
GROUP BY Region
ORDER BY Avg_Sales_Cycle_Days ASC;
