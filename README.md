# Enterprise-AI-Text-to-SQL-Assistant

# Enterprise AI Text-to-SQL Assistant

## Overview

Enterprise AI Text-to-SQL Assistant is an AI-powered system designed to convert natural language questions into optimized SQL queries using open-source Large Language Models (LLMs). The project focuses on intelligent database querying through semantic schema understanding, embedding-based retrieval, and automated SQL generation.

The system enables users to interact with enterprise databases using natural language without requiring SQL knowledge.

---

## Features

- Natural Language to SQL conversion
- Open-source LLM integration
- Semantic schema understanding
- Embedding-based column matching
- Alias and synonym handling
- PostgreSQL database integration
- Dynamic schema retrieval
- AI-powered SQL generation
- Intelligent query understanding

---

## Workflow

User Query  
↓  
Semantic Search  
↓  
Schema Retrieval  
↓  
Embedding-Based Matching  
↓  
Prompt Engineering  
↓  
LLM SQL Generation  
↓  
SQL Execution

---

## Architecture

The system uses a modular AI pipeline:

- Schema Fetching Module
- Semantic Retrieval Module
- Embedding Mapper
- Alias Mapper
- Prompt Builder
- SQL Generator
- PostgreSQL Execution Pipeline

---

## Tech Stack

### AI & NLP
- Qwen 2.5
- SQLCoder
- Hugging Face Transformers
- Sentence Transformers
- LangChain

### Backend
- Python

### Database
- PostgreSQL
- Neon Database

### AI Techniques
- Semantic Search
- Embedding-Based Retrieval
- Prompt Engineering
- LoRA Fine-Tuning Concepts

---

## Key Functionalities

### Natural Language Understanding
Converts user questions into structured SQL queries using LLMs.

### Semantic Column Matching
Handles synonyms and user-friendly language using embedding-based retrieval.

### Schema-Aware Query Generation
Dynamically fetches database schema and generates optimized SQL queries.

### Intelligent Prompt Engineering
Builds structured prompts for accurate SQL generation.

---

## Project Structure

```bash
enterprise-text-to-sql/
│
├── app/
├── schema/
├── embeddings/
├── models/
├── utils/
├── main.py
├── requirements.txt
├── .env
└── README.md
```

---

## Example Query

### User Input

```text
Show employees with salary greater than 50000
```

### Generated SQL

```sql
SELECT * FROM employees WHERE salary > 50000;
```

---

## Results

- Successfully generated SQL queries from natural language input
- Implemented semantic schema understanding using embeddings
- Improved synonym handling for database column matching
- Integrated PostgreSQL schema retrieval and query execution workflows

---

## Future Improvements

- Add FastAPI deployment
- Multi-database support
- Query optimization engine
- Vector database integration
- Advanced agentic workflows
- Real-time enterprise dashboard

---

## Installation

### Clone Repository

```bash
git clone https://github.com/PoojaRJ20/enterprise-text-to-sql.git
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python main.py
```

---

## Security Note

Database credentials and API keys are managed using environment variables and are not stored directly in the repository.

---

## Learning Outcomes

- Understanding of Text-to-SQL systems
- Practical experience with open-source LLMs
- Semantic search and embedding workflows
- Prompt engineering techniques
- Database integration with AI pipelines
- Modular AI system architecture

---

## Author

Pooja Joshi

GitHub: https://github.com/PoojaRJ20
