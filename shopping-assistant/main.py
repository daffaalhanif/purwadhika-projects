from shopping_assistant.graph import ShoppingAssistantGraph
from langgraph.graph import StateGraph


def chatbot_invoke(graph: StateGraph):
    app = graph.compile()
    history = []

    while True:
        user_input = input("Anda: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Terima kasih telah berkunjung! Sampai jumpa lagi!")
            break

        result = app.invoke({
            "messages": [
                {"role": "user", "content": user_input}
            ],
            "history": history,
        })

        print("Chatbot:", result["messages"][-1].content)

        # mengupdate context dengan history percakapan terbaru
        history.append(f"User: {user_input}")
        history.append(f"Chatbot: {result['messages'][-1].content}")

        if len(history) > 10:
            history = history[-10:]  # simpan hanya 10 pesan terakhir untuk konteks

def chatbot_stream(graph: StateGraph):
    app = graph.compile()
    history = []

    while True:
        user_input = input("Anda: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Terima kasih telah berkunjung! Sampai jumpa lagi!")
            break

        for output in app.stream({
            "messages": [
                {"role": "user", "content": user_input},
            ],
            "history": history,
        }):
            for key, value in output.items():
                if key == "filter_agent":
                    next_agent = value["messages"][0].content.strip().lower()
                    if next_agent not in ["product", "promo"]:
                        next_agent = "basic"
                    print(f"🔀 Routing ke agent {next_agent}")
                else:
                    print(f"🤖 {key}:\n{value['messages'][0].content}")

                    # mengupdate context dengan history percakapan terbaru
                    history.append(f"User: {user_input}")
                    history.append(f"Chatbot: {value['messages'][0].content}")
                    
                    if len(history) > 10:
                        history = history[-10:]  # simpan hanya 10 pesan terakhir untuk konteks

if __name__ == "__main__":
    graph = ShoppingAssistantGraph()

    # Pilih mode chatbot: invoke atau stream
    print("=" * 60)
    mode = input("Pilih mode chatbot (invoke/stream) [default invoke]: ").strip().lower()
    print("=" * 60)

    print("🛍️  Selamat datang di Amazon Store!")
    print("   Ketik 'quit' / 'exit' / 'q' untuk keluar.")
    print("=" * 60)
    if mode == "stream":
        chatbot_stream(graph)
    else:
        chatbot_invoke(graph)


