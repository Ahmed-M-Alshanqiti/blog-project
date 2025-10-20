# 📝 Blog Project (Django + DRF + Channels + PostgreSQL + Docker)

A full-featured Django project that combines REST APIs, real-time chat, user authentication (JWT), posts, comments, notifications, and WebSockets — all containerized with Docker.

---

## 🚀 Features

- Django 5.2 + Django REST Framework
- JWT Authentication (`djangorestframework-simplejwt`)
- Real-time Chat using **Django Channels + Redis**
- PostgreSQL database
- Nginx + Daphne (ASGI) setup
- Dockerized multi-container architecture
- Supports both **ASGI** and **WSGI**
- Ready for deployment

---

## 🏗️ Project Structure

blog_project/
│
├── blog_project/ # Main Django config (ASGI, WSGI, settings)
├── users/ # User model, JWT auth
├── posts/ # Posts, likes, comments
├── Chat/ # Real-time chat via Channels
├── notifications/ # Real-time notifications
├── api/ # DRF API endpoints
├── docker-compose.yml
├── Dockerfile
├── Dockerfile.nginx
├── entrypoint.sh
└── manage.py

---

## ⚙️ Environment Variables (`.env`)

Before running, create a `.env` file in your root directory:

SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=\*
DATABASE_URL=postgres://postgres:postgres@db:5432/postgres
REDIS_URL=redis://redis:6379

---

## 🐳 Run with Docker (Recommended)

### 1️⃣ Build and start containers

```bash
docker-compose up --build


2️⃣ Apply migrations
docker-compose exec web python manage.py migrate

3️⃣ Create a superuser

`docker-compose exec web python manage.py createsuperuser`

4️⃣ Access the app

Django API → http://localhost/api/v1/

Admin → http://localhost/admin/

DRF Browsable API → styled automatically

🧑‍💻 Run Locally (without Docker)
1️⃣ Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Set up environment variables

Create .env with:

SECRET_KEY=your_secret_key_here
DEBUG=True
DATABASE_URL=postgres://postgres:postgres@localhost:5432/postgres

4️⃣ Apply migrations & run
python manage.py migrate
python manage.py runserver

🧠 Notes

The app supports both ASGI (via Daphne) and WSGI (for compatibility).

Static files are served by Nginx in Docker.

Redis handles WebSocket messaging and notifications.

🧰 Useful Commands
Purpose	Command
Build and run containers	docker-compose up --build
Stop containers	docker-compose down
Run migrations	docker-compose exec web python manage.py migrate
Create superuser	docker-compose exec web python manage.py createsuperuser
Collect static files	docker-compose exec web python manage.py collectstatic --noinput
👨‍💻 Author

Ahmed M. Alshanqiti
📦 GitHub: @Ahmed-M-Alshanqiti




```
