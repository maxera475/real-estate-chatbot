import pandas as pd
from typing import Dict, Any

def search_properties(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    """
    Filters the main DataFrame based on a dictionary of parsed filters.
    """
    if df is None or df.empty:
        return pd.DataFrame()
        
    results = df.copy()
    
    if filters.get('bhk'):
        results = results[results['bhk'] == filters['bhk']]
    if filters.get('max_price'):
        results = results[results['price'] <= filters['max_price']]
    if filters.get('city'):
        results = results[results['city'].str.lower() == filters['city'].lower()]
    if filters.get('status'):
        results = results[results['status'] == filters['status']]
    if filters.get('locality'):
        results = results[results['locality'].str.contains(filters['locality'], case=False, na=False)]
        
    return results