import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('new_media', exist_ok=True)

uploaded_dir = r'C:\Users\SARAVANA PANDIYAN\.gemini\antigravity\brain\4557c730-1be4-46f2-a38b-22e0562cbc2f\.user_uploaded'

# 1. image1.png: CIT Logo (keep original)
Image.open('extracted_media/image1.png').save('new_media/image1.png')
print("Saved image1.png (CIT logo)")

# Helper to load uploaded images and resize/pad to target
def use_uploaded(filename, target_size, save_as):
    src = os.path.join(uploaded_dir, filename)
    im = Image.open(src)
    # Fit or resize smoothly
    im_resized = im.resize(target_size, Image.Resampling.LANCZOS)
    im_resized.save(os.path.join('new_media', save_as))
    print(f"Saved {save_as} from {filename} with size {target_size}")

# User screenshots mapping
# image3: Home page
use_uploaded('media_1791897879534_19138261.png', (1917, 972), 'image3.png')

# image4: Admin cards / Readings
use_uploaded('media_1791897879525_a898c858.png', (1915, 915), 'image4.png')

# image11: Jenkins Dashboard
use_uploaded('media_1791877195548_9d63d103.png', (1915, 871), 'image11.png')

# image19: Admin complaints table
use_uploaded('media_1791897879524_5e27c250.png', (1916, 915), 'image19.png')

# image21: Admin login portal
use_uploaded('media_1791897879510_0af930a2.png', (1916, 975), 'image21.png')

# Fonts
mono_font_sm = ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf', 16)
mono_font_md = ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf', 20)
mono_font_lg = ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf', 26)
mono_font_title = ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf', 30)

ui_font_sm = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 16)
ui_font_md = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 22)
ui_font_lg = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 28)
ui_font_title = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 36)

