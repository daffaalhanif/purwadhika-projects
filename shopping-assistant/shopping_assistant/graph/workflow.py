from typing import Literal
from langgraph.graph import StateGraph,START,END
from .nodes import *
from .state import State

def classify_flow(state: State) -> Literal["product_agent", "promo_agent", "basic_agent"]:
    """
    Fungsi routing: membaca output filter agent dan menentukan node mana yang akan dijalankan selanjutnya.
    Return type harus berupa string yang valid.
    """
    classification = state["messages"][-1].content.strip().lower()
    if classification == "product":
        return "product_agent"
    elif classification == "promo":
        return "promo_agent"
    else:
        return "basic_agent"

class ShoppingAssistantGraph(StateGraph):
    def __init__(self):
        super().__init__(State)
        self.add_node("filter_agent", filter_agent)
        self.add_node("product_agent", product_agent)
        self.add_node("promo_agent", promo_agent)
        self.add_node("basic_agent", basic_agent)
        self.add_edge(START, "filter_agent")
        self.add_conditional_edges("filter_agent", classify_flow)
        self.add_edge("product_agent", END)
        self.add_edge("promo_agent", END)
        self.add_edge("basic_agent", END)
    

# Buat test untuk memastikan workflow berjalan dengan benar
if __name__ == "__main__":
    graph = ShoppingAssistantGraph()
    app = graph.compile()

    history_invoke = []

    # test dengan invoke
    print("=" * 60 + "\nTesting invoke method\n" + "=" * 60)
    result = app.invoke({
        "messages": [
            {"role": "user", "content": "ada promo apa?"}
        ],
        "history": history_invoke,
    })

    print(result["messages"][-1].content)

    history_invoke.append(f"User: ada promo apa?")
    history_invoke.append(f"Chatbot: {result['messages'][-1].content}")
    
    # test dengan stream 
    print("=" * 60 + "\nTesting stream method\n" + "=" * 60)

    history_stream = []

    for output in app.stream({
        "messages": [
            {"role": "user", "content": "ada promo apa saja?"}
        ],
        "history": history_stream,
        }):
        
        for key,value in output.items():
            if key == "filter_agent":
                next_agent = value["messages"][0].content.strip().lower()
                print(f"🧠 Filter agent memutuskan untuk menjalankan node: {next_agent}_agent")
            else:
                print(f"🤖 {key}_agent:\n{value['messages'][0].content}")
                
                history_stream.append(f"User: ada promo apa saja?")
                history_stream.append(f"Chatbot: {value['messages'][0].content}")

