# Agentic Finance Engine

An autonomous hybrid RAG system designed for deep analysis of financial 10-K filings. This engine leverages agentic workflows to retrieve unstructured text and perform precise quantitative analysis on structured financial tables (CSVs) extracted from SEC filings.

## 🚀 Key Features

* **Hybrid RAG Architecture**: Combines dense vector retrieval (ChromaDB) with sparse keyword search to handle complex financial queries.
* **Agentic Data Analysis**: Custom LangChain tools that bypass standard RAG limitations to directly analyze and calculate metrics from raw CSV financial tables.
* **Dual Interface**:
    * **Backend**: High-performance FastAPI server for ingestion and reasoning.
    * **Frontend**: Interactive Streamlit dashboard for real-time querying and visualization.
* **Modern Tooling**: Built with `uv` for lightning-fast dependency management and Python 3.12+.

## 🛠️ Tech Stack

* **Orchestration**: LangChain, LangGraph
* **LLM**: OpenAI GPT-4o-mini
* **Vector Store**: ChromaDB
* **Backend**: FastAPI, Uvicorn
* **Frontend**: Streamlit
* **Data Processing**: Pandas, Unstructured
* **Package Manager**: uv

## ⚡ Quick Start

Follow these steps to get the engine running on your local machine.

### 1. Prerequisites
Ensure you have [uv](https://github.com/astral-sh/uv) installed (a modern, extremely fast Python package manager).

```bash
# On macOS/Linux
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh

# On Windows (PowerShell)
powershell -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"

```

### 2. Clone the Repository

```bash
git clone [https://github.com/abheesht-ml/Agentic-Finance-Engine.git](https://github.com/abheesht-ml/Agentic-Finance-Engine.git)
cd Agentic-Finance-Engine

```

### 3. Environment Configuration

You must create a `.env` file to store your API keys.

1. Create the file in the root directory:
```bash
touch .env

```


2. Open the file in your text editor and add your OpenAI API Key:
```env
OPENAI_API_KEY=sk-your-key-here

```



### 4. Install Dependencies

Initialize the project and install all required packages:

```bash
uv sync

```

### 5. Run the Engine

Use the unified launcher to start both the FastAPI backend and Streamlit frontend simultaneously:

```bash
uv run python start.py

```

Once running, access the interfaces at:

* **Frontend Dashboard**: [http://localhost:8501](https://www.google.com/search?q=http://localhost:8501)
* **Backend API Docs**: [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)

## 📂 Project Structure

```text
├── src/
│   ├── app.py            # Streamlit frontend application
│   ├── server.py         # FastAPI backend server
│   ├── tools.py          # Agent tools for CSV/Financial analysis
│   ├── ingestion.py      # RAG pipeline and document processing
│   ├── graph.py          # LangGraph state management
│   ├── database.py       # Vector store connection logic
│   └── input_schemas.py  # Pydantic models for API validation
├── start.py              # Unified launcher for Backend & Frontend
├── pyproject.toml        # Project dependencies
├── uv.lock               # Dependency lock file
└── .env                  # Environment configuration (not committed)

```

## 🧠 Architecture Overview

1. **Ingestion**: The system scrapes and processes 10-K filings, separating narrative text from financial tables.
2. **Indexing**: Text chunks are embedded into ChromaDB; tables are stored as raw CSVs for precise calculation.
3. **Retrieval**: A router determines if the query requires semantic context (RAG) or quantitative analysis (Tools).
4. **Execution**:
* *Text Query*: Retrieves top-k chunks and synthesizes an answer.
* *Math Query*: The Agent loads specific CSVs into a Python environment to perform deterministic calculations (e.g., "Calculate YoY Net Sales growth").

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.
