import pandas as pd
import numpy as np
import sqlite3
import random
from datetime import datetime, timedelta

def generate_mock_salesforce_data(num_records=1000):
    """Generates synthetic B2B CRM Opportunity data mirroring Salesforce/NVIDIA operations."""
    np.random.seed(42)
    random.seed(42)
    
    stages = ['Prospecting', 'Qualification', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
    probabilities = {
        'Prospecting': 0.1, 
        'Qualification': 0.3, 
        'Proposal': 0.5, 
        'Negotiation': 0.8, 
        'Closed Won': 1.0, 
        'Closed Lost': 0.0
    }
    regions = ['NA', 'EMEA', 'APAC', 'LATAM']
    products = ['Data Center GPUs', 'Gaming GPUs', 'Enterprise Software', 'Networking']
    
    data = []
    base_date = datetime.today() - timedelta(days=365)
    
    for i in range(num_records):
        created_date = base_date + timedelta(days=random.randint(0, 300))
        stage = random.choices(stages, weights=[15, 15, 15, 15, 25, 15])[0]
        
        # Calculate close date based on stage
        if stage in ['Closed Won', 'Closed Lost']:
            close_date = created_date + timedelta(days=random.randint(15, 90))
        else:
            close_date = datetime.today() + timedelta(days=random.randint(10, 90))
            
        amount = round(random.uniform(10000, 500000), 2)
        
        data.append({
            'Opportunity_ID': f'OPP-{1000+i}',
            'Region': random.choice(regions),
            'Product': random.choice(products),
            'Stage': stage,
            'Probability': probabilities[stage],
            'Amount': amount,
            'Created_Date': created_date.strftime('%Y-%m-%d'),
            'Close_Date': close_date.strftime('%Y-%m-%d')
        })
        
    return pd.DataFrame(data)

def run_pipeline():
    print("Extracting data (generating mock CRM data)...")
    df = generate_mock_salesforce_data(1500)
    
    print("Transforming data...")
    # Add calculated columns for pipeline analysis
    df['Expected_Revenue'] = df['Amount'] * df['Probability']
    df['Created_Date'] = pd.to_datetime(df['Created_Date'])
    df['Close_Date'] = pd.to_datetime(df['Close_Date'])
    
    # Calculate Sales Cycle length for closed deals
    df['Sales_Cycle_Days'] = np.where(
        df['Stage'].isin(['Closed Won', 'Closed Lost']),
        (df['Close_Date'] - df['Created_Date']).dt.days,
        np.nan
    )
    
    # Convert dates back to strings for SQLite compatibility
    df['Created_Date'] = df['Created_Date'].dt.strftime('%Y-%m-%d')
    df['Close_Date'] = df['Close_Date'].dt.strftime('%Y-%m-%d')
    
    print("Loading data into SQLite database...")
    conn = sqlite3.connect('sales_data.db')
    df.to_sql('opportunities', conn, if_exists='replace', index=False)
    conn.close()
    
    print("Pipeline execution complete. Data saved to 'sales_data.db'.")

if __name__ == "__main__":
    run_pipeline()
