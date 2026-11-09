# Enterprise CTMS Copilot

> AI-Powered Clinical Trial Management System (CTMS) Copilot built using **FastAPI**, **LangChain**, **Multi-Agent AI**, **RAG**, **SQL Agent**, **ChromaDB**, and **MySQL**.

---

# Overview

Enterprise CTMS Copilot is an intelligent AI assistant designed for Clinical Trial Management Systems (CTMS). It enables clinical operations teams to ask natural language questions about clinical trials and receive accurate, context-aware responses by combining:

- Multi-Agent AI
- Retrieval Augmented Generation (RAG)
- SQL Database Querying
- Vector Search
- Large Language Models (LLMs)

The application supports multiple CTMS business modules including Trial Planning, Budget Management, Monitoring, Site Management, and Patient Recruitment.

---

# Features

## AI Capabilities

- Multi-Agent Architecture
- Supervisor Agent
- Retrieval Augmented Generation (RAG)
- SQL Agent
- Hybrid Search
- Conversation Memory
- Context-Aware Responses

---

## Clinical Trial Modules

- Trial Planning
- Budget Management
- Site Management
- Monitoring
- Patient Recruitment

---

## Technical Features

- FastAPI REST API
- LangChain Integration
- Chroma Vector Database
- MySQL Database
- HuggingFace Embeddings
- OpenAI Compatible LLM Support
- Logging with Loguru
- Modular Architecture

---

# Project Architecture

```
                        User
                         │
                         ▼
                Enterprise CTMS Copilot
                         │
                FastAPI REST API
                         │
             Enterprise Supervisor Agent
                         │
     ┌──────────────┬──────────────┬──────────────┐
     ▼              ▼              ▼              ▼
 Trial Agent    Budget Agent   Monitoring    Site Agent
                                         Recruitment Agent
     │
     ├──────────────┐
     ▼              ▼
 SQL Agent       RAG Agent
     │              │
 MySQL DB      Chroma Vector DB
```

---

# Technology Stack

| Category | Technology |
|-----------|------------|
| Backend | FastAPI |
| AI Framework | LangChain |
| Vector Database | ChromaDB |
| Database | MySQL |
| Embeddings | HuggingFace Sentence Transformers |
| LLM | OpenAI Compatible Models |
| Logging | Loguru |
| Validation | Pydantic |
| Deployment | Uvicorn |


# Supported AI Modules

| Module | Description |
|----------|-------------|
| auto | Automatic Agent Selection |
| trial_planning | Clinical Trial Planning |
| budget_management | Budget Analysis |
| monitoring | Monitoring Activities |
| site_management | Site Operations |
| patient_recruitment | Recruitment Analysis |

---

# API Endpoints

## Base URL

```
http://localhost:8000
```

---

## Enterprise Copilot

**POST**

```
/api/v1/ctms/copilot
```

### Sample Request

```json
{
  "question": "Show all active Phase III oncology trials.",
  "session_id": "session-001",
  "user_id": "john.doe",
  "role": "CRA",
  "module": "auto"
}
```

### Sample Response

```json
{
  "success": true,
  "answer": "There are 18 active Phase III oncology trials.",
  "agent": "Trial Planning Agent",
  "sources": [],
  "execution_time": 2.14
}
```

---

## Health Check

```
GET /api/v1/ctms/health
```

Response

```json
{
  "status":"UP",
  "service":"Enterprise CTMS Copilot"
}
```

---

## Available Modules

```
GET /api/v1/ctms/modules
```

---

## Registered Agents

```
GET /api/v1/ctms/agents
```

---

# Multi-Agent Workflow

```
User Question
      │
      ▼
Supervisor Agent
      │
      ├──────── Trial Agent
      ├──────── Budget Agent
      ├──────── Monitoring Agent
      ├──────── Site Agent
      └──────── Recruitment Agent
             │
      ┌──────┴───────────┐
      ▼                  ▼
 SQL Agent          RAG Agent
      │                  │
      ▼                  ▼
 MySQL Database     ChromaDB
      │
      ▼
LLM Response
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-org/Enterprise_CTMS_Copilot.git

cd Enterprise_CTMS_Copilot
```

---

## Create Virtual Environment

Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

Current dependencies include:

- langchain
- langchain-openai
- langchain-core
- langchain-community
- langchain-chroma
- langchain-huggingface
- sentence-transformers
- pypdf
- python-dotenv
- sqlalchemy
- pymysql
- uvicorn
- streamlit
- mlflow
- loguru

---

# Configuration

Create a `.env` file.

Example:

```text
OPENAI_API_KEY=xxxxxxxx

MODEL_NAME=gpt-4o

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_DATABASE=enterprise_ctms

CHROMA_COLLECTION=enterprise_ctms
CHROMA_PATH=./chroma_db
```

---

# Running the Application

```bash
uvicorn app.main:app --reload
```

Open

```
http://localhost:8000/docs
```

Swagger UI will be available.

---

# AI Components

## Supervisor Agent

Responsible for

- Intent Detection
- Agent Routing
- Response Aggregation

---

## Trial Planning Agent

Supports

- Protocol Queries
- Trial Information
- Milestones
- Timelines

---

## Budget Agent

Supports

- Budget Analysis
- Cost Tracking
- Financial Reports
- Invoice Analysis

---

## Monitoring Agent

Supports

- Site Visits
- Monitoring Reports
- Compliance

---

## Site Management Agent

Supports

- Site Information
- Investigator Details
- Site Performance

---

## Recruitment Agent

Supports

- Enrollment
- Recruitment Metrics
- Screening Status

---

# RAG Pipeline

```
Documents

     │

PDF Loader

     │

Text Splitter

     │

Embedding Model

     │

ChromaDB

     │

Retriever

     │

LLM

     │

Answer
```

---

# SQL Agent

Supports natural language questions such as

- Show active trials
- List delayed sites
- Total enrolled patients
- Budget utilization
- Monitoring visits completed

---

# Logging

Application logs include

- Startup
- Database Health
- Vector Database Status
- Agent Execution
- Request Details
- Error Handling

---

# Future Enhancements

- LangGraph Integration
- Human-in-the-Loop Workflow
- Knowledge Graph Support
- Azure OpenAI
- Authentication & Authorization
- RBAC
- Redis Cache
- Docker Support
- Kubernetes Deployment
- CI/CD Pipeline
- Monitoring Dashboard
- Streamlit Chat UI

---

# Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

# License

MIT License

---

# Author

Enterprise CTMS Copilot

AI-Powered Clinical Trial Management System using FastAPI, LangChain, Multi-Agent AI, SQL Agent, and Retrieval Augmented Generation (RAG).