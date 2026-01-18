# 🩺 AI Health Agent

**AI Health Agent** is an AI-powered application that analyzes blood test reports and delivers **personalized, meaningful health insights** using a **multi-model intelligent agent architecture**.
It is designed to provide reliable, explainable results through a cascading LLM system and a modern, user-friendly interface.

---

## 🌟 Features

* 🤖 **Intelligent Agent-Based Architecture**
  Multi-model cascade system for higher reliability and accuracy

* 🧠 **In-Context Learning**
  Knowledge build-up from past analyses to improve future insights

* 🧾 **Medical Report Analysis**
  Detailed, personalized interpretation of blood reports

* 📄 **PDF Upload & Processing**

  * Upload PDFs up to ~20 MB
  * Validation and text extraction using PDFPlumber

* 🔐 **User Authentication & Session Management**
  Powered by Supabase Auth

* 🕒 **Session History Tracking**
  Review and revisit previous analyses

* 🎨 **Modern UI**
  Built with Streamlit, offering real-time feedback and responsiveness

---

## 🛠️ Tech Stack

| Layer           | Technology                 |
| --------------- | -------------------------- |
| Frontend        | Streamlit                  |
| AI / LLMs       | Groq (Multi-model cascade) |
| Database        | Supabase                   |
| Authentication  | Supabase Auth              |
| PDF Extraction  | PDFPlumber                 |
| File Validation | Python-Magic               |

---

## 🚀 Installation & Setup

### 🧰 Requirements

* Python **3.8+**
* Streamlit **1.30.0+**
* Groq API Key
* Supabase Account
* PDFPlumber
* Python-Magic

  * **Windows:** `python-magic-bin`
  * **Linux / macOS:** `python-magic`

---

### 📝 Setup Steps

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/omsdl10/AI-HEALTH-AGENT.git
cd AI-HEALTH-AGENT
```

#### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3️⃣ Configure Environment Variables

Create the following file:

```
.streamlit/secrets.toml
```

Add your credentials:

```toml
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-key"
GROQ_API_KEY = "your-groq-api-key"
```

---

#### 4️⃣ Set Up Database Schema

* Navigate to your Supabase project
* Open the **SQL Editor**
* Run the SQL script located at:

```
public/db/script.sql
```

This will initialize all required tables.

---

#### 5️⃣ Run the Application

```bash
streamlit run src/main.py
```

---

## 📂 Project Structure (Overview)

```
AI-HEALTH-AGENT/
│
├── src/
│   ├── main.py
│   ├── agents/
│   ├── utils/
│   └── services/
│
├── public/
│   └── db/
│       └── script.sql
│
├── requirements.txt
├── README.md
└── .streamlit/
    └── secrets.toml
```

##

