# Software Finder Web Application

## Overview

Software Finder is a full-stack, multi-service web application built as a technical task. It allows users to input their business preferences and receive a software recommendation from a Python and Flask-based frontend application.

The project is built with a professional microservices architecture and includes a separate, powerful backend service built with Python and Django. This second service provides a secure administrator dashboard for managing the application's data and a full REST API for serving the data to other applications.

The recommendation logic is handled by an asynchronous background task system using Celery and Redis to ensure the user interface is always fast and responsive. The entire application is containerized using Docker and Docker Compose, allowing for a simple, reliable one-command setup on any system.

### Key Features

* **Intelligent Recommendation Engine:** A Flask application that uses a weighted scoring algorithm, including keyword matching, to provide relevant software recommendations.
* **Asynchronous Task Processing:** The recommendation process runs as a background job using Celery and Redis, ensuring the UI remains responsive even for long-running tasks.
* **Secure Admin Dashboard:** A separate Django application provides a production-ready, password-protected admin panel for viewing, adding, editing, and deleting software data.
* **REST API:** The Django service also exposes a professional REST API endpoint to serve the software data in a clean JSON format, allowing other applications to connect to it.
* **Modern UI:** A clean, single-page interface styled with Tailwind CSS for a responsive user experience.
* **Containerized with Docker:** The entire multi-service application (Flask App, Django App, Celery Worker, Redis, and MySQL Database) is managed by Docker Compose for easy setup and deployment.

---

## Technologies Used

* **Recommendation Service:** Python, Flask, Gunicorn
* **Admin & API Service:** Python, Django, Django REST Framework
* **Background Processing:** Celery, Redis
* **Database:** MySQL
* **Data Processing:** Pandas
* **Frontend:** HTML, Tailwind CSS (via CDN)
* **Containerization:** Docker, Docker Compose

---

## Local Setup and Installation

To run this project locally, please ensure you have **Git** and **Docker Desktop** installed.

**1. Clone the repository:**
Open your terminal and clone this repository to your local machine.
```bash
git clone https://github.com/sahadabdulkarim/findYourSoftware.git
cd findYourSoftware
```

**2. Create the `.env` file:**
Create a file named `.env` in the root of the project. Copy the contents of `.env.example` into it and replace the placeholder passwords with your own strong passwords.

**3. Run the application:**
Make sure Docker Desktop is running. Then, execute the following command from the project's root directory:
```bash
docker-compose up
```
This single command will build and start all three services.

---

## Usage

The application exposes three different endpoints on different ports.

### 1. The Main Web Application

* **URL:** `http://127.0.0.1:5001/`
* **Description:** This is the main user-facing application where you can get software recommendations.

### 2. The Django Admin Panel

* **URL:** `http://127.0.0.1:8000/admin/`
* **Description:** This is the secure dashboard for managing the software data.
* **Setup:** Before you can log in, you must create an administrator account. Open a **second terminal window** (while the application is running) and execute the following command:
    ```bash
    docker-compose exec admin_api python manage.py createsuperuser
    ```
    Follow the prompts to create your username and password. You can then use these to log in to the admin panel.

### 3. The REST API Endpoint

* **URL:** `http://127.0.0.1:8000/api/software/`
* **Description:** This endpoint provides a public, read-only list of all the software in the database in JSON format. No authentication is required to view it.

---
