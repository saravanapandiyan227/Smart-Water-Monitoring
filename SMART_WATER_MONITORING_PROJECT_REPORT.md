# COIMBATORE INSTITUTE OF TECHNOLOGY
### (Government Aided Autonomous Institution Affiliated to Anna University)
### 23IT723 – DEVOPS LABORATORY
## MINI PROJECT REPORT

# SMART WATER MONITORING AND COMPLAINT MANAGEMENT SYSTEM (AQUAWATCH)

**OCTOBER 2026**

**Submitted by:**  
**SARAVANA PANDIYAN**  
Roll No: **23IT045** | Register No: **2303717620522022**  
B.Tech. Information Technology — Semester VII  

---

## BONAFIDE CERTIFICATE

Certified that this project report titled **“SMART WATER MONITORING AND COMPLAINT MANAGEMENT SYSTEM”** is the bonafide work of **SARAVANA PANDIYAN (Reg No: 2303717620522022)** completed during the academic year **2025–2026 – Semester VII** for the project presentation and practical examination of **23IT723 – DEVOPS LABORATORY** under our supervision.

Certified that the candidate was examined during the DevOps Laboratory Project Examination held on _____________________.

**Review Members:**  
- **Dr. M. Sangeetha**, Department of Information Technology  
- **Dr. E. Arul**, Department of Information Technology  

---

## 23IT723 – DEVOPS LABORATORY EVALUATION SCHEME

| S.No. | Evaluation Component | Key Verification Points | Marks |
|---|---|---|:---:|
| 1 | Problem Definition & Project Planning | Problem statement, objectives, architecture, technology selection | 10 |
| 2 | Git Repository & Version Control | Repository creation, clean commits, README, .gitignore, database exclusion | 15 |
| 3 | Branching, Merging & Collaboration | Branch structure, commit history verification, reproducible codebase | 10 |
| 4 | Application Development & Build | Flask backend with SQLite, parameterized queries, dynamic templates | 15 |
| 5 | Jenkins Continuous Integration | Declarative Jenkinsfile, 4-stage pipeline, console log verification | 15 |
| 6 | Docker Containerization | Dockerfile optimization (python:3.11-slim), image build (`water-monitoring-ci`), port mapping 5002:5000 | 10 |
| 7 | Ansible Automation & Deployment | Playbook `water-deploy.yml`, community.docker module, idempotent execution | 5 |
| 8 | Testing & Verification | Pytest suite with 13 automated tests, isolated temporary DB fixture | 5 |
| 9 | Documentation & Technical Presentation | Architecture diagrams, step-by-step commands, execution logs | 5 |
| 10 | Final Demonstration & Viva-Voce | Live demonstration of complaint workflow, admin updates, Docker persistence | 10 |
| **TOTAL** | | | **100** |

---

## TABLE OF CONTENTS

