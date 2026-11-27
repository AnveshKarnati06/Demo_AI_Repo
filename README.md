# Enterprise IT Service Assistant

An AI-powered Enterprise IT Service Assistant that helps users retrieve IT knowledge, answer support questions, and draft incident reports using Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs).

## Features

- AI-powered IT support assistant
- Retrieval-Augmented Generation (RAG)
- Knowledge base search from enterprise documents
- Context-aware responses
- Source-cited answers
- Incident draft generation
- Human review workflow for incidents
- Local LLM support through Ollama
- User-friendly web interface with Streamlit

## Project Architecture

```
User Query
    │
    ▼
Streamlit UI
    │
    ▼
RAG Pipeline
    │
 ┌──┴──┐
 │      │
 ▼      ▼
Vector DB   Enterprise Documents
 │
 ▼
Retriever
 │
 ▼
LLM (Ollama)
 │
 ▼
Response + Sources
```

## Technologies Used

- Python 3.11+
- Streamlit
- LangChain
- Ollama
- ChromaDB / Vector Store
- HuggingFace Embeddings
- Retrieval-Augmented Generation (RAG)
- Git & GitHub

## Project Structure

```text
Enterprise_IT_Service_Assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── data/
├── src/
├── embeddings/
├── vectorstore/
├── assets/
└── .gitignore
```

## Installation

### Clone Repository

```bash
git clone https://github.com/AnveshKarnati06/Demo_AI_Repo.git
cd Enterprise_IT_Service_Assistant
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows

```powershell
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
streamlit run app.py
```

## Sample Use Cases

### Knowledge Retrieval

- Password reset procedures
- VPN troubleshooting
- Software installation guidance
- IT policy lookup

### Incident Management

- Generate incident drafts
- Summarize reported issues
- Recommend resolution steps
- Route incidents for review

## Key Learning Outcomes

- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)
- Prompt Engineering
- Vector Databases
- Embedding Models
- Enterprise AI Applications
- Streamlit Development
- Git & GitHub Workflow

## Future Enhancements

- Multi-agent architecture
- Microsoft Teams integration
- ServiceNow integration
- Ticket tracking dashboard
- Role-based authentication
- Knowledge base auto-sync

## Disclaimer

This project is developed for learning and internship purposes. Generated incident reports are drafts and should be reviewed by authorized personnel before submission.

## Author

**Anvesh Karnati**

AI/ML Intern

GitHub: https://github.com/AnveshKarnati06