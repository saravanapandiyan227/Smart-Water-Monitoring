# 💧 Smart Water Monitoring and Complaint Management System

A complete, professional **college-level DevOps project** demonstrating a functional Flask web application with a full CI/CD pipeline using Jenkins, Docker, Pytest, and Ansible.

---

## 📋 Table of Contents

1. [Project Description](#project-description)
2. [Project Objectives](#project-objectives)
3. [Main Features](#main-features)
4. [Technology Stack](#technology-stack)
5. [Database Schema](#database-schema)
6. [Application Workflow](#application-workflow)
7. [DevOps Workflow](#devops-workflow)
8. [Project Structure](#project-structure)
9. [Prerequisites](#prerequisites)
10. [Run Locally](#run-locally)
11. [Run Pytest](#run-pytest)
12. [Docker Build & Run](#docker-build--run)
13. [Docker Volume — Persistent Storage](#docker-volume--persistent-storage)
14. [Jenkins CI/CD](#jenkins-cicd)
15. [Ansible Deployment](#ansible-deployment)
16. [Accessing the Application](#accessing-the-application)
17. [Admin Credentials](#admin-credentials)
18. [Troubleshooting](#troubleshooting)
19. [Limitations and Future Enhancements](#limitations-and-future-enhancements)
20. [Viva Demonstration Guide](#viva-demonstration-guide)

---

## Project Description

**AquaWatch — Smart Water Monitoring and Complaint Management System** is a web-based application that enables residents to:

- View simulated water quality monitoring data (water level, pH, turbidity, temperature).
- Submit water-related complaints with a unique Complaint ID.
- Track complaint status in real time.

It also provides an **Admin Dashboard** to manage complaints and view monitoring readings.

> ⚠️ **Disclaimer:** All water readings displayed are **simulated sensor data** for demonstration purposes only. This application is NOT connected to physical IoT sensors. Thresholds shown are illustrative and not official water safety criteria.

---

## Project Objectives

- Demonstrate a working Flask web application with SQLite database integration.
- Implement a complete DevOps CI/CD pipeline: Git → GitHub → Jenkins → Docker → Pytest → Ansible.
- Showcase containerization with Docker and persistent storage using Docker Volumes.
- Implement automated testing using Pytest.
- Deploy the application using Ansible.

---

## Main Features

### Resident Features
- View professional home page with live water status summary.
- View water monitoring dashboard with latest readings.
- Submit water complaints (category, location, description, priority).
- Receive a unique Complaint ID (e.g., `WC-00001`) after submission.
- Track complaint status using the Complaint ID.

### Admin Features
- Secure session-based admin login.
- Dashboard with complaint statistics (Total, Pending, In Progress, Resolved, Closed).
- View all complaints with full details.
- Update complaint status through a working HTML form.
- View latest water monitoring readings.

### Water Monitoring
- Simulated readings: Water Level (%), pH, Turbidity (NTU), Temperature (°C).
- Status classification: **Normal**, **Warning**, **Critical** based on configurable thresholds.
- Reading history table from SQLite database.

### Complaint Categories
Water Leakage · Low Water Pressure · No Water Supply · Water Quality Issue · Pipeline Damage · Overflowing Water Tank · Contaminated Water · Other

### Complaint Priorities
Low · Medium · High · Critical

### Complaint Status Workflow
`Pending → Assigned → In Progress → Resolved → Closed`

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python 3.11, Flask |
| Database | SQLite (via Python's built-in `sqlite3`) |
| Containerization | Docker (python:3.11-slim) |
| Testing | Pytest |
| CI/CD | Jenkins (Declarative Pipeline) |
| Deployment | Ansible (community.docker) |
| Version Control | Git, GitHub |
| Persistence | Docker Named Volume |

---

## Database Schema

### Table: `water_complaints`

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PK AUTOINCREMENT | Unique complaint ID |
| `complaint_type` | TEXT NOT NULL | Complaint category |
| `location` | TEXT NOT NULL | Location/address |
| `description` | TEXT NOT NULL | Problem description |
| `priority` | TEXT NOT NULL | Low / Medium / High / Critical |
| `status` | TEXT NOT NULL | Pending / Assigned / In Progress / Resolved / Closed |
| `created_at` | DATETIME | Submission timestamp |
| `updated_at` | DATETIME | Last update timestamp |

### Table: `water_readings`

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PK AUTOINCREMENT | Reading ID |
| `water_level` | REAL | Water level percentage |
| `ph_level` | REAL | pH value |
| `turbidity` | REAL | Turbidity in NTU |
| `temperature` | REAL | Water temperature in °C |
| `water_status` | TEXT | Normal / Warning / Critical |
| `recorded_at` | DATETIME | Recording timestamp |

- Database file: `data/water_monitoring.db` (local) / `/app/data/water_monitoring.db` (inside Docker)
- Tables are created automatically on first run.
- Sample readings are inserted only once when the table is empty.
- All SQL queries use parameterized statements to prevent SQL injection.

---

## Application Workflow

```
Resident
  → Open Website (Home Page)
  → View Water Monitoring Dashboard
  → Report Water Complaint
      → Select Category, Enter Location & Description, Select Priority
      → Submit (POST /submit_complaint)
      → Flask validates input → SQLite stores complaint
  → Receive Unique Complaint ID (WC-00001)
  → Track Complaint (POST /track)
      → Flask retrieves complaint from SQLite by ID
  → Admin Updates Status (POST /update_status)
  → Resident Views Updated Status
```

> **Important:** Submitting a complaint does NOT trigger Jenkins. These are completely separate workflows.

---

## DevOps Workflow

```
Developer
  → Code changes → git commit → git push → GitHub
  → Jenkins detects change (webhook or manual trigger)
  → Stage 1: Checkout — fetch latest code
  → Stage 2: Build   — docker build -t water-monitoring-ci .
  → Stage 3: Test    — docker run --rm water-monitoring-ci python -m pytest test_app.py
  → Stage 4: Deploy  — docker exec ansible-docker-lab ansible-playbook -i /inventory.ini /water-deploy.yml
  → Ansible deploys container with persistent Docker Volume
  → Flask app accessible at http://localhost:5002
```

---

## Project Structure

```
WaterMonitoring/
├── app.py                    # Flask backend — all routes and database logic
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker image definition
├── Jenkinsfile               # Jenkins CI/CD pipeline
├── test_app.py               # Pytest automated tests (13 tests)
├── .gitignore                # Files excluded from Git
├── README.md                 # This documentation
├── ansible/
│   └── water-deploy.yml      # Ansible deployment playbook
├── templates/
│   ├── base.html             # Base layout (navbar, footer, flash messages)
│   ├── index.html            # Home page
│   ├── monitoring.html       # Water monitoring dashboard
│   ├── report.html           # Complaint reporting form
│   ├── track.html            # Complaint tracking page
│   ├── admin_login.html      # Admin login page
│   └── admin.html            # Admin dashboard
├── static/
│   ├── style.css             # Premium CSS theme (blue/aqua water theme)
│   └── script.js             # Client-side JavaScript
└── data/
    └── .gitkeep              # Keeps data/ in Git; DB is created at runtime
```

---

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Run Flask app locally |
| pip | Latest | Install Python packages |
| Docker | 20.10+ | Build and run containers |
| Jenkins | 2.x | CI/CD automation |
| Ansible | 2.10+ | Container deployment |
| Git | Any | Version control |

---

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/WaterMonitoring.git
cd WaterMonitoring
```

### 2. Create and activate a Python virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Flask application

```bash
python app.py
```

The application will start at: **http://localhost:5000**

### 5. Environment variables (optional for local dev)

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_SECRET_KEY` | `dev-secret-key-change-in-production` | Flask session key |
| `ADMIN_USERNAME` | `admin` | Admin login username |
| `ADMIN_PASSWORD` | `admin123` | Admin login password |
| `DATABASE_PATH` | `data/water_monitoring.db` | SQLite database path |
| `FLASK_DEBUG` | `false` | Enable debug mode |

> ⚠️ **Security Warning:** The default values are for development/demonstration only. Always use environment variables with strong values in any real deployment.

---

## Run Pytest

### Locally (after activating virtualenv):

```bash
python -m pytest test_app.py
```

### With verbose output:

```bash
python -m pytest test_app.py -v
```

### Inside Docker:

```bash
docker run --rm water-monitoring-ci python -m pytest test_app.py -v
```

The test suite uses isolated temporary databases — it does NOT modify your development database.

**Tests covered:**
1. Flask application initializes successfully
2. Home page returns HTTP 200
3. Monitoring page returns HTTP 200
4. Complaint reporting page returns HTTP 200
5. Valid complaint can be submitted
6. Submitted complaint is stored in SQLite
7. Complaint can be retrieved by ID
8. Tracking page displays complaint status
9. Admin login with valid credentials
10. Unauthorized access to admin dashboard is rejected
11. Admin dashboard returns HTTP 200 after authentication
12. Admin can update a complaint status
13. Status update is saved in SQLite

---

## Docker Build & Run

### Build the Docker image

```bash
docker build -t water-monitoring-ci .
```

### Run the container (standalone, without Ansible)

```bash
docker run -d \
  --name water-monitoring-app \
  -p 5000:5000 \
  -v water_monitoring_data:/app/data \
  water-monitoring-ci
```

Access at: **http://localhost:5000**

---

## Docker Volume — Persistent Storage

The SQLite database is stored inside a **Docker Named Volume** to persist data across container restarts and replacements.

### Create the volume

```bash
docker volume create water_monitoring_data
```

### Inspect the volume

```bash
docker volume inspect water_monitoring_data
```

### How it works

- Volume name: `water_monitoring_data`
- Container mount point: `/app/data`
- Database inside container: `/app/data/water_monitoring.db`

The Docker Volume is **managed by Docker** and is independent of the container lifecycle. Even if you stop, remove, and recreate the container, all complaint data and water readings are preserved.

> Do NOT run `docker volume rm water_monitoring_data` unless you want to permanently delete the database.

---

## Jenkins CI/CD

### Configure Jenkins

1. Install Jenkins (or use an existing Jenkins server).
2. Install required plugins: **Git**, **Pipeline**, **Docker Pipeline**.
3. Ensure Jenkins can run `docker` commands (add Jenkins user to `docker` group on Linux).
4. Create a new **Pipeline** job.
5. Set **Pipeline Definition** to: `Pipeline script from SCM`.
6. Set **SCM** to `Git` and enter your GitHub repository URL.
7. Set **Script Path** to: `Jenkinsfile`.
8. Save and trigger the build.

### Pipeline Stages

| Stage | Action |
|-------|--------|
| **Checkout** | Fetch latest source code from GitHub |
| **Build** | `docker build -t water-monitoring-ci .` |
| **Test** | `docker run --rm water-monitoring-ci python -m pytest test_app.py` |
| **Deploy** | `docker exec ansible-docker-lab ansible-playbook -i /inventory.ini /water-deploy.yml` |

The pipeline **fails immediately** if Build or Test fails — it will NOT deploy a broken build.

---

## Ansible Deployment

### Prerequisites

The Ansible playbook uses `community.docker`. Install it inside the Ansible container:

```bash
ansible-galaxy collection install community.docker
```

### Copy the playbook into the Ansible container

```bash
docker cp ansible/water-deploy.yml ansible-docker-lab:/water-deploy.yml
```

### Run the playbook manually

```bash
docker exec ansible-docker-lab ansible-playbook -i /inventory.ini /water-deploy.yml
```

### What the playbook does

1. Creates the `water_monitoring_data` Docker Volume (if not already created).
2. Deploys the `water-monitoring-ci` image as container `water-monitoring-ansible`.
3. Maps host port `5002` → container port `5000`.
4. Mounts the persistent volume at `/app/data`.
5. Sets `restart_policy: unless-stopped`.
6. Verifies the container is running.

The playbook is **idempotent** — running it multiple times will not create duplicate containers or remove persistent data.

---

## Accessing the Application

| Deployment Method | URL |
|-------------------|-----|
| Local Flask | http://localhost:5000 |
| Docker (standalone) | http://localhost:5000 |
| After Ansible Deploy | http://localhost:5002 |

---

## Admin Credentials

| Field | Demo Value |
|-------|-----------|
| Username | `admin` |
| Password | `admin123` |
| Login URL | `/admin/login` |

> Set `ADMIN_USERNAME` and `ADMIN_PASSWORD` environment variables to override the defaults in any real deployment.

---

## Troubleshooting

### Flask app won't start — "No module named flask"
```bash
# Ensure virtualenv is activated, then:
pip install -r requirements.txt
```

### Database not found / permissions error
```bash
# Ensure the data/ directory exists:
mkdir -p data
python app.py   # init_db() creates the database automatically
```

### Docker build fails
```bash
# Check Docker is running:
docker info
# Retry the build:
docker build -t water-monitoring-ci .
```

### Pytest fails — database path error
```bash
# Tests use a temp database — ensure DATABASE_PATH env var is not hard-coded elsewhere
python -m pytest test_app.py -v
```

### Ansible playbook fails — community.docker not found
```bash
docker exec ansible-docker-lab ansible-galaxy collection install community.docker
```

### Container not visible at port 5002
```bash
# Check if container is running:
docker ps
# Check logs:
docker logs water-monitoring-ansible
```

### Jenkins cannot run Docker commands
```bash
# On Linux, add Jenkins user to docker group:
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

---

## Limitations and Future Enhancements

### Current Limitations (Demonstration Project)
- Authentication uses simple session-based login with environment-variable credentials — not suitable for production.
- No password hashing (admin password stored in environment, not database).
- No CSRF protection (omitted for simplicity).
- Water readings are seeded sample data — not from real sensors.
- No email/SMS notification system for complaint updates.
- No user registration or user accounts for residents.

### Possible Future Enhancements
- Integrate real IoT sensor APIs for live water readings.
- Add user registration and JWT-based authentication.
- Implement CSRF protection and input sanitization.
- Add email notifications when complaint status changes.
- Deploy to cloud infrastructure (AWS/GCP/Azure).
- Add Prometheus metrics and Grafana dashboards.
- Implement Kubernetes for container orchestration.
- Add a REST API for mobile app integration.

---

## Viva Demonstration Guide

### Recommended Demo Flow

1. **Show the Home Page** — explain the water status banner, stats cards, and how-it-works section.
2. **Visit Monitoring Dashboard** — explain the gauge cards, threshold table, and reading history from SQLite.
3. **Submit a Complaint** — fill in the form, explain server-side validation, show the unique Complaint ID.
4. **Track the Complaint** — enter the Complaint ID, show the status timeline.
5. **Admin Login** — log in with `admin`/`admin123`, explain session-based authentication.
6. **Admin Dashboard** — show stats cards, filter tabs, and the inline status update form.
7. **Update Status** — change a complaint status, explain that it modifies the SQLite database.
8. **Track Again** — show the updated status back on the tracking page.
9. **Explain the DevOps Pipeline** — Checkout → Build → Test → Deploy with Ansible.
10. **Show Pytest** — run `python -m pytest test_app.py -v` and explain each test.
11. **Show Docker Volume** — run `docker volume inspect water_monitoring_data`.

### Key Points to Explain

- **SQLite** stores all complaints and readings persistently via Docker Volume.
- **Flask** handles routing, validation, session management, and database operations.
- **Pytest** uses isolated temporary databases so tests never affect production data.
- **Docker** packages the entire app so it runs identically in any environment.
- **Jenkins** automates build → test → deploy but is NOT triggered by complaint submissions.
- **Ansible** is idempotent — safe to run multiple times without side effects.
- **Docker Volume** ensures data persists even if the container is deleted and recreated.

---

*AquaWatch — Smart Water Monitoring and Complaint Management System*  
*College DevOps Laboratory Project — 2026*
