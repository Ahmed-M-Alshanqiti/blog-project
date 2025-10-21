# 📝 Blog Project (Django + DRF + Channels + PostgreSQL + Docker)

A full-featured Django project that combines REST APIs, real-time chat, user authentication (JWT), posts, comments, notifications, and WebSockets—all containerized with Docker.

---

## 🚀 Features

-   **Backend Core:** Django 5.2 + Django REST Framework
-   **Authentication:** JWT Authentication (`djangorestframework-simplejwt`)
-   **Real-time:** Real-time Chat/Notifications using **Django Channels + Redis** (WebSockets)
-   **Database:** PostgreSQL
-   **Architecture:** Dockerized services for quick setup.
-   **Mode Support:** Supports both **ASGI** and **WSGI**
-   **Readiness:** Ready for local development and production deployment.

---

## 🏗️ Project Structure

blog_project/ │ ├── blog_project/ # Main Django config (ASGI, WSGI, settings) ├── users/ # User model, JWT auth ├── posts/ # Posts, likes, comments ├── Chat/ # Real-time chat via Channels ├── notifications/ # Real-time notifications ├── api/ # DRF API endpoints ├── docker-compose.yml # Defines services (db, redis, web, asgi, nginx) ├── Dockerfile # Python/Django image build ├── Dockerfile.nginx # Nginx image build ├── entrypoint.sh # Migration/Static collection script └── manage.py


---

## ⚙️ Local Development Setup (Recommended)

This setup runs the **PostgreSQL** and **Redis** services inside Docker containers, but runs the Django application directly on your host machine for fast iteration and debugging.

### Prerequisites

1.  **Docker** and **Docker Compose** installed and running.
2.  **Python 3.12+** and a **Virtual Environment** (`.venv`) set up.
3.  Ensure the following packages are installed in your virtual environment: `pip install -r requirements.txt python-dotenv`.

### Step 1: Navigate and Configure

Ensure you are in the project root directory (where `manage.py` is located).

Create a file named **`.env`** in the project root with the following settings. This is **CRITICAL** for connecting your local Django app to the Docker services via `localhost`.

```env
# .env file for local host development

# General Django Settings
DEBUG=True
SECRET_KEY=a-secret-key-for-local-development
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
POSTGRES_DB=blog_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DATABASE_HOST=localhost # Must be localhost to connect from the host machine
DATABASE_PORT=5432

# Redis Settings
REDIS_HOST=localhost    # Must be localhost to connect from the host machine
REDIS_PORT=6379
REDIS_URL=redis://localhost:6379

# Static/Media Roots (Paths on your host machine)
STATIC_ROOT=./staticfiles
MEDIA_ROOT=./media
Step 2: Run Docker Services
Start only the db and redis containers. They will be mapped to your host ports (5432 and 6379).

Bash

# Start the db and redis containers
docker compose up -d db redis
Step 3: Initialize Database and Start Server
Once the containers are running, you can run Django commands from your terminal.

Bash

# 1. Apply database migrations
py manage.py migrate 

# 2. Start the Django development server
py manage.py runserver 
You can now access the site at: http://127.0.0.1:8000/



👨‍💻 Author
Ahmed M. Alshanqiti 📦 GitHub: @Ahmed-M-Alshanqiti