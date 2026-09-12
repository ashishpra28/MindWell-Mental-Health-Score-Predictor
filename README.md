# 🧠 MindWell — Mental Health Score Predictor & AI Assistant

MindWell is an end-to-end Machine Learning and Agentic AI application that predicts a student's mental health score based on lifestyle, academic, and social-media usage patterns.

It also includes an AI-powered conversational assistant that analyzes the predicted score and provides personalized guidance using a LangGraph-based workflow.

---

## ✨ Features

- 📊 Mental health score prediction using Machine Learning
- 🤖 AI-powered conversational assistant
- 🔀 LangGraph-based agentic workflow
- ⚡ Real-time prediction through FastAPI
- 💬 Personalized lifestyle and score-based guidance
- 🐳 Dockerized backend and frontend
- 📈 ML model inference through a REST API
- 🖥️ Responsive web interface

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │      Frontend       │
                    │ HTML / CSS / JS     │
                    └──────────┬──────────┘
                               │
                    REST API Requests
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │      Backend        │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐        ┌─────────────────┐
        │   ML Predictor  │        │  LangGraph AI   │
        │                 │        │    Assistant    │
        │ Scikit-learn /  │        │                 │
        │ XGBoost Model   │        │ Agent Workflow  │
        └─────────────────┘        └─────────────────┘
                 │                           │
                 └─────────────┬─────────────┘
                               ▼
                         User Response
