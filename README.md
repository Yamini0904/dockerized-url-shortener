# 🚀 Dockerized URL Shortener API

Production-ready URL shortening service built using FastAPI and PostgreSQL, fully containerized with Docker.

---

## 🛠 Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL 15
- Docker
- Docker Compose

---

## ⚙️ Features

- Shorten URLs
- Redirect to original URLs
- Click analytics tracking
- PostgreSQL persistent storage
- Multi-container Docker architecture
- Internal Docker networking
- Swagger API documentation

---

## 🐳 Run Locally

```bash
docker compose up --build
```

Access API docs:
http://localhost:8000/docs

---

## 🏗 Architecture

- App container (FastAPI)
- Database container (PostgreSQL)
- Internal Docker network
- Persistent volume for database

---

## 📌 Key Learning Outcomes

- Container orchestration using Docker Compose
- Service-to-service networking (db instead of localhost)
- Environment variable configuration
- Debugging containerized database connectivity issues

---

## 👩‍💻 Author

Akkaloori Yamini 
