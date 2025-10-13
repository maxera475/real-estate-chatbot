# 🏘️ AI-Powered Property Finder Chatbot

An intelligent, conversational chat interface built with Streamlit to help users discover real estate properties using natural language queries.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-brightgreen.svg)](https://streamlit.io)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-blue.svg)](https://pandas.pydata.org/)

This project replaces traditional filter-based search with a GPT-like chat interface. Users can ask questions like *"Show me 2BHK flats in Pune under 1 Cr"* and receive a helpful summary along with a list of relevant properties from a local dataset.

---

## 🚀 Key Features

-   **Natural Language Understanding:** Parses user queries to extract key filters like BHK, city, budget, and status.
-   **Data-Driven Responses:** Searches a provided CSV dataset to find matching properties.
-   **Dynamic Summaries:** Generates a concise, data-grounded summary of the search results.
-   **Interactive UI:** A clean and intuitive chat interface built with Streamlit's native components.
-   **Modular & Scalable:** The code is organized into a professional, "industrial-level" structure, making it easy to maintain and extend.

---

## 📂 Project Structure
The project is organized into a modular structure for clarity and scalability.

'''


real-estate-chatbot/
│
├── data/
│   ├── project.csv                   # Core project details like name and status.
│   ├── ProjectAddress.csv            # Address information for each project.
│   ├── ProjectConfiguration.csv      # Details on property configurations (e.g., BHK).
│   └── ProjectConfigurationVariant.csv # Specific variants with price, area, etc.
│
├── src/
│   ├── init.py                   # Makes the 'src' directory a Python package.
│   ├── config.py                     # Manages file paths and project constants.
│   ├── data_loader.py                # Module for loading and merging all CSV data.
│   ├── query_parser.py               # Handles natural language understanding and filter extraction.
│   ├── response_generator.py         # Creates the summary and property cards for the UI.
│   ├── search_engine.py              # Contains the core logic for filtering properties.
│   └── utils.py                      # Utility functions (e.g., price formatting).
│
├── app.py                            # The main Streamlit application file to be executed.
│
├── requirements.txt                  # A list of all required Python packages for the project.
│
└── README.md                         # This file.



'''                      
---

## 🛠️ Setup and Installation

Follow these steps to set up the project on your local machine.

### Prerequisites

-   Python 3.9 or higher
-   `pip` (Python package installer)

### Installation Steps

1.  **Clone the Repository:**
    ```sh
    git clone [https://github.com/maxera475/real_estate_chatbot.git]
    cd real-estate-chatbot
    ```

2.  **Install Dependencies:**
    Install all the required Python libraries using the `requirements.txt` file.
    ```sh
    pip install -r requirements.txt
    ```

---

## ▶️ How to Run

Once the setup is complete, you can run the Streamlit application with a single command.

1.  **Navigate to the project's root directory** in your terminal.

2.  **Run the following command:**
    ```sh
    streamlit run app.py
    ```

3.  Your web browser should automatically open with the chatbot interface running.

---

## 💬 Example Queries

Here are a few examples of queries you can try:

-   `2bhk in pune under 80 lakh`
-   `ready to move 3bhk in mumbai`
-   `properties in pune for 2 cr`
-   `1bhk in chembur`