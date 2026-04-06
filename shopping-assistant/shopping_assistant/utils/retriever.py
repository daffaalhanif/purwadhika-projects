from langchain_qdrant import QdrantVectorStore
from shopping_assistant.config import *


def retrieve_documents(collection_name: str, query: str, top_k: int = 5):
    qdrant_loader = QdrantLoader(collection_name=collection_name)
    results = qdrant_loader.similarity_search(query=query, k=top_k)
    return results

if __name__ == "__main__":
    # collection_name = "amazon_products"
    # query = "laptop gaming dengan harga terjangkau"
    # results = retrieve_documents(collection_name, query)

    # print(f"Hasil pencarian untuk query: '{query}'\n")
    # for idx, doc in enumerate(results, 1):
    #     print(f"{idx}. {doc.metadata['name']} - Harga Diskon: {doc.metadata['discounted_price']} (Diskon: {doc.metadata['discount_percentage']}%)")
    #     print(f"   Deskripsi: {doc.page_content[:100]}...")  
    #     print()
    from langchain_core.messages import SystemMessage, HumanMessage
    query = "Saya mau cari laptop gaming dengan harga terjangkau, ada rekomendasi?"
    results = retrieve_documents(collection_name="amazon_products",
                                  query=query)
    
    system_prompt = SystemMessage(
        f"""
        Kamu adalah asisten belanja yang membantu pengguna menemukan produk yang mereka cari.
        Berdasarkan query pengguna, berikut adalah beberapa produk yang relevan:
        {results}
        """
    )

    user_message = HumanMessage(query)

    response = llm.invoke([
        system_prompt,
        user_message
    ])

    print(response.content)