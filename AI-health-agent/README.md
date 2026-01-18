##AI Health Agent##
AI Health Agent is an AI-powered application that analyzes blood reports and provides personalized, meaningful health insights using a multi-model intelligent agent architecture. 



## 🌟 Features

- Intelligent agent-based architecture with **multi-model cascade system** for reliable results
- **In-context learning** & knowledge build-up from past analyses 
- **Medical report analysis** with detailed personalized insights 
- **PDF upload, validation, and text extraction** (up to ~20 MB) 
- **User authentication & session management** 
- **Session history tracking** for review of past analyses   
- Modern UI with real-time feedback and responsiveness

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
   git clone https://github.com/omsdl10/AI-HEALTH-AGENT.git
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

