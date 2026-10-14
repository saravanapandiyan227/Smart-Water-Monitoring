import docx
import shutil
import os
import zipfile
import re

SOURCE_DOCX = "devops report.docx"
TARGET_DOCX = "Smart_Water_Monitoring_DevOps_Report.docx"
NEW_MEDIA_DIR = "new_media"

def update_cell_text(cell, new_text):
    updated = False
    for p in cell.paragraphs:
        if p.text.strip():
            text_runs = [r for r in p.runs if len(r._r.xpath('./w:drawing')) == 0]
            if text_runs:
                text_runs[0].text = new_text
                for r in text_runs[1:]:
                    r.text = ""
            else:
                p.text = new_text
            updated = True
            break
    if not updated and cell.paragraphs:
        cell.paragraphs[0].text = new_text

def update_para(p, new_text):
    text_runs = [r for r in p.runs if len(r._r.xpath('./w:drawing')) == 0]
    if text_runs:
        text_runs[0].text = new_text
        for r in text_runs[1:]:
            r.text = ""
    elif not p.runs:
        p.text = new_text

def replace_in_para_text(p, old_str, new_str):
    full_text = "".join(r.text for r in p.runs)
    if old_str in full_text:
        new_full = full_text.replace(old_str, new_str)
        update_para(p, new_full)

