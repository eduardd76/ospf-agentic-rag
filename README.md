# 🧠 OSPF Troubleshooting AI Agent (LangGraph + Chainlit)

This is a practical AI-powered troubleshooting assistant for OSPF (Open Shortest Path First) networking issues, built with:

- 🔗 LangGraph for agent orchestration
- 🤖 OpenAI GPT-4 for log analysis, diagnosis, and CLI generation
- 💬 Chainlit for an interactive UI
- 🧠 FAISS vector database for protocol knowledge
- 📚 A curated expert-level OSPF troubleshooting guide as the knowledge base

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/ospf-agentic-rag.git
cd ospf-agentic-rag
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # On Linux/macOS
venv\Scripts\activate.bat       # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application with Chainlit
```bash
chainlit run main.py
```

This will launch a local web UI where you can interact with the OSPF AI agent.

---

## 🧪 Sample OSPF Log

Paste the following into the app for testing:

```text
%OSPF-5-ADJCHG: Process 1, Nbr 10.0.0.2 on Gi0/0 from EXSTART to DOWN, Neighbor Down: MTU mismatch detected
```

The agent will:
- Detect the OSPF issue
- Retrieve protocol knowledge
- Diagnose root cause and impact
- Suggest CLI commands
- Validate the fix

---

## 📚 Knowledge Base

The OSPF knowledge base lives in:

```
knowledge_base/ospf_troubleshooting.txt
```

You can add more entries for other issues like:
- Authentication mismatch
- Hello/Dead interval mismatch
- Area type conflicts
- Network type mismatches

---

## 🛠 Extending the App

Ideas to expand this project:

| Feature | Description |
|---------|-------------|
| 🔄 Add BGP, EIGRP     | Extend troubleshooting for other protocols |
| 🧰 Local LLM          | Use Llama.cpp or GPT4All with LangChain |
| 📦 Containerization   | Deploy in Docker or on Kubernetes |
| 🔌 Kafka integration  | Real-time log ingestion for NOC environments |
| 🤝 REST API mode      | Make the app callable from other systems |

---

## 👤 About the Author

Created by [Eduard Dulharu](https://www.linkedin.com/in/eduarddulharu)  
Senior Network Architect | AI in Networking Advocate | CTO @ Brilu

---

## 📄 License

MIT License
