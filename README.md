# Software Finder Web Application

## Overview

Software Finder is a full-stack web application built as a technical task. It allows users to input their business preferences and receive a software recommendation based on a predefined dataset. The project demonstrates skills in backend development with Flask, data processing with Pandas, database management with MySQL, and modern frontend design using HTML and Tailwind CSS. The entire application is containerized using Docker and Docker Compose for easy setup and deployment.

### Key Features

* **Intelligent Scoring Engine:** Recommendations are based on a weighted scoring system that prioritizes the most important user criteria.
* **Keyword Matching:** Users can enter comma-separated keywords (e.g., "collaboration, agile") to receive highly relevant recommendations based on software features and tags.
* **Modern UI:** A clean, single-page interface styled with Tailwind CSS for a responsive user experience.
* **Containerized with Docker:** The entire application (Flask backend + MySQL database) is managed by Docker Compose, allowing for a simple one-command setup on any system.
* **Robust Backend:** The Flask backend API handles user requests, connects securely to the database, and processes data efficiently using Pandas.

---

## Technologies Used

* **Backend:** Python, Flask, Gunicorn
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
cd software-finder-project
