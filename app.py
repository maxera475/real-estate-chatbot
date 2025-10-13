import streamlit as st
from src.data_loader import DataLoader
from src import query_parser, search_engine, response_generator


st.set_page_config(page_title="Intelligent Property Finder", page_icon="🏘️", layout="wide")


st.title("Intelligent Property Finder")


@st.cache_resource
def load_data():
    """Loads data using the DataLoader class."""
    loader = DataLoader()
    return loader.get_data()

master_df = load_data()


if master_df is not None:
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How can I help you find your dream property today?"}]

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("What are you looking for?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your query and searching our database..."):
                # 1. Parse and search
                filters = query_parser.parse_query(prompt)
                results_df = search_engine.search_properties(master_df, filters)
                
                # 2. Generate summary
                summary = response_generator.generate_summary(results_df, filters)
                st.markdown(summary)
                
                # 3. Directly display cards using native Streamlit components
                response_generator.display_property_cards(results_df)

                # 4. Create a text-only version for chat history
                history_text = summary + "\n" + response_generator.generate_text_for_history(results_df)
                st.session_state.messages.append({"role": "assistant", "content": history_text})
else:
    st.error("The property database could not be loaded. Please ensure the data files are present and correctly formatted.")