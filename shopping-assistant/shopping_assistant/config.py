from dotenv import load_dotenv
import os 

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
)

qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

class QdrantLoader(QdrantVectorStore):
    def __init__(self, collection_name: str):
        super().__init__(
            client=qdrant_client,
            collection_name=collection_name,
            embedding=embeddings,
        )