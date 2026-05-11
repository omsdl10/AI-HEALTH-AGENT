# AI Health Agent

AI Health Agent is a Streamlit app for uploading health reports, generating AI-powered analysis, and asking follow-up questions.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run src/main.py
```

Create `.streamlit/secrets.toml` before running analysis:

```toml
GROQ_API_KEY = "your-groq-api-key"
```

## Deploy

Use `src/main.py` as the Streamlit entry point when this folder is the app root.
If deploying from the GitHub repository root, use `AI-health-agent/src/main.py`.

Required app secret:

```toml
GROQ_API_KEY = "your-groq-api-key"
```

The app uses a local SQLite database at `data/health_agent.sqlite3`. This is fine for demos and single-instance deployments, but hosted platforms may reset local files during redeploys or restarts. For production, use a managed database.
