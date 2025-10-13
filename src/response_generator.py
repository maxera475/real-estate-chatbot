import streamlit as st
import pandas as pd
from typing import Dict, Any
from src.utils import format_price
from src.config import MAX_RESULTS_TO_DISPLAY

def generate_summary(results_df: pd.DataFrame, filters: Dict[str, Any]) -> str:
    """Generates a dynamic, data-grounded summary of the search results."""
    if results_df.empty:
        parts = []
        if 'bhk' in filters: parts.append(filters['bhk'])
        if 'city' in filters: parts.append(f"in {filters['city']}")
        if 'max_price' in filters: parts.append(f"under {format_price(filters['max_price'])}")
        criteria_str = " ".join(parts)
        return f"Apologies, but I couldn't find any properties matching your criteria ({criteria_str}). You may want to adjust your budget or search in a different area."

    count = len(results_df)
    city = filters.get('city', results_df['city'].iloc[0])
    top_localities = results_df['locality'].value_counts().nlargest(3).index.tolist()
    
    summary = f"I found **{count} {'property' if count == 1 else 'properties'}** in **{city}** matching your request. "
    
    if top_localities:
        summary += f"The top localities for these listings are **{', '.join(top_localities)}**."
        
    return summary

def display_property_cards(results_df: pd.DataFrame):
    """
    Displays property details using Streamlit's native components.
    """
    if results_df.empty:
        return

    st.subheader("Top Matches:")
    
    for _, row in results_df.head(MAX_RESULTS_TO_DISPLAY).iterrows():
        with st.container(border=True):
            st.markdown(f"**{row['projectName']}**")
            st.caption(f"📍 {row['locality']}, {row['city']}")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Price**\n\n{format_price(row['price'])}")
            with col2:
                st.markdown(f"**Configuration**\n\n🏠 {row['bhk']}")
            with col3:
                status = row['status'].replace('_', ' ').title()
                st.markdown(f"**Status**\n\n{status}")

            st.divider()

            details_list = []
            if pd.notna(row.get('carpetArea')):
                details_list.append(f"📐 {int(row['carpetArea'])} sq.ft")
            if pd.notna(row.get('bathrooms')):
                details_list.append(f"🛁 {row['bathrooms']} Baths")
            if pd.notna(row.get('parkingType')):
                details_list.append(f"🅿️ {row['parkingType']}")
            
            if details_list:
                st.markdown(" | ".join(details_list))

            if row['status'] == 'READY_TO_MOVE':
                possession_info = "Ready for Possession"
            elif pd.notna(row.get('possessionDate')):
                possession_info = f"Possession by {row['possessionDate']}"
            else:
                possession_info = "Under Construction"
                
            st.success(f"🔑 **Possession:** {possession_info}")

def generate_text_for_history(results_df: pd.DataFrame) -> str:
    """Generates a simple text-only version of the results for chat history."""
    if results_df.empty:
        return ""
    
    text_cards = []
    for _, row in results_df.head(MAX_RESULTS_TO_DISPLAY).iterrows():
        card = (
            f"**{row['projectName']}**\n"
            f"- Location: {row['locality']}, {row['city']}\n"
            f"- Type: {row['bhk']}\n"
            f"- Price: {format_price(row['price'])}"
        )
        text_cards.append(card)
    
    return "\n\n---\n\n".join(text_cards)