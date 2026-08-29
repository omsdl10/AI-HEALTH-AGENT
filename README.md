---
title: AI Health Agent
sdk: streamlit
app_file: src/main.py
---

# AI Health Agent

AI Health Agent is a Streamlit application that helps users upload blood report PDFs, generate AI-assisted health insights, and ask follow-up questions about the report in a chat-style workflow.

The app is designed for educational and wellness-oriented interpretation. It is not a medical device and does not replace advice from a qualified healthcare professional.

## Features

- PDF report upload with file validation and text extraction
- Sample report mode for quick testing
- AI-generated health analysis with risk signals and recommendations
- Follow-up chat using report context
- Local user accounts and session history
- SQLite storage for users, chat sessions, and messages
- Groq-powered LLM responses with model fallback handling
- Streamlit UI with authentication, sidebar history, and analysis workflow

## Tech Stack

- Streamlit for the web interface
- Groq for LLM inference
- SQLite for local app data
- PDFPlumber for PDF text extraction
- LangChain, FAISS, and Hugging Face embeddings for contextual follow-up chat

## Project Structure

```text
.
├── public/db/script.sql
├── requirements.txt
├── src
│   ├── agent
│   ├── auth
│   ├── components
│   ├── config
│   ├── services
│   ├── utils
│   └── main.py
└── README.md
```

## Run Locally

1. Clone the repository.

```bash
git clone https://github.com/omsdl10/AI-HEALTH-AGENT.git
cd AI-HEALTH-AGENT/AI-health-agent
```

2. Create and activate a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Add your Groq API key.

Create `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "your-groq-api-key"
```

5. Start the app.

```bash
streamlit run src/main.py
```

## Deploy

### Streamlit Community Cloud

Use these settings:

```text
Repository: omsdl10/AI-HEALTH-AGENT
Branch: main
Main file path: AI-health-agent/src/main.py
```

Add this app secret:

```toml
GROQ_API_KEY = "your-groq-api-key"
```

### Hugging Face Spaces

This README includes Hugging Face Spaces metadata for a Streamlit app. If this folder is uploaded as the Space root, Hugging Face can run it with:

```text
SDK: Streamlit
App file: src/main.py
```

Add `GROQ_API_KEY` as a Space secret.

## Data Storage

The app creates a local SQLite database at:

```text
data/health_agent.sqlite3
```

This works well for local development, demos, and single-instance deployments. On free hosted platforms, local files may be reset during rebuilds, redeploys, or restarts. For production use, replace SQLite with a managed database such as PostgreSQL.

## Security Notes

- Do not commit `.streamlit/secrets.toml`.
- Rotate exposed API keys before public deployment.
- Uploaded reports may contain sensitive health information. Use a deployment platform and database setup appropriate for the privacy requirements of your users.

## Medical Disclaimer

AI Health Agent provides AI-generated analysis for informational purposes only. It should not be used for diagnosis, treatment decisions, emergencies, or as a substitute for professional medical advice. Always consult a qualified healthcare provider for medical concerns.
