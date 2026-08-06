# 🚀 AI-Powered Smart Blog Platform (Microservices Architecture)

An enterprise-grade, decoupled web platform built to demonstrate modern **Microservices Architecture** and **AI/ML Integration**. The system utilizes a full-stack **Django** monolith as the core web portal and database manager, which communicates asynchronously with a high-performance **FastAPI** microservice serving as an intelligent text analysis and spam-filtering engine.

---

## 🏗️ System Architecture & Data Flow

Rather than using a tightly-coupled monolithic design, this project implements a **Fault-Tolerant Microservices Pattern** [Context].

```text
[User / Browser] 
       │
       ▼ (1. Submit Custom HTML/Django Form)
[Django Monolith - Port 8000]
       │
       ▼ (2. Intercepted by pre_save Signal / Observer Pattern)
[blog/signals.py] ───(3. HTTP POST Payload)───► [FastAPI AI Engine - Port 8001]
       │                                                      │
       │                                                      ▼ (4. Pydantic Validation & AI Processing)
       │                                              [api.py (/analyze-post)]
       │                                                      │
       ◄───(5. JSON Response: summary & is_spam flag)────────┘
       │
       ▼ (6. Injects AI Metadata dynamically into Columns)
[SQLite / SQLAlchemy DB] (7. Final Safe Commit)
```

### Key Architectural Strengths:
*   **Fault Isolation (Graceful Degradation):** If the FastAPI AI service goes offline for maintenance, the core Django network catches the connection timeout safely. Users can still post content without errors; the system gracefully marks the AI metadata as offline and processes it later.
*   **Polyglot-Ready API:** Since the AI analyzer is served via an isolated async REST endpoint, this exact same AI engine can be plugged into **PHP (Laravel)** or **.NET (C#)** services with a single HTTP client call.

---

## 🛠️ Tech Stack & Dependencies

*   **Core Monolith:** Python 3.12+, Django 5.0+ (MVT Architecture)
*   **AI Microservice:** FastAPI, Uvicorn (Async ASGI Server)
*   **Data Validation:** Pydantic Fields (Strict Type Safety)
*   **Data Processing & ML:** NumPy, Pandas, Scikit-Learn
*   **Database:** SQLite / SQLAlchemy Engine

---

## 📁 Project Structure

```text
smart_blog/
│
├── core/                   # Main Django settings and routing (Global Gateway)
│   ├── settings.py
│   └── urls.py
│
├── blog/                   # Django Web Application Module (MVC Pattern)
│   ├── models.py           # Database schemas with Dunder/Magic methods
│   ├── views.py            # Clean Function-based Controller views
│   ├── signals.py          # Model Observers managing the API network hooks
│   └── templates/          # Jinja2/DTL frontend portal forms
│
├── api.py                  # Isolated FastAPI script running the AI model engine
├── manage.py               # Project execution CLI utility
└── requirements.txt        # Enterprise environment dependencies
```

---

## ⚡ Installation & Local Setup

Follow these steps to spin up the dual-server microservices environment locally:

### 1. Clone the Repository & Environment Setup
```bash
git clone https://github.com
cd py-blog

# Create and Activate Virtual Environment
python -m venv venv
source venv/Scripts/activate  # On Git Bash / Mac: source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Migrations & Superuser (Admin) Setup
```bash
python manage.py makemigrations
python manage.py migrate

# Create admin panel access credentials
python manage.py createsuperuser
```

### 4. Running the Microservices (Dual-Server Execution)

You need to open **two separate terminal windows** inside your active virtual environment:

*   **Terminal 1: Run Django Core (Port 8000)**
    ```bash
    python manage.py runserver
    ```
    *Access Core Portal:* `http://127.0.0`  
    *Access Admin Control:* `http://127.0.0`

*   **Terminal 2: Run FastAPI AI Engine (Port 8001)**
    ```bash
    uvicorn api:app --port 8001 --reload
    ```
    *Access Interactive Swagger UI:* `http://127.0.0`

---

## 🧪 Real-World Integration Scenarios

1.  **AI Summary Generation:** When writing a long blog post via the custom interface, the FastAPI engine handles pattern boundaries and returns a truncated `[AI Generated Summary]` back into Django's storage layer.
2.  **Spam Protection Flagging:** If the input text context triggers malicious or blacklisted keywords (e.g., *"click here"*, *"free money"*), the model automatically sets the database flag `is_spam = True`, which can be intercepted by admin dashboards.

---

## 🔮 Future Roadmap (Scale Enhancements)
- [ ] Implement **Apache Kafka** or **RabbitMQ** message brokers to replace the direct HTTP sync requests with complete asynchronous event-driven streaming.
- [ ] Integrate **Docker** containers for multi-environment orchestration and model-drift tracking via **MLflow**.

---
*Developed with clean-code design principles, OOP best practices, and enterprise repository maps.*
