# OpsMemory

AI Incident Response Agent with Persistent Learning powered by Hindsight.

## Overview

OpsMemory is an AI-powered incident response assistant designed to help engineers analyze production incidents using persistent memory.

Instead of treating every incident as a completely new problem, OpsMemory remembers previous incidents, retrieves relevant historical evidence, reasons over that memory, and learns from confirmed resolutions.

## Learning Loop

New Incident
→ Recall Historical Memory
→ Reflect & Analyze
→ Recommended Investigation / Resolution
→ Engineer Confirms Resolution
→ Retain New Learning
→ Future Incidents Benefit from Past Experience

## Hindsight Integration

OpsMemory uses Hindsight as its persistent memory layer.

The system uses three core Hindsight capabilities:

- Retain — stores incident information and confirmed resolutions.
- Recall — retrieves relevant historical memories for a new incident.
- Reflect — reasons over recalled memories to produce incident intelligence.

This allows OpsMemory to improve its responses based on previously resolved incidents.

## Technology Stack

- Python
- FastAPI
- Hindsight
- HTML
- CSS
- JavaScript
- Uvicorn
- GitHub

## Project Structure

OpsMemory/
├── backend/
│   ├── main.py
│   ├── hindsight_test.py
│   └── seed_demo.py
├── frontend/
│   └── index.html
├── requirements.txt
├── .gitignore
└── README.md

## Running Locally

### 1. Create and activate the virtual environment

python -m venv venv
.\venv\Scripts\Activate.ps1

### 2. Install dependencies

pip install -r requirements.txt

### 3. Configure environment variables

Create a .env file in the project root:

HINDSIGHT_API_KEY=your_hindsight_api_key
HINDSIGHT_API_URL=https://api.hindsight.vectorize.io
HINDSIGHT_BANK_ID=your_memory_bank_id

Never commit .env or API keys to GitHub.

### 4. Start the backend

uvicorn backend.main:app --reload

The backend runs locally on:

http://127.0.0.1:8000

### 5. Start the frontend

python -m http.server 5500 --directory frontend

Then open:

http://127.0.0.1:5500

## Demo Flow

1. Enter a new production incident.
2. OpsMemory recalls relevant historical incidents.
3. Hindsight Reflect analyzes the recalled evidence.
4. OpsMemory presents likely causes and recommended actions.
5. The engineer confirms the actual resolution.
6. The confirmed resolution is retained in Hindsight.
7. A future similar incident can retrieve and use that learned experience.

## Example Learning Scenario

A previous checkout incident may reveal that a slow database query was caused by a full table scan and was resolved by adding a database index.

When a future checkout performance incident occurs, OpsMemory can recall that historical experience and use it as evidence while analyzing the new incident.

## Purpose

OpsMemory demonstrates how persistent memory can transform an incident response assistant from a stateless chatbot into a system that can learn from previous operational experience.

## Security

API keys and environment secrets are kept outside the source code and excluded from Git using .gitignore.

## License

This project is created for educational and hackathon demonstration purposes.
