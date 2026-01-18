##AI Health Agent
**AI Health Agent** is an AI-powered application that analyzes blood reports and provides personalized, meaningful health insights using a multi-model intelligent agent architecture. 



## 🌟 Features

- Intelligent agent-based architecture with **multi-model cascade system** for reliable results :contentReference[oaicite:2]{index=2}  
- **In-context learning** & knowledge build-up from past analyses :contentReference[oaicite:3]{index=3}  
- **Medical report analysis** with detailed personalized insights :contentReference[oaicite:4]{index=4}  
- **PDF upload, validation, and text extraction** (up to ~20 MB) :contentReference[oaicite:5]{index=5}  
- **User authentication & session management** :contentReference[oaicite:6]{index=6}  
- **Session history tracking** for review of past analyses :contentReference[oaicite:7]{index=7}  
- Modern UI with real-time feedback and responsiveness :contentReference[oaicite:8]{index=8}

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit   
- **AI Integration:** Multi-model cascade using Groq (LLMs) 
- **Database:** Supabase  
- **PDF Extraction:** PDFPlumber
- **Authentication:** Supabase Auth

---

## 🚀 Installation & Setup

### 🧰 Requirements

- Python **3.8+**
- Streamlit **1.30.0+**
- Groq API key
- Supabase account
- PDFPlumber
- Python-magic (`python-magic-bin` on Windows or `python-magic` on Linux/Mac)

### 📝 Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/harshhh28/hia.git
   cd AI-health-agent
Install dependencies

bash
Copy code
pip install -r requirements.txt
Configure environment variables
Create a file at .streamlit/secrets.toml and add:

toml
Copy code
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-key"
GROQ_API_KEY = "your-groq-api-key"

Set up database schema
Use the SQL script from public/db/script.sql to initialize your Supabase tables. 
GitHub

Run the app

bash
Copy code
streamlit run src/main.py

📁 Project Structure
AI-health-agent/
├── requirements.txt
├── README.md
├── src/
│   ├── main.py                 # Application entry point
│   ├── auth/                   # Authentication related modules
│   │   ├── auth_service.py     # Supabase auth integration
│   │   └── session_manager.py  # Session management
│   ├── components/             # UI Components
│   │   ├── analysis_form.py    # Report analysis form
│   │   ├── auth_pages.py       # Login/Signup pages
│   │   ├── footer.py          # Footer component
│   │   └── sidebar.py         # Sidebar navigation
│   ├── config/                # Configuration files
│   │   ├── app_config.py      # App settings
│   │   └── prompts.py         # AI prompts
│   ├── services/              # Service integrations
│   │   └── ai_service.py      # AI service integration
│   ├── agents/                # Agent-based architecture components
│   │   ├── agent_manager.py   # Agent management
│   │   └── model_fallback.py  # Model fallback logic
│   └── utils/                 # Utility functions
│       ├── validators.py      # Input validation
│       └── pdf_extractor.py   # PDF processing