1. [Introduction](#1-introduction)
2. [Objectives](#2-objectives)
3. [Abstract](#3-abstract)
4. [Technology Stack](#4-technology-stack)
5. [System Architecture](#5-system-architecture)
6. [Module 1 — User Interface & Water Monitoring](#6-module-1--user-interface--water-monitoring)
7. [Module 2 — Complaint Reporting & Priority Selection](#7-module-2--complaint-reporting--priority-selection)
8. [Module 3 — Flask Backend & Route Management](#8-module-3--flask-backend--route-management)
9. [Module 4 — SQLite Database Management](#9-module-4--sqlite-database-management)
10. [Module 5 — Git & GitHub Source Control](#10-module-5--git--github-source-control)
11. [Module 6 — Docker Containerization](#11-module-6--docker-containerization)
12. [Module 7 — Jenkins CI/CD Pipeline](#12-module-7--jenkins-cicd-pipeline)
13. [Module 8 — Automated Testing (Pytest)](#13-module-8--automated-testing-pytest)
14. [Module 9 — Ansible Deployment](#14-module-9--ansible-deployment)
15. [Module 10 — Persistent Storage (Docker Volume)](#15-module-10--persistent-storage-docker-volume)
16. [Module 11 — Admin Dashboard & Status Workflow](#16-module-11--admin-dashboard--status-workflow)
17. [Module 12 — Application & Deployment Verification](#17-module-12--application--deployment-verification)
18. [Results and Output (Screenshots)](#18-results-and-output)
19. [Commands Used](#19-commands-used)
20. [Advantages](#20-advantages)
21. [Limitations](#21-limitations)
22. [Future Enhancements](#22-future-enhancements)
23. [Conclusion](#23-conclusion)

---

## 1. INTRODUCTION

The **Smart Water Monitoring and Complaint Management System (AquaWatch)** is a web-based public utility monitoring and grievance redressal platform engineered to address challenges in urban water distribution and public utility reporting. In conventional municipality and campus settings, water leakage, contamination, pipeline damage, and supply disruptions often go unreported or suffer from severe communication delays between residents and maintenance authorities.

AquaWatch provides an integrated digitalized platform where residents can inspect simulated real-time water quality parameters (water tank level, pH level, turbidity, and water temperature), register complaints with location and priority, receive a tracking ID (e.g., `WC-00001`), and monitor progress live on a visual status timeline. An authorized Administrative Portal allows maintenance supervisors to review incoming complaints and systematically update statuses across the lifecycle: **Pending &rarr; Assigned &rarr; In Progress &rarr; Resolved &rarr; Closed**.

Beyond core web functionality, this project implements an end-to-end DevOps automation pipeline. Source code is tracked using Git/GitHub, containerized into an optimized Docker image, validated through automated Pytest unit and integration tests, orchestrated via Jenkins CI/CD declarative pipelines, deployed with Ansible configuration management, and protected against data loss through a persistent Docker Named Volume backing the SQLite database.

---

## 2. OBJECTIVES

- To develop a clean, responsive water utility web application using Python Flask, HTML5, CSS3, and JavaScript.
- To implement simulated real-time water quality monitoring for key parameters (Water Level, pH, Turbidity, Temperature) with illustrative threshold categorization (Normal, Warning, Critical).
- To provide a transparent grievance registration mechanism that assigns unique Complaint IDs and offers real-time status tracking.
- To create an Admin Management Dashboard with session-based authentication to manage complaint workflows and inspect complaint statistics.
- To implement Git and GitHub source code control with rigorous exclusion rules preventing database and credential leaks.
- To containerize the application using lightweight Docker images (`python:3.11-slim`) for repeatable execution.
- To build a 4-stage Jenkins CI/CD pipeline automating Checkout, Build, Pytest Validation, and Ansible Deployment.
- To incorporate Pytest automated test coverage (13 tests) executing against isolated temporary databases.
- To automate container deployment and port mapping (5002:5000) using Ansible and the `community.docker` module.
- To implement a persistent Docker Named Volume (`water_monitoring_data`) guaranteeing zero data loss across container recreation.

---

## 3. ABSTRACT

Effective water management and prompt infrastructure maintenance are vital for smart communities and college campuses. Traditional water complaint systems rely on verbal communication, physical registers, or unmonitored helpdesk emails, leading to lost complaints, lack of accountability, and zero visibility into water quality trends.

The proposed **Smart Water Monitoring and Complaint Management System** combines a functional Flask web application with a full modern DevOps CI/CD pipeline. The user-facing module allows residents to view live water quality measurements, log categorized complaints, and track resolutions. The admin module empowers utility managers to update statuses and monitor system health. The underlying infrastructure follows a production-grade DevOps workflow: Developer code push triggers a 4-stage Jenkins pipeline which builds the Docker container (`water-monitoring-ci`), runs 13 automated Pytest test cases, and invokes an Ansible playbook (`water-deploy.yml`) inside an `ansible-docker-lab` container. The application container (`water-monitoring-ansible`) exposes port 5002 on the host and mounts a Docker Named Volume (`water_monitoring_data`) to `/app/data`, preserving complaint history permanently across container redeployments.

---

## 4. TECHNOLOGY STACK

| Technology | Version | Purpose in Project |
|---|---|---|
| **HTML5 & CSS3** | HTML5 / CSS3 | Responsive frontend with water-utility theme |
| **JavaScript** | ES6+ | Character counter, form validation, filter tabs |
| **Python** | 3.11.9 | Core backend programming language |
| **Flask** | 3.0.3 | Web application framework and session routing |
| **SQLite** | 3.x (Built-in) | Embedded database storing complaints and readings |
| **Git & GitHub** | 2.45+ | Version control & remote repository management |
| **Docker** | 29.x | Containerization and portable runtime environment |
| **Pytest** | 8.2.2 | Automated testing framework (13 test cases) |
| **Jenkins** | 2.580.1 LTS | CI/CD automation and declarative pipeline orchestration |
| **Ansible** | 2.19 / community.docker | Container provisioning and idempotent deployment |
| **Docker Volume** | Named Volume | Persistent database storage (`water_monitoring_data`) |

---

## 5. SYSTEM ARCHITECTURE

```
[ Developer ] 
      │ (git push)
      ▼
[ GitHub Repository ]
      │ (webhook / pull)
      ▼
[ Jenkins CI/CD Pipeline ] (http://localhost:8080)
      ├── Stage 1: Checkout ───────► Fetch latest source code
      ├── Stage 2: Build ──────────► docker build -t water-monitoring-ci .
      ├── Stage 3: Test ───────────► docker run --rm ... pytest test_app.py -v (13/13 Pass)
      └── Stage 4: Deploy ─────────► Ansible Playbook (inside ansible-docker-lab)
                                            │
                                            ▼
                           [ Docker Container: water-monitoring-ansible ]
                                  (Exposed Port: 5002:5000)
                                            │
                                            ▼
                           [ Docker Named Volume: water_monitoring_data ]
                                  (/app/data/water_monitoring.db)
```

---

## 6. MODULES SUMMARY

### Module 1 — User Interface & Water Monitoring
Provides dashboard with gauges for Water Level (%), pH (6.5–8.5), Turbidity (NTU), Temperature (°C), and historical readings table.

### Module 2 — Complaint Reporting & Priority Selection
Allows reporting issues under 8 categories (Water Leakage, Low Pressure, Contamination, etc.) with priority levels (Low, Medium, High, Critical) and automatic Complaint ID generation (`WC-00001`).

### Module 3 — Flask Backend & Route Management
Manages public and protected administrative endpoints in `app.py`:
- `/`: Home page with quick stats
- `/monitoring`: Water quality sensor dashboard
- `/report` & `/submit_complaint`: Complaint registration
- `/track`: Search complaint and render status timeline
- `/admin/login`, `/admin`, `/update_status`: Authenticated supervisor controls

### Module 4 — SQLite Database Management
Maintains two persistent tables: `water_complaints` and `water_readings`. All SQL operations use parameterized queries to prevent injection vulnerabilities.

### Module 5 — Git & GitHub Source Control
Tracks code with `.gitignore` explicitly excluding `.db`, `.venv/`, and `.env` files.

### Module 6 — Docker Containerization
Builds lightweight `python:3.11-slim` container with all dependencies pinned in `requirements.txt`.

### Module 7 — Jenkins CI/CD Pipeline
Executes automated 4-stage pipeline stopping immediately if any test fails.

### Module 8 — Automated Testing (Pytest)
13 unit and integration tests covering routes, database queries, and session authentication using isolated temporary SQLite databases.

### Module 9 — Ansible Deployment
Deploys `water-monitoring-ansible` on port 5002 with restart policy `unless-stopped` using `community.docker.docker_container`.

### Module 10 — Persistent Storage (Docker Volume)
Preserves database across container recreation through `water_monitoring_data:/app/data`.

### Module 11 — Admin Dashboard & Status Workflow
Allows supervisors to advance complaints through `Pending → Assigned → In Progress → Resolved → Closed`.

### Module 12 — Application & Deployment Verification
Validates that port 5002 is reachable, tests pass, and data survives container deletion.

---

## 18. RESULTS AND OUTPUT

### Live Application Evidence
- **Host Port 5002:** AquaWatch Application running and accessible.
- **Port 8080:** Jenkins Dashboard running with `water-monitoring-pipeline`.
- **Pytest:** 13 passed in 0.63s.
- **Ansible:** `ok=4 changed=1 unreachable=0 failed=0`.
- **Database:** Complaints persisted across container restart in `water_monitoring_data`.

---

## 19. COMMANDS USED

```bash
# 1. Local execution
cd WaterMonitoring
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py

# 2. Pytest execution
python -m pytest test_app.py -v

# 3. Docker build & volume creation
docker build -t water-monitoring-ci .
docker volume create water_monitoring_data

# 4. Ansible deployment
docker cp ansible/water-deploy.yml ansible-docker-lab:/water-deploy.yml
docker exec ansible-docker-lab ansible-playbook -i /inventory.ini /water-deploy.yml

# 5. Database verification
docker exec water-monitoring-ansible python -c "import sqlite3; conn=sqlite3.connect('data/water_monitoring.db'); print(conn.execute('SELECT * FROM water_complaints').fetchall())"
```

---

## 20. CONCLUSION

The **Smart Water Monitoring and Complaint Management System** successfully demonstrates the integration of a full-stack Flask web application with a complete DevOps automated pipeline using Git, GitHub, Docker, Pytest, Jenkins, Ansible, and Docker Volumes, providing a reliable and verifiable software delivery model.
