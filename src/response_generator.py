# src/response_generator.py

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
    Displays property details using Streamlit's native components,
    including st.metric for a more interesting design.
    """
    if results_df.empty:
        return

    st.subheader("Here are your top matches:")
    
    # Loop through the top N results
    for _, row in results_df.head(MAX_RESULTS_TO_DISPLAY).iterrows():
        # Use st.container to draw a bordered box for each card
        with st.container(border=True):
            
            # Row 1: Project Name and Location
            st.subheader(f"{row['projectName']}")
            st.caption(f"📍 {row['locality']}, {row['city']}")
            st.divider()

            # Row 2: Key Metrics
            # Use st.metric for a large, bold display of key info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Price", value=format_price(row['price']))
            with col2:
                st.metric(label="Configuration", value=row['bhk'])
            with col3:
                area = f"{int(row['carpetArea'])} sq.ft" if pd.notna(row.get('carpetArea')) else "N/A"
                st.metric(label="Carpet Area", value=area)

            st.divider()
            
            # Row 3: Other Details and Possession Status
            col1, col2 = st.columns([1.5, 1]) # Make first column wider

            with col1:
                # Build a list of other amenities
                details_list = []
                if pd.notna(row.get('bathrooms')):
                    details_list.append(f"**Bathrooms:** {row['bathrooms']} 🛁")
                if pd.notna(row.get('parkingType')):
                    details_list.append(f"**Parking:** {row['parkingType']} 🅿️")
                
                if details_list:
                    st.markdown("  \n".join(details_list))
                else:
                    st.markdown("More details available upon request.")

            with col2:
                # Use st.success or st.warning for visual status
                if row['status'] == 'READY_TO_MOVE':
                    st.success("🔑 Ready for Possession")
                elif pd.notna(row.get('possessionDate')):
                    st.warning(f"🔑 Possession by {row['possessionDate']}")
                else:
                    st.warning("🔑 Under Construction")

def generate_text_for_history(results_df: pd.DataFrame) -> str:
    """Generates a simple text-only version of the results for chat history."""
    if results_df.empty:
        return ""
    
    text_cards = []
    # Loop through the results and create a simple formatted string for each.
    for _, row in results_df.head(MAX_RESULTS_TO_DISPLAY).iterrows():
        card = (
            f"**{row['projectName']}**\n"
            f"- Location: {row['locality']}, {row['city']}\n"
            f"- Type: {row['bhk']}\n"
            f"- Price: {format_price(row['price'])}"
        )
        text_cards.append(card)
    
    # Join all the text cards together with a separator.
    return "\n\n---\n\n".join(text_cards)