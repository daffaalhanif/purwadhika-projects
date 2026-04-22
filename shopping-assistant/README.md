# Shopping Assistant

A shopping chatbot built with **LangGraph** for **Amazon Store**. This chatbot uses a multi-agent architecture with automatic routing to answer questions about products, promotions, and general inquiries.

## Features

- **Multi-agent routing** - questions are automatically classified and routed to the appropriate agent (product, promo, or general)
- **Two output modes** - `invoke` for complete responses, `stream` for incremental output per node
- **Conversation memory** - retains up to 10 recent messages as context
- **Semantic search** - vector-based product search using Qdrant (optional)
- **Dynamic promotions** - promotions are automatically adjusted based on the day

## Architecture

```
User Input
    │
    ▼
┌─────────────┐
│ filter_agent│  → Classifies intent: product / promo / other
└──────┬──────┘
       │
  ┌────┴──────────────┐
  ▼         ▼         ▼
product   promo     basic
 agent    agent     agent
  │         │         │
  └────┬────┘─────────┘
       ▼
   Response
```

| Agent | Role |
|---|---|
| `filter_agent` | Classifies user questions into `product`, `promo`, or `other` |
| `product_agent` | Answers questions about available products in the store |
| `promo_agent` | Answers questions about current promotions |
| `basic_agent` | Answers general questions outside of products and promotions |

## Project Structure

```
shopping-assistant/
├── main.py                         # Application entry point
├── requirements.txt                # Project dependencies
├── pyproject.toml                  # Package configuration
├── data/
│   └── amazon_products.csv         # Amazon product dataset (for Qdrant)
├── scripts/
│   └── load_qdrant.py              # Script to load data into Qdrant
└── shopping_assistant/
    ├── __init__.py
    ├── config.py                   # LLM, embeddings, and Qdrant configuration
    ├── dummy_data/
    │   ├── products.py             # Dummy store product data
    │   └── promos.py               # Dummy daily promotion data
    ├── graph/
    │   ├── nodes.py                # All agent node definitions
    │   ├── state.py                # State definition (TypedDict)
    │   └── workflow.py             # Graph and routing logic definition
    └── utils/
        └── retriever.py            # Semantic search utility via Qdrant
```

## Prerequisites

- Python 3.10+
- [OpenAI API Key](https://platform.openai.com/api-keys)
- [Qdrant](https://qdrant.tech/) Cloud account *(optional, for semantic search)*

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/daffaalhanif/purwadhika-projects.git
cd purwadhika-projects/shopping-assistant
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### 4. Configure environment variables

Create a `.env` file inside the `shopping-assistant/` folder:

```bash
cp .env.example .env
```

Fill in the `.env` file with your credentials:

```env
OPENAI_API_KEY=sk-...

# Optional - only required if using Qdrant
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_URL=https://your-cluster.qdrant.io
```

## Running the App

```bash
python main.py
```

When launched, you will be prompted to select an output mode:

```
============================================================
Select chatbot mode (invoke/stream) [default invoke]:
============================================================
🛍️  Welcome to Amazon Store!
    Type 'quit' / 'exit' / 'q' to exit.
============================================================
You: _
```

| Mode | Description |
|---|---|
| `invoke` | Displays the final response after all nodes have finished processing |
| `stream` | Displays output from each node incrementally along with routing info |

## Using Qdrant (Optional)

This feature enables semantic product search using the Amazon dataset.

### 1. Make sure Qdrant credentials are filled in `.env`

### 2. Load data into Qdrant

```bash
python scripts/load_qdrant.py
```

This script reads `data/amazon_products.csv`, converts each product into a vector document, and uploads it to the `amazon_products` collection in Qdrant.

### 3. Use the retriever in your code

```python
from shopping_assistant.utils.retriever import retrieve_documents

results = retrieve_documents(
    collection_name="amazon_products",
    query="affordable gaming laptop",
    top_k=5
)
```

## Example Conversation

```
You: what jackets do you have?
🔀 Routing to product agent
🤖 product_agent:
Hi! We have a great jacket collection priced at Rp399,000, ranging from
denim jackets, bombers, to windbreakers. Would you like me to help you
find one that suits your style? 😊

You: any promotions today?
🔀 Routing to promo agent
🤖 promo_agent:
Great news! Today is Friday, enjoy 30% off all products. Take advantage
of this promo now! 🎉

You: what time does the store close?
🔀 Routing to basic agent
🤖 basic_agent:
Our store is open every day from 09:00 to 21:00 WIB. Is there anything
else I can help you with? 😊
```

## Tech Stack

| Library | Purpose |
|---|---|
| [LangGraph](https://langchain-ai.github.io/langgraph/) | Multi-agent graph orchestration |
| [LangChain](https://python.langchain.com/) | LLM abstraction and tooling |
| [OpenAI GPT-4o-mini](https://platform.openai.com/) | Primary language model |
| [Qdrant](https://qdrant.tech/) | Vector database for semantic search |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Environment variable management |
