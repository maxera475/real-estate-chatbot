import pandas as pd
import numpy as np
import logging
from src import config

logging.basicConfig(level=logging.INFO)

class DataLoader:
    """Handles loading, merging, and preprocessing of the real estate data."""

    def __init__(self):
        self.project_path = config.PROJECT_CSV_PATH
        self.address_path = config.ADDRESS_CSV_PATH
        self.config_path = config.CONFIG_CSV_PATH
        self.variant_path = config.VARIANT_CSV_PATH
        self.master_df = None

    def _load_csvs(self):
        """Loads all necessary CSV files into pandas DataFrames."""
        try:
            df_project = pd.read_csv(self.project_path)
            df_address = pd.read_csv(self.address_path)
            df_config = pd.read_csv(self.config_path)
            df_variant = pd.read_csv(self.variant_path)
            return df_project, df_address, df_config, df_variant
        except FileNotFoundError as e:
            logging.error(f"Data loading error: {e}. Ensure CSV files are in the 'data' directory.")
            raise

    def _merge_dataframes(self, df_project, df_address, df_config, df_variant):
        """Merges the individual DataFrames into a single master DataFrame."""
        df_merged = pd.merge(df_variant, df_config, left_on='configurationId', right_on='id', suffixes=('_variant', '_config'))
        df_merged = pd.merge(df_merged, df_project, left_on='projectId', right_on='id', suffixes=('', '_project'))
        df_merged = pd.merge(df_merged, df_address, on='projectId', suffixes=('', '_address'))
        return df_merged

    def _clean_and_engineer_features(self, df):
        """Performs data cleaning and feature engineering."""
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df.dropna(subset=['price'], inplace=True)
        df['price'] = df['price'].astype(np.int64)
        
        df['carpetArea'] = pd.to_numeric(df['carpetArea'], errors='coerce')

        def extract_from_slug(slug):
            parts = str(slug).split('-')
            if len(parts) > 2:
                city = parts[-2].capitalize()
                locality = parts[-3].capitalize()
                return city, locality
            return 'Unknown', 'Unknown'

        df[['city', 'locality']] = df['slug'].apply(lambda x: pd.Series(extract_from_slug(x)))
        
        df['possessionDate'] = pd.to_datetime(df['possessionDate'], errors='coerce').dt.strftime('%b %Y')

        final_cols = {
            'projectName': 'projectName', 'city': 'city', 'locality': 'locality',
            'type': 'bhk', 'price': 'price', 'status': 'status', 'carpetArea': 'carpetArea',
            'bathrooms': 'bathrooms', 'furnishedType': 'furnishedType', 'parkingType': 'parkingType',
            'possessionDate': 'possessionDate', 'slug': 'slug'
        }
        
        for col in final_cols.keys():
            if col not in df.columns:
                df[col] = np.nan
                
        df_final = df[list(final_cols.keys())].rename(columns=final_cols)
        
        df_final['bhk'] = df_final['bhk'].str.replace('BHK', ' BHK').str.strip()
        return df_final

    def get_data(self) -> pd.DataFrame:
        """Main method to load, process, and return the master DataFrame."""
        if self.master_df is None:
            logging.info("Loading and processing data for the first time...")
            dfs = self._load_csvs()
            merged_df = self._merge_dataframes(*dfs)
            self.master_df = self._clean_and_engineer_features(merged_df)
            logging.info("Data processing complete.")
        return self.master_df