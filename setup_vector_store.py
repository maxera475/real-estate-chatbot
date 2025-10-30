# setup_vector_store.py
import pandas as pd
import logging
from llama_index.core import Document, VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from src.data_loader import DataLoader
import chromadb

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def create_property_document(row):
    """Creates a text document for a single property row."""
    # Combine all relevant data into a natural language description
    details = f"""
    Project Name: {row['projectName']}
    Location: {row['locality']}, {row['city']}
    Configuration: {row['bhk']}
    Price: {row.get('price', 'N/A')}
    Status: {row.get('status', 'N/A')}
    Carpet Area: {row.get('carpetArea', 'N/A')} sq.ft
    Bathrooms: {row.get('bathrooms', 'N/A')}
    Possession Date: {row.get('possessionDate', 'N/A')}
    Parking: {row.get('parkingType', 'N/A')}
    """
    return Document(text=details, metadata={"projectId": row.get('slug', 'N/A')})

def main():
    logging.info("Starting data loading...")
    # 1. Load the master DataFrame
    loader = DataLoader()
    master_df = loader.get_data()
    
    if master_df is None or master_df.empty:
        logging.error("Failed to load data. Exiting.")
        return

    logging.info(f"Loaded {len(master_df)} property records.")
    
    # 2. Convert DataFrame rows to Llama-Index Document objects
    documents = [create_property_document(row) for _, row in master_df.iterrows()]
    
    # 3. Initialize ChromaDB (the vector database)
    # This will create a 'chroma_db' folder to store the index
    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("property_index")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # 4. Initialize the Embedding Model
    # This runs locally to convert your text into vectors
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    
    logging.info("Creating and persisting vector index. This may take a few minutes...")
    
    # 5. Create and save the index
    VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model,
        show_progress=True
    )
    
    logging.info("Vector store created and persisted successfully in the 'chroma_db' folder.")

if __name__ == "__main__":
    main()