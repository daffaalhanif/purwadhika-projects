from typing import Annotated
from typing_extensions import TypedDict 
from langgraph.graph.message import add_messages 

class State(TypedDict):
    """
    State adalah TypedDict yang digunakan untuk menyimpan dan berbagi informasi antar node dalam graph.
    State dapat berisi berbagai informasi seperti histori percakapan, profil pengguna, atau data lain yang relevan dengan konteks percakapan.
    """
    messages: Annotated[list, add_messages]
    history: list

# Buat test untuk memastikan State dapat menyimpan dan berbagi informasi dengan benar
if __name__ == "__main__":
    # Contoh penggunaan State
    state = State(messages=[], history=[])
    
    # Tambahkan pesan ke state
    state['messages'].append("Halo, bagaimana kabarmu?")
    state['history'].append("Percakapan dimulai.")
    
    # Tampilkan isi state
    print("Messages:", state['messages'])
    print("History:", state['history'])