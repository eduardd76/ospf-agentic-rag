# 🧠 OSPF Troubleshooting Agent (LangGraph + Chainlit)

Un agent AI pentru diagnosticarea problemelor OSPF folosind:
- ✅ LangGraph (flow logic)
- ✅ LLM (GPT-4) pentru reasoning și CLI
- ✅ Chainlit UI pentru interacțiune live
- ✅ FAISS + knowledge base Cisco-like

---

## 🚀 Cum rulezi local

### 1. Clonează repo-ul
```bash
git clone https://github.com/<your-username>/ospf-agentic-rag.git
cd ospf-agentic-rag
```

### 2. Creează mediu virtual și instalează dependențele
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate.bat
pip install -r requirements.txt
```

### 3. Rulează aplicația
```bash
chainlit run main.py
```

---

## 🔍 Exemplu de log OSPF

```text
%OSPF-5-ADJCHG: Process 1, Nbr 10.0.0.2 on Gi0/0 from EXSTART to DOWN, Neighbor Down: MTU mismatch detected
```

---

## 📚 Knowledge Base

Editabil în: `knowledge_base/ospf_troubleshooting.txt`  
Include cazuri: MTU mismatch, authentication mismatch, timer issues, area problems, etc.

---

## 🛠 Pentru Extindere

- Adaugă BGP în KB + rules în `graph.py`
- Înlocuiește OpenAI cu LLM local via LangChain
- Rulează Chainlit ca API REST (dacă vrei CI/CD)

---

## ✨ Creat de [@eduarddulharu](https://www.linkedin.com/in/eduarddulharu)
