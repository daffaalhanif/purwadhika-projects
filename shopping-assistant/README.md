# 🛍️ Shopping Assistant

Chatbot asisten belanja berbasis **LangGraph** untuk **Toko Pakaian Purwadhika**. Chatbot ini menggunakan arsitektur multi-agent dengan routing otomatis untuk menjawab pertanyaan seputar produk, promo, maupun pertanyaan umum.

## Fitur

- **Multi-agent routing** — pertanyaan diklasifikasikan secara otomatis ke agent yang tepat (produk, promo, atau umum)
- **Dua mode output** — `invoke` untuk respons penuh sekaligus, `stream` untuk output bertahap per node
- **Memori percakapan** — menyimpan hingga 10 pesan terakhir sebagai konteks
- **Semantic search** — pencarian produk berbasis vektor menggunakan Qdrant (opsional)
- **Promo dinamis** — promo disesuaikan otomatis berdasarkan hari

## Arsitektur

```
User Input
    │
    ▼
┌─────────────┐
│ filter_agent│  → Mengklasifikasikan intent: product / promo / other
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

| Agent | Tugas |
|---|---|
| `filter_agent` | Mengklasifikasikan pertanyaan user menjadi `product`, `promo`, atau `other` |
| `product_agent` | Menjawab pertanyaan seputar produk yang tersedia di toko |
| `promo_agent` | Menjawab pertanyaan seputar promo yang berlaku hari ini |
| `basic_agent` | Menjawab pertanyaan umum di luar topik produk dan promo |

## Struktur Project

```
shopping-assistant/
├── main.py                         # Entry point aplikasi
├── requirements.txt                # Dependensi project
├── pyproject.toml                  # Konfigurasi package
├── data/
│   └── amazon_products.csv         # Dataset produk Amazon (untuk Qdrant)
├── scripts/
│   └── load_qdrant.py              # Script untuk load data ke Qdrant
└── shopping_assistant/
    ├── __init__.py
    ├── config.py                   # Konfigurasi LLM, embeddings, dan Qdrant
    ├── dummy_data/
    │   ├── products.py             # Data dummy produk toko
    │   └── promos.py               # Data dummy promo harian
    ├── graph/
    │   ├── nodes.py                # Definisi semua agent node
    │   ├── state.py                # Definisi State (TypedDict)
    │   └── workflow.py             # Definisi graph dan routing logic
    └── utils/
        └── retriever.py            # Utility semantic search via Qdrant
```

## Prasyarat

- Python 3.10+
- [OpenAI API Key](https://platform.openai.com/api-keys)
- [Qdrant](https://qdrant.tech/) Cloud account *(opsional, untuk semantic search)*

## Instalasi

### 1. Clone repository

```bash
git clone https://github.com/nadifwahdi/purwadhika-repo.git
cd purwadhika-repo/shopping-assistant
```

### 2. Buat dan aktifkan virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependensi

```bash
pip install -r requirements.txt
pip install -e .
```

### 4. Konfigurasi environment variables

Buat file `.env` di dalam folder `shopping-assistant/`:

```bash
cp .env.example .env
```

Isi file `.env` dengan kredensial kamu:

```env
OPENAI_API_KEY=sk-...

# Opsional — hanya diperlukan jika menggunakan Qdrant
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_URL=https://your-cluster.qdrant.io
```

## Menjalankan Aplikasi

```bash
python main.py
```

Saat dijalankan, kamu akan diminta memilih mode output:

```
============================================================
Pilih mode chatbot (invoke/stream) [default invoke]:
============================================================
🛍️  Selamat datang di Toko Pakaian Purwadhika!
   Ketik 'quit' / 'exit' / 'q' untuk keluar.
============================================================
Anda: _
```

| Mode | Deskripsi |
|---|---|
| `invoke` | Menampilkan respons final setelah semua node selesai diproses |
| `stream` | Menampilkan output setiap node secara bertahap beserta info routing |

## Penggunaan Qdrant (Opsional)

Fitur ini memungkinkan pencarian produk secara semantik menggunakan dataset Amazon.

### 1. Pastikan kredensial Qdrant sudah diisi di `.env`

### 2. Load data ke Qdrant

```bash
python scripts/load_qdrant.py
```

Script ini akan membaca `data/amazon_products.csv`, mengubah setiap produk menjadi dokumen vektor, dan meng-upload-nya ke koleksi `amazon_products` di Qdrant.

### 3. Gunakan retriever di kode kamu

```python
from shopping_assistant.utils.retriever import retrieve_documents

results = retrieve_documents(
    collection_name="amazon_products",
    query="laptop gaming dengan harga terjangkau",
    top_k=5
)
```

## Contoh Percakapan

```
Anda: ada jaket apa saja?
🔀 Routing ke agent product
🤖 product_agent:
Halo! Kami punya koleksi jaket keren dengan harga Rp399.000, mulai dari
jaket denim, bomber, hingga windbreaker. Mau saya bantu pilihkan yang
sesuai selera kamu? 😊

Anda: ada promo hari ini?
🔀 Routing ke agent promo
🤖 promo_agent:
Selamat! Hari ini Jumat, ada diskon 30% untuk semua produk. Yuk,
manfaatkan promo ini sekarang! 🎉

Anda: toko buka sampai jam berapa?
🔀 Routing ke agent basic
🤖 basic_agent:
Toko kami buka setiap hari pukul 09.00–21.00 WIB. Ada yang bisa
saya bantu lagi? 😊
```

## Teknologi yang Digunakan

| Library | Fungsi |
|---|---|
| [LangGraph](https://langchain-ai.github.io/langgraph/) | Orkestrasi multi-agent graph |
| [LangChain](https://python.langchain.com/) | Abstraksi LLM dan tooling |
| [OpenAI GPT-4o-mini](https://platform.openai.com/) | Model bahasa utama |
| [Qdrant](https://qdrant.tech/) | Vector database untuk semantic search |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Manajemen environment variables |