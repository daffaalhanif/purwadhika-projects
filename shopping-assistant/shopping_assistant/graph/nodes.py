from shopping_assistant.dummy_data import *

from .state import State
from shopping_assistant.config import *

from datetime import datetime

from shopping_assistant.utils.retriever import retrieve_documents


def filter_agent(state: State):
    """
    Node ini mengklasifikasikan intent pertanyaan user.
    Output: string 'product', 'promo', atau 'other'
    """
    question = state["messages"][0]  # pertanyaan asli user
    history  = state["history"]

    prompt = f"""
    Kamu adalah agent klasifikasi. Tugasmu adalah mengklasifikasikan pertanyaan pelanggan
    menjadi TEPAT SATU dari tiga kategori berikut: [product, promo, other].
    
    Aturan:
    - Jawab HANYA dengan kata: product, promo, atau other
    - Tanpa tanda baca, spasi tambahan, atau penjelasan apapun
    
    Contoh:
    - 'Berapa harga jaket?' -> product
    - 'Ada diskon hari ini?' -> promo
    - 'Toko buka jam berapa?' -> other
    
    chat history: {history}
    question: {question}
    """

    response = llm.invoke(prompt)
    return {"messages": [response]}

def product_agent(state: State):
    """
    Node ini menjawab pertanyaan seputar produk toko menggunakan RAG.

    Args:
        state (State): berisi 'messages' (percakapan) dan 'history' (konteks)

    Returns:
        dict: {"messages": [response]} berisi jawaban product agent

    PENTING: Ambil messages[0], yaitu pertanyaan ASLI user,
    bukan messages[-1] yang berisi output 'product' dari filter_agent.
    """
    question = state["messages"][0]
    history  = state["history"]

    # RAG: ambil produk relevan dari Qdrant
    results = retrieve_documents(
        collection_name="amazon_products",
        query=question.content,
        top_k=5
    )

    # DEBUG
    print("\n======================= PRODUK YANG DI-RETRIEVE =======================")
    for i, doc in enumerate(results, 1):
        print(f"{i}. {doc.metadata.get('name', 'N/A')}")
    print("====================================================================\n")

    # Format jadi teks sederhana
    products_context = "\n".join([
        f"- {doc.metadata['name']} | Harga: {doc.metadata['discounted_price']} | {doc.page_content[:150]}"
        for doc in results
    ])

    prompt = f"""Kamu adalah chatbot yang membantu pelanggan dalam percakapan tentang produk
    dari "Amazon Store". Jawab pertanyaan dengan ramah, sopan, dan persuasif dalam menawarkan
    barang kepada pelanggan. Gunakan chat history untuk menangkap konteks percakapan.
    
    {products_context}
    
    chat history: {history}
    question: {question}
    """

    response = llm.invoke(prompt)
    return {"messages": [response]}

def promo_agent(state: State):
    """
    Node ini menjawab pertanyaan seputar promo toko.
    """
    question = state["messages"][0]
    history  = state["history"]
    day = datetime.now().strftime("%A") 

    prompt = f"""
    Kamu adalah chatbot yang membantu pelanggan dalam percakapan tentang promo
    yang ditawarkan oleh "Amazon Store" sesuai dengan hari. Jawab dengan ramah dan sopan.
    Gunakan chat history untuk menangkap konteks percakapan.
    
    {PROMOS}

    hari: {day}
    chat history: {history}
    question: {question}
    """

    response = llm.invoke(prompt)
    return {"messages": [response]}

def basic_agent(state: State):
    """
    Node ini menjawab pertanyaan umum yang tidak masuk kategori
    produk atau promo.
    """
    question = state["messages"][0]
    history  = state["history"]

    prompt = f"""
    Kamu adalah chatbot "Amazon Store" yang akan membantu menjawab
    pertanyaan pelanggan. Jawab pertanyaan dengan ramah dan sopan.
    Gunakan chat history untuk menangkap konteks percakapan.
    
    chat history: {history}
    question: {question}
    """

    response = llm.invoke(prompt)
    return {"messages": [response]}

# buat test untuk memastikan semua agent dapat bekerja dengan benar 
if __name__ == "__main__":
    # Simulasi state awal dengan pertanyaan user
    state = State(messages=["Apakah ada diskon untuk jaket?"], history=["Percakapan dimulai."])
    
    # Uji filter_agent
    filter_output = filter_agent(state)
    print("Filter Agent Output:", filter_output["messages"][0].content)
    
    # Uji product_agent
    product_output = product_agent(state)
    print("Product Agent Output:", product_output["messages"][0].content)
    
    # Uji promo_agent
    promo_output = promo_agent(state)
    print("Promo Agent Output:", promo_output["messages"][0].content)

    # Uji basic_agent
    basic_output = basic_agent(state)
    print("Basic Agent Output:", basic_output["messages"][0].content)