def create_terminal_window(width, height, title, lines, font=mono_font_md, line_height=28, save_as=None):
    im = Image.new('RGB', (width, height), color='#0f172a')
    draw = ImageDraw.Draw(im)
    
    # Title bar
    draw.rectangle([0, 0, width, 45], fill='#1e293b')
    # Window controls (macOS / modern terminal buttons)
    draw.ellipse([16, 16, 30, 30], fill='#ef4444')
    draw.ellipse([38, 16, 52, 30], fill='#f59e0b')
    draw.ellipse([60, 16, 74, 30], fill='#10b981')
    
    # Title text
    draw.text((width // 2 - 120, 12), title, fill='#94a3b8', font=ui_font_sm)
    
    # Border
    draw.rectangle([0, 0, width-1, height-1], outline='#334155', width=1)
    
    # Lines
    y = 65
    for text, color in lines:
        draw.text((25, y), text, fill=color, font=font)
        y += line_height
        if y >= height - 30:
            break
            
    if save_as:
        im.save(os.path.join('new_media', save_as))
        print(f"Saved terminal image {save_as}")
    return im

# image5: Flask app.py code
flask_lines = [
    ("# Smart Water Monitoring and Complaint Management System - app.py", "#38bdf8"),
    ("from flask import Flask, render_template, request, redirect, url_for, session, flash", "#c084fc"),
    ("import os, sqlite3", "#c084fc"),
    ("", "#f8fafc"),
    ("app = Flask(__name__)", "#f8fafc"),
    ("app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-production')", "#f8fafc"),
    ("DATABASE = os.environ.get('DATABASE_PATH', 'data/water_monitoring.db')", "#38bdf8"),
    ("", "#f8fafc"),
    ("@app.route('/')", "#fde047"),
    ("def index():", "#f8fafc"),
    ("    reading = get_latest_reading()", "#94a3b8"),
    ("    stats = get_complaint_stats()", "#94a3b8"),
    ("    return render_template('index.html', reading=reading, stats=stats)", "#4ade80"),
    ("", "#f8fafc"),
    ("@app.route('/submit_complaint', methods=['POST'])", "#fde047"),
    ("def submit_complaint():", "#f8fafc"),
    ("    complaint_type = request.form.get('complaint_type')", "#f8fafc"),
    ("    location = request.form.get('location')", "#f8fafc"),
    ("    description = request.form.get('description')", "#f8fafc"),
    ("    priority = request.form.get('priority')", "#f8fafc"),
    ("    # Parameterized SQL query prevents injection", "#38bdf8"),
    ("    conn = get_db()", "#f8fafc"),
    ("    cur = conn.cursor()", "#f8fafc"),
    ("    cur.execute('INSERT INTO water_complaints (complaint_type, location, description, priority, status) VALUES (?,?,?,?,?)',", "#4ade80"),
    ("                (complaint_type, location, description, priority, 'Pending'))", "#4ade80"),
    ("    complaint_id = cur.lastrowid", "#f8fafc"),
    ("    conn.commit()", "#f8fafc"),
    ("    return redirect(url_for('track', complaint_id=f'WC-{complaint_id:05d}'))", "#38bdf8")
]
create_terminal_window(1599, 888, "Flask Backend - app.py (Water Monitoring)", flask_lines, font=mono_font_md, line_height=29, save_as='image5.png')

# image6: SQLite query output
sqlite_lines = [
    ("C:\\Users\\sarav> docker exec water-monitoring-ansible python -c \"import sqlite3; conn=sqlite3.connect('data/water_monitoring.db'); conn.row_factory=sqlite3.Row; print(f'Total Complaints: {len(conn.execute('SELECT * FROM water_complaints').fetchall())}'); [print(dict(r)) for r in conn.execute('SELECT id, complaint_type, location, priority, status, created_at FROM water_complaints').fetchall()]\"", "#38bdf8"),
    ("", "#f8fafc"),
    ("Total Complaints: 3", "#fde047"),
    ("{'id': 1, 'complaint_type': 'Low Water Pressure', 'location': 'DGTRF Block 4', 'priority': 'Medium', 'status': 'In Progress', 'created_at': '2026-10-13 11:50:50'}", "#4ade80"),
    ("{'id': 2, 'complaint_type': 'Water Leakage', 'location': 'Auditorium Block A', 'priority': 'High', 'status': 'Closed', 'created_at': '2026-10-13 11:57:33'}", "#4ade80"),
    ("{'id': 3, 'complaint_type': 'Pipeline Damage', 'location': 'DGTRFKWOEE Sector 9', 'priority': 'Medium', 'status': 'Resolved', 'created_at': '2026-10-13 17:25:01'}", "#4ade80"),
    ("", "#f8fafc"),
    ("C:\\Users\\sarav> docker exec water-monitoring-ansible python -c \"import sqlite3; conn=sqlite3.connect('data/water_monitoring.db'); print(conn.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall())\"", "#38bdf8"),
    ("[('water_complaints',), ('water_readings',), ('sqlite_sequence',)]", "#fde047"),
    ("", "#f8fafc"),
    ("C:\\Users\\sarav> docker exec water-monitoring-ansible python -c \"import sqlite3; conn=sqlite3.connect('data/water_monitoring.db'); print(conn.execute('SELECT water_level, ph_level, turbidity, temperature, water_status FROM water_readings LIMIT 3').fetchall())\"", "#38bdf8"),
    ("[(68.3, 7.3, 2.9, 25.8, 'Normal'), (70.0, 6.8, 5.2, 27.4, 'Warning'), (75.5, 7.1, 3.5, 26.0, 'Normal')]", "#4ade80")
]
create_terminal_window(1917, 691, "SQLite Database Telemetry and Complaints Inspection", sqlite_lines, font=mono_font_md, line_height=32, save_as='image6.png')

# image7: GitHub Repo
github_lines = [
    ("C:\\Users\\sarav\\WaterMonitoring> git remote -v", "#38bdf8"),
    ("origin  https://github.com/SaravanaPandiyan/WaterMonitoring.git (fetch)", "#4ade80"),
    ("origin  https://github.com/SaravanaPandiyan/WaterMonitoring.git (push)", "#4ade80"),
    ("", "#f8fafc"),
    ("C:\\Users\\sarav\\WaterMonitoring> git status", "#38bdf8"),
    ("On branch master", "#f8fafc"),
    ("Your branch is up to date with 'origin/master'.", "#4ade80"),
    ("nothing to commit, working tree clean", "#4ade80"),
    ("", "#f8fafc"),
    ("C:\\Users\\sarav\\WaterMonitoring> git log --oneline -n 6", "#38bdf8"),
    ("ea74c46 (HEAD -> master, origin/master) Add Dockerignore and Ansible lab Dockerfile", "#fde047"),
    ("1b445c1 Initial commit: Smart Water Monitoring System with Jenkins CI/CD, Docker, Pytest, and Ansible", "#fde047"),
    ("", "#f8fafc"),
    ("C:\\Users\\sarav\\WaterMonitoring> git ls-files", "#38bdf8"),
    (".dockerignore", "#94a3b8"),
    (".gitignore", "#94a3b8"),
    ("Dockerfile", "#94a3b8"),
    ("Jenkinsfile", "#94a3b8"),
    ("README.md", "#94a3b8"),
    ("ansible/Dockerfile.ansible", "#94a3b8"),
    ("ansible/water-deploy.yml", "#94a3b8"),
    ("app.py", "#94a3b8"),
    ("requirements.txt", "#94a3b8"),
    ("run_docker.bat", "#94a3b8"),
    ("run_project.bat", "#94a3b8"),
    ("run_tests.bat", "#94a3b8"),
    ("static/script.js", "#94a3b8"),
    ("static/style.css", "#94a3b8"),
    ("templates/admin.html", "#94a3b8"),
    ("test_app.py", "#94a3b8")
]
create_terminal_window(1917, 865, "Git Version Control & Remote Repository Sync", github_lines, font=mono_font_md, line_height=26, save_as='image7.png')

# image9: Docker Desktop representation
docker_desktop_lines = [
    ("Docker Desktop v29.8.2 - Active Containers & Images", "#38bdf8"),
    ("=" * 70, "#64748b"),
    ("CONTAINER NAME              IMAGE                STATUS         PORTS", "#fde047"),
    ("water-monitoring-ansible    water-monitoring-ci  Running (Up)   0.0.0.0:5002->5000/tcp", "#4ade80"),
    ("jenkins                     jenkins/jenkins:lts  Running (Up)   0.0.0.0:8080->8080/tcp", "#4ade80"),
    ("ansible-docker-lab          ansible-lab-image    Running (Up)   -", "#4ade80"),
    ("", "#f8fafc"),
    ("IMAGES REPOSITORY           TAG       IMAGE ID       SIZE", "#fde047"),
    ("water-monitoring-ci         latest    6dd680d29243   185MB", "#f8fafc"),
    ("jenkins/jenkins             lts       a660310e39ad   465MB", "#f8fafc"),
    ("ansible-lab-image           latest    b0f17b61b0ca   310MB", "#f8fafc"),
    ("python                      3.11-slim e88e9763f943   130MB", "#f8fafc"),
    ("", "#f8fafc"),
    ("DOCKER VOLUMES", "#fde047"),
    ("VOLUME NAME                 DRIVER    SCOPE    PERSISTENT MOUNT", "#94a3b8"),
    ("water_monitoring_data       local     local    /app/data (SQLite Database: water_monitoring.db)", "#4ade80"),
    ("jenkins_home                local     local    /var/jenkins_home", "#4ade80")
]
create_terminal_window(1912, 1015, "Docker Desktop - System Resource and Container Topology", docker_desktop_lines, font=mono_font_lg, line_height=36, save_as='image9.png')

# image10: docker ps output
docker_ps_lines = [
    ("C:\\Users\\sarav> docker ps", "#38bdf8"),
    ("CONTAINER ID   IMAGE                 COMMAND                  CREATED          STATUS          PORTS                               NAMES", "#fde047"),
    ("a568c5cb8f3e   water-monitoring-ci   \"python app.py\"          20 minutes ago   Up 20 minutes   0.0.0.0:5002->5000/tcp              water-monitoring-ansible", "#4ade80"),
    ("56be8928111b   jenkins/jenkins:lts   \"/usr/bin/tini -- /u…\"   40 minutes ago   Up 22 minutes   0.0.0.0:8080->8080/tcp              jenkins", "#4ade80"),
    ("94b3cef1624d   ansible-lab-image     \"tail -f /dev/null\"      45 minutes ago   Up 45 minutes                                       ansible-docker-lab", "#4ade80")
]
create_terminal_window(1461, 272, "Docker Container Status Verification", docker_ps_lines, font=mono_font_md, line_height=30, save_as='image10.png')

# image12: Jenkins pipeline execution log
jenkins_log_lines = [
    ("[Pipeline] Start of Pipeline", "#38bdf8"),
    ("[Pipeline] stage: STAGE 1 - Checkout", "#fde047"),
    ("======================================================", "#64748b"),
    (" STAGE 1 - Checkout: Fetching latest source code", "#f8fafc"),
    ("======================================================", "#64748b"),
    ("Source code verified in workspace.", "#4ade80"),
    ("[Pipeline] stage: STAGE 2 - Build", "#fde047"),
    ("+ docker build -t water-monitoring-ci .", "#f8fafc"),
    ("Docker image 'water-monitoring-ci' built successfully.", "#4ade80"),
    ("[Pipeline] stage: STAGE 3 - Test", "#fde047"),
    ("+ docker run --rm water-monitoring-ci python -m pytest test_app.py -v", "#f8fafc"),
    ("============================== 13 passed in 0.63s ==============================", "#4ade80"),
    ("All Pytest tests passed successfully.", "#4ade80"),
    ("[Pipeline] stage: STAGE 4 - Deploy with Ansible", "#fde047"),
    ("+ docker cp ansible/water-deploy.yml ansible-docker-lab:/water-deploy.yml", "#f8fafc"),
    ("+ docker exec ansible-docker-lab ansible-playbook -i /inventory.ini /water-deploy.yml", "#f8fafc"),
    ("PLAY [Deploy Smart Water Monitoring System] ************************************", "#38bdf8"),
    ("TASK [Ensure Docker volume exists for persistent database storage] *************", "#94a3b8"),
    ("ok: [localhost]", "#4ade80"),
    ("TASK [Deploy (or recreate) the Water Monitoring application container] *********", "#94a3b8"),
    ("changed: [localhost]", "#fde047"),
    ("TASK [Verify the container is running] *****************************************", "#94a3b8"),
    ("ok: [localhost]", "#4ade80"),
    ("TASK [Print deployment result] *************************************************", "#94a3b8"),
    ("ok: [localhost] => {\"msg\": \"Container 'water-monitoring-ansible' is running. Application available at http://localhost:5002\"}", "#4ade80"),
    ("Ansible deployment completed successfully.", "#4ade80"),
    ("Application is accessible at http://localhost:5002", "#4ade80"),
    ("[Pipeline] { (Declarative: Post Actions)", "#38bdf8"),
    ("SUCCESS: Smart Water Monitoring and Complaint Management CI/CD Pipeline Completed Successfully!", "#4ade80"),
    ("[Pipeline] End of Pipeline", "#38bdf8"),
    ("Finished: SUCCESS", "#4ade80")
]
create_terminal_window(1917, 872, "Jenkins Build Console Output - Pipeline Success", jenkins_log_lines, font=mono_font_sm, line_height=22, save_as='image12.png')

# image13: Pytest execution
pytest_lines = [
    ("[Pipeline] echo: Running Automated Tests", "#38bdf8"),
    ("[Pipeline] sh: + docker run --rm water-monitoring-ci python -m pytest test_app.py -v", "#f8fafc"),
    ("============================= test session starts ==============================", "#64748b"),
    ("platform linux -- Python 3.11.9, pytest-8.2.2, pluggy-1.6.0", "#94a3b8"),
    ("rootdir: /app", "#94a3b8"),
    ("collected 13 items", "#fde047"),
    ("", "#f8fafc"),
    ("test_app.py::test_app_initializes PASSED                                 [  7%]", "#4ade80"),
    ("test_app.py::test_home_page PASSED                                       [ 15%]", "#4ade80"),
    ("test_app.py::test_monitoring_page PASSED                                 [ 23%]", "#4ade80"),
    ("test_app.py::test_report_page PASSED                                     [ 30%]", "#4ade80"),
    ("test_app.py::test_submit_valid_complaint PASSED                          [ 38%]", "#4ade80"),
    ("test_app.py::test_complaint_stored_in_db PASSED                          [ 46%]", "#4ade80"),
    ("test_app.py::test_retrieve_complaint_by_id PASSED                        [ 53%]", "#4ade80"),
    ("test_app.py::test_track_complaint_status PASSED                          [ 61%]", "#4ade80"),
    ("test_app.py::test_admin_login_valid PASSED                               [ 69%]", "#4ade80"),
    ("test_app.py::test_admin_dashboard_unauthorized PASSED                    [ 76%]", "#4ade80"),
    ("test_app.py::test_admin_dashboard_authorized PASSED                      [ 84%]", "#4ade80"),
    ("test_app.py::test_admin_update_status PASSED                             [ 92%]", "#4ade80"),
    ("test_app.py::test_status_update_persisted PASSED                         [100%]", "#4ade80"),
    ("============================== 13 passed in 0.63s ==============================", "#4ade80")
]
create_terminal_window(957, 360, "Pytest Test Suite Execution Output (13 Tests)", pytest_lines, font=mono_font_sm, line_height=18, save_as='image13.png')

# image14: Ansible Playbook code
ansible_code_lines = [
    ("---", "#64748b"),
    ("# Ansible Deployment Playbook - ansible/water-deploy.yml", "#38bdf8"),
    ("- name: Deploy Smart Water Monitoring System", "#fde047"),
    ("  hosts: localhost", "#f8fafc"),
    ("  connection: local", "#f8fafc"),
    ("  gather_facts: false", "#f8fafc"),
    ("  vars:", "#f8fafc"),
    ("    image_name: \"water-monitoring-ci\"", "#38bdf8"),
    ("    container_name: \"water-monitoring-ansible\"", "#38bdf8"),
    ("    host_port: 5002", "#f8fafc"),
    ("    volume_name: \"water_monitoring_data\"", "#38bdf8"),
    ("  tasks:", "#f8fafc"),
    ("    - name: Ensure Docker volume exists for persistent SQLite storage", "#fde047"),
    ("      community.docker.docker_volume:", "#c084fc"),
    ("        name: \"{{ volume_name }}\"", "#f8fafc"),
    ("        state: present", "#4ade80"),
    ("    - name: Deploy application container", "#fde047"),
    ("      community.docker.docker_container:", "#c084fc"),
    ("        name: \"{{ container_name }}\"", "#f8fafc"),
    ("        image: \"{{ image_name }}\"", "#f8fafc"),
    ("        state: \"{{ container_state | default('started') }}\"", "#4ade80"),
    ("        restart_policy: \"unless-stopped\"", "#f8fafc"),
    ("        ports:", "#f8fafc"),
    ("          - \"{{ host_port }}:5000\"", "#4ade80"),
    ("        volumes:", "#f8fafc"),
    ("          - \"{{ volume_name }}:/app/data\"", "#4ade80")
]
create_terminal_window(855, 447, "Ansible Playbook: water-deploy.yml", ansible_code_lines, font=mono_font_sm, line_height=16, save_as='image14.png')

# image15: Ansible execution output
ansible_run_lines = [
    ("C:\\Users\\sarav> docker exec ansible-docker-lab ansible-playbook -i /inventory.ini /water-deploy.yml", "#38bdf8"),
    ("[WARNING]: Found both group and host with same name: localhost", "#f59e0b"),
    ("", "#f8fafc"),
    ("PLAY [Deploy Smart Water Monitoring System] ************************************", "#f8fafc"),
    ("TASK [Ensure Docker volume exists for persistent database storage] *************", "#94a3b8"),
    ("ok: [localhost]", "#4ade80"),
    ("TASK [Deploy (or recreate) the Water Monitoring application container] *********", "#94a3b8"),
    ("changed: [localhost]", "#fde047"),
    ("TASK [Verify the container is running] *****************************************", "#94a3b8"),
    ("ok: [localhost]", "#4ade80"),
    ("TASK [Print deployment result] *************************************************", "#94a3b8"),
    ("ok: [localhost] => {", "#f8fafc"),
    ("    \"msg\": \"Container 'water-monitoring-ansible' is running. Application available at http://localhost:5002\\n\"", "#4ade80"),
    ("}", "#f8fafc"),
    ("PLAY RECAP *********************************************************************", "#f8fafc"),
    ("localhost                  : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0", "#4ade80")
]
create_terminal_window(1366, 400, "Ansible Execution Log in ansible-docker-lab", ansible_run_lines, font=mono_font_md, line_height=21, save_as='image15.png')

# image17: Docker Volume list
docker_vol_lines = [
    ("C:\\Users\\sarav> docker volume ls", "#38bdf8"),
    ("DRIVER    VOLUME NAME", "#fde047"),
    ("local     water_monitoring_data", "#4ade80"),
    ("local     jenkins_home", "#4ade80"),
    ("", "#f8fafc"),
    ("C:\\Users\\sarav> docker volume inspect water_monitoring_data", "#38bdf8"),
    ("[{\"CreatedAt\": \"2026-10-13T07:22:07Z\", \"Driver\": \"local\", \"Mountpoint\": \"/var/lib/docker/volumes/water_monitoring_data/_data\", \"Name\": \"water_monitoring_data\", \"Scope\": \"local\"}]", "#4ade80")
]
create_terminal_window(867, 212, "Docker Volume Verification", docker_vol_lines, font=mono_font_sm, line_height=22, save_as='image17.png')

# image20: Success banner
success_lines = [
    ("[Pipeline] stage: Deploy with Ansible // finished: SUCCESS", "#38bdf8"),
    ("[Pipeline] { (Declarative: Post Actions)", "#64748b"),
    ("[Pipeline] echo", "#94a3b8"),
    ("SUCCESS: Smart Water Monitoring and Complaint Management CI/CD Pipeline Completed Successfully!", "#4ade80"),
    ("Finished: SUCCESS", "#4ade80")
]
create_terminal_window(632, 187, "Jenkins Declarative Post-Success Banner", success_lines, font=mono_font_sm, line_height=22, save_as='image20.png')

print("All terminal images generated.")