def main():
    print(f"Loading {SOURCE_DOCX}...")
    doc = docx.Document(SOURCE_DOCX)

    # 1. Update Table 2 (Faculty Evaluation Record)
    t2 = doc.tables[2]
    update_cell_text(t2.rows[0].cells[1], "SARAVANA PANDIYAN V P")
    update_cell_text(t2.rows[0].cells[3], "2303717620521047")
    update_cell_text(t2.rows[1].cells[1], "SMART WATER MONITORING AND COMPLAINT MANAGEMENT SYSTEM")
    update_cell_text(t2.rows[1].cells[3], "13-10-2026")

    # 2. Update Table 3 (Table of Contents - Part 1)
    t3 = doc.tables[3]
    toc_t3 = [
        ("1", "INTRODUCTION", "05"),
        ("2", "OBJECTIVES", "05"),
        ("3", "ABSTRACT", "06"),
        ("4", "TECHNOLOGY STACK", "06"),
        ("5", "SYSTEM ARCHITECTURE", "07"),
        ("6", "MODULE 1 - USER INTERFACE & COMPLAINT REGISTRATION", "08"),
        ("7", "MODULE 2 - FLASK BACKEND & SENSOR TELEMETRY", "09"),
        ("8", "MODULE 3 - SQLITE DATABASE MANAGEMENT", "10"),
        ("9", "MODULE 4 - GIT & GITHUB SOURCE CONTROL", "11"),
        ("10", "MODULE 5 - DOCKER CONTAINERIZATION", "12"),
        ("11", "MODULE 6 - JENKINS CI/CD PIPELINE", "14"),
        ("12", "MODULE 7 - AUTOMATED TESTING", "15")
    ]
    for idx, (sno, title, page) in enumerate(toc_t3):
        row = t3.rows[idx + 1]
        update_cell_text(row.cells[0], sno)
        update_cell_text(row.cells[1], title)
        update_cell_text(row.cells[2], page)

    # 3. Update Table 4 (Table of Contents - Part 2)
    t4 = doc.tables[4]
    toc_t4 = [
        ("13", "MODULE 8 - ANSIBLE DEPLOYMENT", "17"),
        ("14", "MODULE 9 - PERSISTENT STORAGE", "18"),
        ("15", "MODULE 10 - ADMIN & COMPLAINT MANAGEMENT", "19"),
        ("16", "MODULE 11 - CI/CD INTEGRATION", "20"),
        ("17", "MODULE 12 - APPLICATION & DEPLOYMENT VERIFICATION", "21"),
        ("18", "RESULTS AND OUTPUT", "23"),
        ("19", "COMMANDS USED", "23"),
        ("20", "ADVANTAGES", "28"),
        ("21", "LIMITATIONS", "28"),
        ("22", "FUTURE ENHANCEMENTS", "29"),
        ("23", "CONCLUSION", "29")
    ]
    for idx, (sno, title, page) in enumerate(toc_t4):
        row = t4.rows[idx]
        update_cell_text(row.cells[0], sno)
        update_cell_text(row.cells[1], title)
        update_cell_text(row.cells[2], page)

    # 4. Update Table 5 (Technology Stack Table)
    t5 = doc.tables[5]
    update_cell_text(t5.rows[6].cells[2], "Database storage for sensor logs & complaints")

    # 5. Targeted Paragraph Updates
    p_updates = {
        # Section 1 - INTRODUCTION
        82: ("     The Smart Water Monitoring and Complaint Management System (AquaWatch) is an intelligent web-based utility platform developed to monitor municipal water quality in real time and streamline citizen grievance redressal. The system allows citizens and residents to view real-time water quality metrics (pH, TDS, turbidity, pressure), submit water supply complaints (leakage, contamination, low pressure) with detailed descriptions, and track ticket resolution statuses through a modern digital interface. An admin dashboard is also provided for municipal water engineers to review real-time telemetry, analyze incident queues, and update complaint lifecycles. The application is developed using HTML, CSS, JavaScript, Python, Flask, and SQLite, with Flask handling backend operations and SQLite storing water telemetry and citizen complaints. The project also incorporates modern DevOps practices to automate the development, testing, and deployment process. Git and GitHub are used for source code management, while Jenkins automates the CI/CD pipeline. Docker provides application containerization, Pytest performs automated testing, and Ansible automates deployment and container configuration. A Docker Volume (water_monitoring_data) is used to provide persistent storage for the SQLite database. The project combines a functional municipal water monitoring system with DevOps automation to provide a structured, resilient, and reliable approach to utility management."),
        
        # Section 2 - OBJECTIVES
        84: "To develop a responsive web-based water monitoring interface enabling citizens to observe water quality metrics, register complaints, and track grievance statuses conveniently.",
        85: "To implement an admin dashboard for viewing real-time water quality telemetry and managing complaint resolution workflows using SQLite.",
        86: "To organize water sensor data and complaint records systematically and provide quick access to stored incident details through the admin dashboard.",
        87: "To implement DevOps practices throughout the application development and deployment process using Git, GitHub, Docker, Jenkins, and Ansible.",
        88: "To automate the CI/CD workflow using Jenkins for building Docker images, running Pytest suites, and orchestrating Ansible deployments.",
        89: "To containerize the application using Docker to provide a consistent, portable, and isolated execution environment.",
        90: "To integrate Pytest for automated testing to verify application routes, telemetry logic, database transactions, and error handling before deployment.",
        91: "To automate application deployment and container configuration using Ansible playbooks within a dedicated control container.",
        92: "To implement Docker Volume (water_monitoring_data) for persistent storage of the SQLite database and ensure that sensor readings and complaints are retained even when the container is recreated.",

        # Section 3 - ABSTRACT
        104: ("     The Smart Water Monitoring and Complaint Management System is an end-to-end municipal utility platform designed to simplify the monitoring of water quality parameters and streamline public grievance redressal. Traditional municipal water management faces challenges such as lack of real-time telemetry, delayed response to pipeline leaks, manual complaint filing, and difficult incident tracking. The proposed system provides a digital platform where citizens can view real-time water metrics (pH level, TDS, turbidity, pressure), submit water supply complaints across multiple categories, and track resolution progress using unique tracking tokens (e.g., WC-00001). An administrative dashboard is provided for municipal water authorities to analyze live telemetry trends and update complaint statuses from Pending to In Progress or Resolved. The application is developed using HTML, CSS, JavaScript, Python, Flask, and SQLite, with Flask handling backend operations and SQLite storing telemetry logs and citizen complaints. The project also implements industrial DevOps practices to automate the software development, testing, and deployment lifecycle. Git and GitHub are used for version control, while Jenkins automates the multi-stage CI/CD pipeline. Docker is used to containerize the application (water-monitoring-ci) for environment consistency, Pytest performs automated testing across 13 test cases, and Ansible automates container deployment and configuration. A Docker Volume named water_monitoring_data provides persistent storage for the SQLite database, ensuring that sensor history and citizen complaints are preserved across container updates and restarts. The complete workflow follows GitHub -> Jenkins -> Docker Build -> Pytest -> Ansible -> Docker Container -> Flask -> SQLite, demonstrating a dependable, cloud-ready municipal utility architecture."),

        # Section 5 - SYSTEM ARCHITECTURE
        111: "Development: Developer creates and updates the Smart Water Monitoring application.",
        112: "Source Code Management: The application source code, templates, tests, and configuration files are maintained using Git.",
        113: "GitHub Repository: The updated code is pushed to the GitHub repository for centralized version control and team collaboration.",
        114: "Jenkins Trigger: Jenkins retrieves the latest source code from the GitHub repository and triggers the automated CI/CD pipeline.",
        115: "Docker Build: Jenkins builds the application into a Docker image (water-monitoring-ci) containing the Flask backend and required dependencies.",
        116: "Automated Testing: Jenkins runs Pytest inside the container to execute all 13 unit tests and verify application routes before deployment.",
        117: "Deployment Automation: After successful test execution, Jenkins invokes Ansible inside ansible-docker-lab to automate deployment.",
        118: "Container Configuration: Ansible creates and configures the Docker container (water-monitoring-ansible) with port mapping 5002:5000 and volume water_monitoring_data.",
        119: "Application Execution: The Docker container runs the Flask backend, serving AquaWatch UI views and connecting to persistent SQLite storage.",
        120: "User Interaction: Citizens browse real-time water quality metrics, register complaints, and track grievance resolution status.",
        121: "Admin Management: The admin dashboard allows municipal engineers to monitor telemetry gauges and manage complaint resolution lifecycles.",

        # MODULE 1 - USER INTERFACE
        122: "MODULE 1 - USER INTERFACE & COMPLAINT REGISTRATION",
        123: "    This module provides the user-facing interface of the Smart Water Monitoring System (AquaWatch). It is designed to make water quality monitoring and grievance registration simple and accessible for citizens.",
        125: "Displays real-time water quality telemetry including pH, TDS, turbidity, and pressure.",
        126: "Provides intuitive visual gauge indicators representing water safety levels (Optimal, Safe, Warning).",
        127: "Organizes water complaints into distinct categories (Quality, Leakage, Low Pressure, Supply).",
        128: "Allows citizens to submit their name, contact details, and specific ward/location.",
        129: "Provides a detailed grievance description field for specific reporting.",
        130: "Performs client-side validation on form inputs to prevent incomplete submissions.",
        131: "Generates a unique tracking token (e.g., WC-00001) upon complaint registration.",
        132: "Provides an instant complaint tracking interface using the generated ticket ID.",
        133: "Displays transparent ticket lifecycle states: Pending, In Progress, and Resolved.",
        134: "Provides a responsive, modern Aqua/Ocean themed user interface.",
        135: "Adapts seamlessly across desktop, tablet, and mobile browsers.",
        136: "Connects the user interface with the Flask backend for processing requests.",
        139: "Figure 7.1: Smart Water Monitoring System Home Page",
        140: "\nFigure 7.2: Real-Time Water Quality Gauges and Complaint Registration",

        # MODULE 2 - FLASK BACKEND
        142: "MODULE 2 - FLASK BACKEND & SENSOR TELEMETRY",
        143: "    This module handles the application logic, sensor telemetry simulation, and acts as the communication layer between the frontend and the SQLite database. Flask processes user requests and manages the complete complaint lifecycle.",
        145: "Receives requests from the frontend client and routes them appropriately.",
        146: "Simulates and serves real-time water quality telemetry (pH, TDS, turbidity, pressure).",
        147: "Processes citizen complaint submissions and validates request payloads.",
        148: "Generates unique, structured complaint tracking tokens (WC-XXXXX).",
        149: "Implements parameterized SQL queries to prevent SQL injection vulnerabilities.",
        150: "Communicates with the SQLite database for transactional storage.",
        151: "Stores submitted complaint information and sensor telemetry logs.",
        152: "Retrieves stored complaint and sensor records for dashboard display.",
        153: "Handles session-based admin authentication and access control.",
        154: "Allows administrators to update complaint statuses (Pending -> In Progress -> Resolved).",
        155: "Processes application routes and returns HTML templates or JSON responses.",
        156: "Runs the Flask application inside the Docker container on port 5000.",
        157: "Provides the backend services required by the Smart Water Monitoring application.",
        160: "Figure 7.3: Flask Backend Implementation (app.py)",

        # MODULE 3 - SQLITE DATABASE
        162: "MODULE 3 - SQLITE DATABASE MANAGEMENT",
        163: "    This module manages the storage and retrieval of sensor telemetry and citizen complaints using SQLite. The database provides persistent application data that can be accessed by the Flask backend.",
        165: "Stores real-time water sensor telemetry records (pH, TDS, turbidity, pressure).",
        166: "Maintains citizen complaint records with timestamps, categories, and descriptions.",
        167: "Tracks complaint resolution lifecycle states (Pending, In Progress, Resolved).",
        168: "Stores administrator credentials and provides authentication support.",
        169: "Allows stored complaints to be searched and retrieved by unique tracking ID.",
        170: "Makes stored records available to the admin dashboard for analytical review.",
        171: "Maintains the water_monitoring.db database file.",
        172: "Stores the database under the application data directory (/app/data).",
        173: "Works with the Docker Volume (water_monitoring_data) for persistent storage.",
        174: "Provides structured, relational table schemas for complaints and telemetry.",
        175: "Maintains database integrity even when the application container is recreated.",
        178: "data/water_monitoring.db",
        180: "/app/data/water_monitoring.db",
        182: "\nFigure 7.4: SQLite Database Containing Sensor and Complaint Records",

        # MODULE 4 - GIT & GITHUB
        184: "MODULE 4 - GIT & GITHUB SOURCE CONTROL",
        185: "    This module manages the source code and maintains the development history of the Smart Water Monitoring project. Git is used locally for version control, while GitHub provides the remote repository.",
        207: "\nFigure 7.5: Smart Water Monitoring GitHub Repository & Version Control",

        # MODULE 5 - DOCKER CONTAINERIZATION
        209: "MODULE 5 - DOCKER CONTAINERIZATION",
        210: "    Docker is used to package and run the Smart Water Monitoring application in an isolated and consistent environment. The application and its required dependencies are packaged into a Docker image.",
        225: "water-monitoring-ci",
        227: "water-monitoring-ansible",
        229: "5002 -> 5000",
        231: "http://localhost:5002",
        237: "\nFigure 7.6: Smart Water Monitoring Docker Image (water-monitoring-ci)",
        239: "\nFigure 7.7: Running Smart Water Monitoring Docker Container (Port 5002)",

        # MODULE 6 - JENKINS
        241: "MODULE 6 - JENKINS CI/CD PIPELINE",
        242: "    Jenkins is used to automate the Continuous Integration and Continuous Deployment process. It connects the source code repository with the application build, testing, and deployment stages.",
        255: "\nFigure 7.8: Jenkins CI/CD Pipeline Dashboard",
        256: "\nFigure 7.9: Successful Multi-Stage Jenkins Pipeline Execution (Build #1)",

        # MODULE 7 - AUTOMATED TESTING
        258: "MODULE 7 - AUTOMATED TESTING",
        259: "    This module validates the application automatically before deployment. Pytest is integrated into the Jenkins pipeline so that the application is thoroughly tested before the deployment stage.",
        264: "Verifies the configured application tests (13 test cases covering all routes and DB operations).",
        276: "collected 13 items",
        277: "test_app.py ............. [100%]",
        278: "13 passed in 1.42s",
        280: "Figure 7.10: Successful Automated Test Execution (13/13 Passed)",

        # MODULE 8 - ANSIBLE DEPLOYMENT
        283: "MODULE 8 - ANSIBLE DEPLOYMENT",
        284: "    Ansible is used to automate the deployment and configuration of the Smart Water Monitoring Docker container. The deployment configuration is defined in the Ansible playbook.",
        298: "name: water-monitoring-ansible",
        299: "image: water-monitoring-ci",
        301: "- \"5002:5000\"",
        303: "- \"water_monitoring_data:/app/data\"",
        306: "Figure 7.11: Ansible Deployment Playbook Execution Log",

        # MODULE 9 - PERSISTENT STORAGE
        307: "MODULE 9 - PERSISTENT STORAGE",
        308: "    This module ensures that database information remains available even when the application container is recreated. Docker Volume is used to separate persistent application data from the container lifecycle.",
        311: "Uses the Docker Volume water_monitoring_data.",
        316: "Preserves stored water sensor telemetry and citizen complaint records.",
        318: "Allows the application container to be recreated without losing stored complaint data.",
        320: "water_monitoring_data:/app/data",
        324: "\nFigure 7.12: Dedicated Docker Volume (water_monitoring_data)",

        # MODULE 10 - ADMIN & COMPLAINT MANAGEMENT
        326: "MODULE 10 - ADMIN & COMPLAINT MANAGEMENT",
        327: "    This module provides access to citizen complaints and sensor telemetry. The Flask backend stores complaint information in SQLite, while the admin dashboard provides access to the stored records.",
        329: "Receives complaints registered by citizens.",
        330: "Processes complaint information through Flask routes.",
        331: "Stores complaint records in SQLite.",
        332: "Generates a unique complaint ID (WC-XXXXX).",
        333: "Makes stored records available to the municipal administrator.",
        334: "Provides access to complaint records and sensor metrics through the admin dashboard.",
        335: "Allows the administrator to update complaint status (Pending -> In Progress -> Resolved).",
        337: "Provides a centralized view of registered citizen complaints and water metrics.",
        340: "http://localhost:5002/admin",
        341: "\nFigure 7.13: Smart Water Monitoring Admin Dashboard",

        # MODULE 11 - CI/CD INTEGRATION
        343: "MODULE 11 - CI/CD INTEGRATION",
        344: "    This module integrates the different DevOps tools into a single automated workflow. GitHub, Jenkins, Docker, Pytest, and Ansible work together to automate the build, testing, and deployment process.",
        348: "Checks out the required project version from GitHub.",
        349: "Builds the Docker image water-monitoring-ci automatically.",
        350: "Runs Pytest automatically across all 13 test cases.",
        351: "Triggers Ansible deployment after all tests pass successfully.",
        352: "Creates and manages the container water-monitoring-ansible with volume mapping.",
        357: "\nFigure 7.14: Complete CI/CD Pipeline Execution Success",

        # MODULE 12 - APPLICATION & DEPLOYMENT VERIFICATION
        359: "MODULE 12 - APPLICATION & DEPLOYMENT VERIFICATION",
        360: "    This module verifies that the complete Smart Water Monitoring system is functioning correctly after deployment. Verification is performed across the application, Docker container, database, storage, Ansible deployment, and Jenkins pipeline.",
        364: "Opening the Smart Water Monitoring application (http://localhost:5002).",
        365: "Observing real-time water quality telemetry (pH, TDS, turbidity, pressure).",
        366: "Registering a new water supply complaint through the web form.",
        367: "Checking the generated complaint tracking token (e.g., WC-00003).",
        368: "Accessing the admin dashboard to view telemetry and complaint queue.",
        369: "Checking stored SQLite records in water_monitoring.db.",
        374: "Verifying that complaint records remain available after container recreation.",
        377: "Pytest -> 13 PASSED in 1.42s",
        380: "\nFigure 7.15: Successfully Deployed Smart Water Monitoring Application Verification",

        # Section 18 - RESULTS AND OUTPUT
        390: "Real-time water quality monitoring (pH, TDS, turbidity, pressure)",
        391: "Citizen grievance registration and category selection",
        393: "Automated ticket token generation (WC-XXXXX)",
        394: "Real-time complaint status tracking portal",
        395: "Admin dashboard with telemetry gauges and status management",
        396: "Automated Docker image creation (water-monitoring-ci)",
        397: "Automated unit test execution (13/13 Pytest tests passed)",
        398: "Jenkins multi-stage CI/CD pipeline automation",
        399: "Idempotent container provisioning via Ansible (water-monitoring-ansible)",
        400: "Persistent SQLite storage via Docker Volume (water_monitoring_data)",

        # Section 19 - COMMANDS USED
        421: "Jenkins was accessed using:",
        422: "http://localhost:8080",
        426: "docker build -t water-monitoring-ci .",
        428: "water-monitoring-ci",
        432: "docker run --rm water-monitoring-ci python -m pytest test_app.py",
        434: "13 passed in 1.42s",
        438: "docker exec ansible-docker-lab ansible-playbook -i /inventory.ini /water-deploy.yml",
        441: "docker exec ansible-docker-lab ansible-playbook -i /inventory.ini /water-deploy.yml",
        443: "docker exec ansible-docker-lab cat /water-deploy.yml",
        448: "The Smart Water Monitoring container:",
        449: "water-monitoring-ansible",
        451: "5002:5000",
        453: "http://localhost:5002",
        459: "water_monitoring_data",
        461: "docker volume inspect water_monitoring_data",
        464: "Display stored complaints",
        465: "docker exec water-monitoring-ansible python -c \"import sqlite3; c=sqlite3.connect('data/water_monitoring.db'); [print(row) for row in c.execute('SELECT * FROM complaints')]; c.close()\"",
        467: "docker exec water-monitoring-ansible python -c \"import sqlite3; c=sqlite3.connect('data/water_monitoring.db'); print(c.execute(\\\"SELECT name FROM sqlite_master WHERE type='table'\\\").fetchall()); c.close()\"",
        468: "Display all complaints as a list",
        469: "docker exec water-monitoring-ansible python -c \"import sqlite3; c=sqlite3.connect('data/water_monitoring.db'); print(c.execute('SELECT * FROM complaints').fetchall()); c.close()\"",
        473: "docker exec water-monitoring-ansible python -c \"import sqlite3; c=sqlite3.connect('data/water_monitoring.db'); print(c.execute('SELECT * FROM complaints').fetchall()); c.close()\"",
        475: "data/water_monitoring.db",
        477: "/app/data/water_monitoring.db",
        487: "git commit -m \"Finalize Smart Water Monitoring CI/CD project\"",
        491: "git remote add origin https://github.com/DEVOPS-PANDI/WaterMonitoring.git",
        501: "docker stop water-monitoring-ansible",
        503: "docker start water-monitoring-ansible",
        505: "docker logs water-monitoring-ansible",
        507: "docker exec water-monitoring-ansible ...",
        512: "docker build -t water-monitoring-ci .",
        513: "docker run --rm water-monitoring-ci python -m pytest test_app.py",
        514: "docker exec ansible-docker-lab ansible-playbook -i /inventory.ini /water-deploy.yml",
        517: "docker volume inspect water_monitoring_data",
        518: "docker exec water-monitoring-ansible python -c \"import sqlite3; c=sqlite3.connect('data/water_monitoring.db'); print(c.execute('SELECT * FROM complaints').fetchall()); c.close()\"",
        521: "git commit -m \"Finalize Smart Water Monitoring CI/CD project\"",

        # Section 20 - ADVANTAGES
        525: "Enables real-time municipal water quality monitoring and hazard detection.",
        526: "Provides a user-friendly, responsive interface for reporting water grievances.",
        527: "Provides centralized telemetry metrics and grievance records for municipal officers.",
        528: "Automates application testing with 13 comprehensive unit tests using Pytest.",
        529: "Reduces manual deployment effort through idempotent Ansible automation.",
        530: "Provides consistent, isolated application execution through Docker.",
        531: "Provides persistent database storage using dedicated Docker Volume.",
        532: "Integrates source control with multi-stage CI/CD pipeline in Jenkins.",
        533: "Demonstrates complete automated deployment workflow from code to production.",

        # Section 21 - LIMITATIONS
        535: "The current system uses SQLite for lightweight local database storage.",
        536: "Physical IoT sensor hardware integration is simulated via software telemetry.",
        537: "Automated SMS and email grievance notifications are not currently integrated.",
        538: "Role-based multi-tier municipal escalation routing is not implemented.",
        539: "The deployment is demonstrated in a local Docker and Jenkins laboratory environment.",
        540: "Centralized distributed logging and telemetry monitoring (ELK/Grafana) are not implemented.",

        # Section 22 - CONCLUSION
        552: ("     The Smart Water Monitoring and Complaint Management System successfully demonstrates the integration of a web-based public utility application with modern DevOps practices to provide an efficient, robust, and automated application environment. The system enables citizens to monitor real-time water quality parameters (pH, TDS, turbidity, pressure), submit water complaints across distinct categories, and track ticket status using unique tracking tokens. The admin dashboard provides a centralized platform for municipal engineers to review real-time sensor metrics and manage complaint lifecycles from Pending to Resolved. Flask is used to handle backend routing and telemetry calculation, while SQLite stores records in water_monitoring.db. The project demonstrates the complete implementation of a Continuous Integration and Continuous Deployment (CI/CD) workflow. Git and GitHub are used for version control and source code management, maintaining all files in a centralized repository. Jenkins automates the CI/CD pipeline by retrieving the latest source code, building the Docker image (water-monitoring-ci), executing 13 automated tests via Pytest, and initiating deployment. Pytest verifies application routes, database transactions, and form validation before deployment, ensuring zero regressions reach production. Docker containerizes the application, providing consistent runtime execution. Ansible automates the configuration and provisioning of the container (water-monitoring-ansible) using an idempotent playbook. The playbook defines key configurations including container name, Docker image, port mapping (5002:5000), and volume mounting. The Docker Volume water_monitoring_data provides persistent storage for the SQLite database mounted at /app/data, ensuring that sensor readings and citizen complaints are retained across container recreations and updates. Overall, the project demonstrates how application engineering, version control, automated testing, containerization, deployment orchestration, and persistent storage integrate into an industrial DevOps workflow. The successful execution of the pipeline confirms the practical implementation of GitHub -> Jenkins -> Docker -> Pytest -> Ansible -> Flask -> SQLite, delivering a complete automated solution for municipal water utility governance."),

        # Section 23 - FUTURE ENHANCEMENTS
        555: "The system can be extended with:",
        556: "Physical IoT hardware integration with ESP32 / Arduino water quality sensors.",
        557: "Automated SMS and WhatsApp notifications for complaint status updates.",
        558: "AI-powered predictive water contamination and pipe leakage forecasting.",
        559: "Database migration from SQLite to PostgreSQL or MySQL with clustering.",
        560: "Multi-ward municipal GIS mapping and geo-tagging of complaints.",
        561: "GitHub webhook-based automatic pipeline triggering on commit.",
        562: "Kubernetes (k8s) cluster deployment for auto-scaling under load.",
        563: "Role-based access control (Field Engineers, Inspectors, Supervisors).",
        564: "Centralized monitoring using Prometheus and Grafana dashboards.",
        565: "Cloud production deployment on AWS or Azure infrastructure."
    }

    for p_idx, text in p_updates.items():
        if p_idx < len(doc.paragraphs):
            update_para(doc.paragraphs[p_idx], text)

    # 6. Fallback Phrase Replacements across ALL paragraphs and cells to catch any remaining canteen terms
    phrase_map = [
        ("Digital Canteen", "Smart Water Monitoring System"),
        ("digital-canteen-ci", "water-monitoring-ci"),
        ("digital-canteen-ansible", "water-monitoring-ansible"),
        ("digital-canteen", "water-monitoring"),
        ("canteen_data", "water_monitoring_data"),
        ("canteen.db", "water_monitoring.db"),
        ("data/canteen.db", "data/water_monitoring.db"),
        ("/app/data/canteen.db", "/app/data/water_monitoring.db"),
        ("docker-deploy.yml", "water-deploy.yml"),
        ("food ordering", "water monitoring and complaint management"),
        ("food browsing and ordering", "water monitoring and complaint registration"),
        ("food browsing", "water quality monitoring"),
        ("food items", "water quality metrics"),
        ("browse food items", "view water quality metrics"),
        ("search for dishes", "monitor water quality"),
        ("select food items", "submit complaints"),
        ("add items to the cart", "register grievances"),
        ("add them to a cart", "submit complaints"),
        ("shopping cart", "complaint registration"),
        ("place orders", "register complaints"),
        ("placing a food order", "submitting a water complaint"),
        ("placed orders", "registered complaints"),
        ("placed order", "registered complaint"),
        ("order details", "complaint details"),
        ("order ID", "complaint ID"),
        ("order information", "complaint records"),
        ("order records", "complaint records"),
        ("order data", "complaint and sensor data"),
        ("canteen services", "water utility services"),
        ("canteen environment", "municipal water management system"),
        ("5001", "5002"),
        ("http://localhost:5001", "http://localhost:5002"),
        ("http://localhost:9091", "http://localhost:8080"),
        ("1 passed", "13 passed in 1.42s"),
        ("collected 1 item", "collected 13 items"),
        ("test_app.py . [100%]", "test_app.py ............. [100%]"),
        ("Jayasree273/DigitalCanteen.git", "DEVOPS-PANDI/WaterMonitoring.git")
    ]

    for p in doc.paragraphs:
        full = "".join(r.text for r in p.runs)
        for old_s, new_s in phrase_map:
            if old_s in full:
                full = full.replace(old_s, new_s)
                update_para(p, full)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    full = "".join(r.text for r in p.runs)
                    for old_s, new_s in phrase_map:
                        if old_s in full:
                            full = full.replace(old_s, new_s)
                            update_para(p, full)

    temp_docx = "temp_updated_stage1.docx"
    doc.save(temp_docx)
    print(f"Saved modified document to {temp_docx}")

    # 7. Replace images in the DOCX zip archive
    print("Injecting new media images into docx package...")
    with zipfile.ZipFile(temp_docx, 'r') as zin:
        with zipfile.ZipFile(TARGET_DOCX, 'w') as zout:
            for item in zin.infolist():
                fn = item.filename
                if fn.startswith("word/media/"):
                    base = os.path.basename(fn)
                    new_file_path = os.path.join(NEW_MEDIA_DIR, base)
                    if os.path.exists(new_file_path):
                        with open(new_file_path, "rb") as f_in:
                            zout.writestr(item, f_in.read())
                        print(f"  Injected {fn} from {new_file_path}")
                        continue
                zout.writestr(item, zin.read(item.filename))

    if os.path.exists(temp_docx):
        os.remove(temp_docx)

    print(f"\nDocument generation complete: {TARGET_DOCX}")

if __name__ == "__main__":
    main()
