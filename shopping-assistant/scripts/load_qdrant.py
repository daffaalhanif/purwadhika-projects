import pandas as pd 
import numpy as np
from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document
from uuid import uuid4
from shopping_assistant.config import *
from tqdm import tqdm

DATA_PATH = "data/amazon_products.csv"

def load_qdrant():
    df = pd.read_csv(DATA_PATH)

    # convert categories ke dalam bentuk list
    df['category'] = df['category'].apply(lambda x: x.split('|') if isinstance(x, str) else [])

    # buat list of document 
    documents = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Turning products into documents..."):
        doc = Document(
            page_content=row["about_product"],
            metadata={
                "id": row["product_id"],
                "name": row["product_name"],
                "discounted_price": row["discounted_price"],
                "actual_price": row["actual_price"],
                "discount_percentage": row["discount_percentage"],
                "category": row["category"],
            }
        )
        documents.append(doc)

    QdrantVectorStore.from_documents(
        embedding=embeddings, 
        documents=documents, 
        collection_name="amazon_products",
        prefer_grpc=True,
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY
    )

    print(f"Berhasil load {len(documents)} produk ke Qdrant!")
    
if __name__ == "__main__":
    load_qdrant()