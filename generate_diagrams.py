import os
from PIL import Image, ImageDraw, ImageFont

NEW_MEDIA_DIR = "new_media"
os.makedirs(NEW_MEDIA_DIR, exist_ok=True)

def draw_rounded_rect(draw, box, radius, fill, outline=None, width=1):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def draw_arrow(draw, start, end, fill="#1e293b", width=3, arrow_size=10):
    x0, y0 = start
    x1, y1 = end
    draw.line([x0, y0, x1, y1], fill=fill, width=width)
    import math
    angle = math.atan2(y1 - y0, x1 - x0)
    angle1 = angle + math.pi * 5 / 6
    angle2 = angle - math.pi * 5 / 6
    p1 = (x1 + arrow_size * math.cos(angle1), y1 + arrow_size * math.sin(angle1))
    p2 = (x1 + arrow_size * math.cos(angle2), y1 + arrow_size * math.sin(angle2))
    draw.polygon([ (x1, y1), p1, p2 ], fill=fill)

# ==========================================
# DIAGRAM 1: image2.png (837 x 552) -> Architecture Diagram
# ==========================================
def generate_image2():
    w, h = 1674, 1104 # 2x for antialiasing
    img = Image.new("RGBA", (w, h), "#ffffff")
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype("segoeuib.ttf", 36)
    f_sub = ImageFont.truetype("segoeui.ttf", 22)
    f_card_hdr = ImageFont.truetype("segoeuib.ttf", 20)
    f_card_bold = ImageFont.truetype("segoeuib.ttf", 18)
    f_card_body = ImageFont.truetype("segoeui.ttf", 16)
    f_card_code = ImageFont.truetype("consola.ttf", 15)
    f_badge = ImageFont.truetype("segoeuib.ttf", 15)

    # Top banner
    draw_rounded_rect(draw, (40, 20, w - 40, 110), 16, fill="#0f2b48")
    draw.text((w // 2, 45), "SMART WATER MONITORING SYSTEM - ARCHITECTURE DIAGRAM", font=f_title, fill="#ffffff", anchor="mm")
    draw.text((w // 2, 85), "End-to-End DevOps CI/CD Pipeline with Docker, Jenkins, Ansible & Persistent SQLite", font=f_sub, fill="#38bdf8", anchor="mm")

    # 6 Top Column Boxes: y: 130 to 520
    cols = [
        {
            "num": "1. DEVELOPMENT", "bg": "#f0fdf4", "border": "#86efac", "hdr_bg": "#dcfce7", "hdr_col": "#166534",
            "title": "Developer (Local)", "badge": "Saravana Pandiyan",
            "bullets": ["Flask Application Dev", "AquaWatch UI Templates", "SQLite DB Schema", "Pytest Suite Creation", "Local testing on :5000"]
        },
        {
            "num": "2. SOURCE CONTROL", "bg": "#f8fafc", "border": "#cbd5e1", "hdr_bg": "#e2e8f0", "hdr_col": "#1e293b",
            "title": "GitHub Repository", "badge": "DEVOPS-PANDI",
            "bullets": ["Version Controlled Code", "Branches: main / master", "Jenkinsfile & Playbooks", ".gitignore excludes DB", "Webhook / Poll SCM"]
        },
        {
            "num": "3. CI PIPELINE", "bg": "#eff6ff", "border": "#93c5fd", "hdr_bg": "#dbeafe", "hdr_col": "#1e40af",
            "title": "Jenkins Automation", "badge": "Port :8080",
            "bullets": ["Stage 1: Checkout SCM", "Stage 2: Build Image", "Stage 3: Run Pytest (13/13)", "Stage 4: Ansible Deploy", "Automated Quality Gate"]
        },
        {
            "num": "4. CONFIGURATION", "bg": "#fffbeb", "border": "#fde68a", "hdr_bg": "#fef3c7", "hdr_col": "#92400e",
            "title": "Ansible Lab", "badge": "ansible-docker-lab",
            "bullets": ["Playbook: water-deploy.yml", "Inventory: /inventory.ini", "Manage Docker daemon", "Idempotent execution", "Zero-downtime deploy"]
        },
        {
            "num": "5. CONTAINERIZATION", "bg": "#fef2f2", "border": "#fecaca", "hdr_bg": "#fee2e2", "hdr_col": "#991b1b",
            "title": "Docker Engine", "badge": "water-monitoring-ci",
            "bullets": ["Python 3.11-slim base", "Exposes Port 5000", "Host mapped to 5002", "Mounts /app/data volume", "Container: water-monitoring-ansible"]
        },
        {
            "num": "6. APPLICATION STACK", "bg": "#f5f3ff", "border": "#ddd6fe", "hdr_bg": "#ede9fe", "hdr_col": "#5b21b6",
            "title": "Flask + SQLite", "badge": "AquaWatch Stack",
            "bullets": ["Frontend: HTML5/Aqua CSS", "Backend: Python Flask", "DB: water_monitoring.db", "Endpoints: /, /admin, /api", "Real-time Telemetry"]
        }
    ]

    col_w = (w - 80 - 5 * 16) // 6
    for idx, c in enumerate(cols):
        cx0 = 40 + idx * (col_w + 16)
        cx1 = cx0 + col_w
        cy0, cy1 = 130, 520
        draw_rounded_rect(draw, (cx0, cy0, cx1, cy1), 12, fill=c["bg"], outline=c["border"], width=2)
        # Header banner
        draw_rounded_rect(draw, (cx0, cy0, cx1, cy0 + 38), 12, fill=c["hdr_bg"])
        draw.text((cx0 + col_w // 2, cy0 + 20), c["num"], font=f_card_hdr, fill=c["hdr_col"], anchor="mm")
        
        # Title and badge
        draw.text((cx0 + col_w // 2, cy0 + 60), c["title"], font=f_card_bold, fill="#0f172a", anchor="mm")
        # badge
        draw_rounded_rect(draw, (cx0 + 15, cy0 + 78, cx1 - 15, cy0 + 104), 6, fill="#ffffff", outline=c["border"], width=1)
        draw.text((cx0 + col_w // 2, cy0 + 91), c["badge"], font=f_badge, fill=c["hdr_col"], anchor="mm")
        
        # Bullets
        by = cy0 + 125
        for b in c["bullets"]:
            draw.text((cx0 + 18, by), f"* {b}", font=f_card_body, fill="#334155")
            by += 28

        # Draw connecting arrows between columns
        if idx < 5:
            draw_arrow(draw, (cx1 + 2, (cy0 + cy1) // 2), (cx1 + 14, (cy0 + cy1) // 2), fill="#64748b", width=3, arrow_size=8)

    # Middle section: Users & Application Running & Data Persistence (y: 545 to 860)
    # Left: Users (x: 40 to 450)
    draw_rounded_rect(draw, (40, 545, 450, 860), 12, fill="#fdf2f8", outline="#fbcfe8", width=2)
    draw_rounded_rect(draw, (40, 545, 450, 583), 12, fill="#fce7f3")
    draw.text((245, 564), "7. USERS & CITIZENS", font=f_card_hdr, fill="#9d174d", anchor="mm")
    
    # Sub boxes for Citizen and Admin
    draw_rounded_rect(draw, (55, 600, 435, 715), 8, fill="#ffffff", outline="#f472b6", width=1)
    draw.text((70, 615), "Citizen / Resident Portal:", font=f_card_bold, fill="#831843")
    draw.text((70, 642), "* View real-time Water Quality (pH, TDS)", font=f_card_body, fill="#475569")
    draw.text((70, 666), "* Submit Water Complaints (Leakage, Pressure)", font=f_card_body, fill="#475569")
    draw.text((70, 690), "* Instant Track with Token ID (WC-XXXXX)", font=f_card_body, fill="#475569")

    draw_rounded_rect(draw, (55, 730, 435, 845), 8, fill="#ffffff", outline="#f472b6", width=1)
    draw.text((70, 745), "Municipal Admin / Engineer:", font=f_card_bold, fill="#831843")
    draw.text((70, 772), "* Secure Session-based Login Authentication", font=f_card_body, fill="#475569")
    draw.text((70, 796), "* Real-time Sensor Metric Gauges & Trends", font=f_card_body, fill="#475569")
    draw.text((70, 820), "* Update Complaint Status (Pending -> Resolved)", font=f_card_body, fill="#475569")

    # Arrow from Users to App
    draw_arrow(draw, (452, 700), (488, 700), fill="#be185d", width=4, arrow_size=10)

    # Middle Center: Running App (x: 490 to 1210)
    draw_rounded_rect(draw, (490, 545, 1210, 860), 12, fill="#f0fdfa", outline="#99f6e4", width=2)
    draw_rounded_rect(draw, (490, 545, 1210, 583), 12, fill="#ccfbf1")
    draw.text((850, 564), "8. SMART WATER MONITORING APPLICATION (RUNNING)", font=f_card_hdr, fill="#115e59", anchor="mm")
    
    # Inner display box simulating UI
    draw_rounded_rect(draw, (510, 600, 1190, 800), 8, fill="#0f172a", outline="#0d9488", width=2)
    # UI Title bar
    draw.text((530, 625), "AquaWatch - Smart Water Quality & Telemetry System", font=f_card_bold, fill="#38bdf8")
    draw.text((1120, 625), "Port 5002", font=f_card_code, fill="#4ade80")
    # Metric cards inside UI
    draw_rounded_rect(draw, (530, 650, 720, 730), 6, fill="#1e293b")
    draw.text((545, 665), "Water pH Level", font=f_card_body, fill="#94a3b8")
    draw.text((545, 695), "7.4 pH (Optimal)", font=f_card_bold, fill="#34d399")

    draw_rounded_rect(draw, (740, 650, 930, 730), 6, fill="#1e293b")
    draw.text((755, 665), "TDS Level", font=f_card_body, fill="#94a3b8")
    draw.text((755, 695), "245 ppm (Good)", font=f_card_bold, fill="#38bdf8")

    draw_rounded_rect(draw, (950, 650, 1170, 730), 6, fill="#1e293b")
    draw.text((965, 665), "Turbidity / Pressure", font=f_card_body, fill="#94a3b8")
    draw.text((965, 695), "1.8 NTU / 42 PSI", font=f_card_bold, fill="#fbbf24")

    # Bottom status bar of UI
    draw.text((530, 760), "Registered Complaints: 3 Active | Storage: Persistent Volume Mounted | Health: 200 OK", font=f_card_code, fill="#e2e8f0")

    # Access URL banner below UI
    draw_rounded_rect(draw, (620, 815, 1080, 848), 6, fill="#0284c7")
    draw.text((850, 831), "Live Host Endpoint: http://localhost:5002", font=f_card_bold, fill="#ffffff", anchor="mm")

    # Arrow to Data persistence
    draw_arrow(draw, (1212, 700), (1248, 700), fill="#0d9488", width=4, arrow_size=10)

    # Right: Data Persistence (x: 1250 to w - 40)
    draw_rounded_rect(draw, (1250, 545, w - 40, 860), 12, fill="#eff6ff", outline="#bfdbfe", width=2)
    draw_rounded_rect(draw, (1250, 545, w - 40, 583), 12, fill="#dbeafe")
    draw.text((1442, 564), "9. DATA PERSISTENCE", font=f_card_hdr, fill="#1e40af", anchor="mm")

    draw_rounded_rect(draw, (1270, 600, w - 60, 740), 8, fill="#ffffff", outline="#3b82f6", width=2)
    draw.text((1290, 620), "SQLite Database Storage", font=f_card_bold, fill="#1d4ed8")
    draw.text((1290, 648), "File: water_monitoring.db", font=f_card_code, fill="#0f172a")
    draw.text((1290, 672), "Path: /app/data/water_monitoring.db", font=f_card_code, fill="#64748b")
    draw.text((1290, 696), "Volume: water_monitoring_data", font=f_card_bold, fill="#0284c7")
    draw.text((1290, 720), "Mount: Docker Named Host Volume", font=f_card_body, fill="#334155")

    draw_rounded_rect(draw, (1270, 755, w - 60, 845), 8, fill="#eff6ff", outline="#93c5fd", width=1)
    draw.text((1285, 775), "Persistence Guarantee:", font=f_card_bold, fill="#1e3a8a")
    draw.text((1285, 802), "Water sensor logs and complaint records", font=f_card_body, fill="#1e40af")
    draw.text((1285, 824), "survive container restart or recreation.", font=f_card_body, fill="#1e40af")

    # Bottom 3 Infographic boxes (y: 880 to 1070)
    # 1. Tech Stack (x: 40 to 650)
    draw_rounded_rect(draw, (40, 880, 650, 1070), 10, fill="#f8fafc", outline="#cbd5e1", width=1)
    draw.text((345, 905), "TECHNOLOGY STACK SUMMARY", font=f_card_bold, fill="#0f172a", anchor="mm")
    badges = [
        ("Python 3.11", "#1e3a8a", "#dbeafe"),
        ("Flask Framework", "#065f46", "#d1fae5"),
        ("SQLite 3", "#1e40af", "#e0e7ff"),
        ("Docker & Volumes", "#0369a1", "#e0f2fe"),
        ("Jenkins CI/CD", "#991b1b", "#fee2e2"),
        ("Ansible Lab", "#374151", "#f3f4f6"),
        ("Pytest Suite", "#15803d", "#dcfce7"),
        ("Bootstrap 5", "#5b21b6", "#ede9fe")
    ]
    bx, by = 60, 930
    for idx, (b_name, b_col, b_bg) in enumerate(badges):
        draw_rounded_rect(draw, (bx, by, bx + 130, by + 30), 6, fill=b_bg, outline=b_col, width=1)
        draw.text((bx + 65, by + 15), b_name, font=f_badge, fill=b_col, anchor="mm")
        bx += 145
        if (idx + 1) % 4 == 0:
            bx = 60
            by += 42

    # 2. Key Ports (x: 670 to 1150)
    draw_rounded_rect(draw, (670, 880, 1150, 1070), 10, fill="#f0fdf4", outline="#bbf7d0", width=1)
    draw.text((910, 905), "SYSTEM PORTS & NETWORK TOPOLOGY", font=f_card_bold, fill="#166534", anchor="mm")
    ports = [
        "Jenkins CI Server       ->  http://localhost:8080",
        "Water Monitoring Host   ->  http://localhost:5002",
        "Container Application   ->  0.0.0.0:5000 (Internal)",
        "Port Mapping Contract   ->  5002:5000",
        "Ansible Control Node    ->  ansible-docker-lab (Lab Net)"
    ]
    py = 930
    for p in ports:
        draw.text((690, py), p, font=f_card_code, fill="#14532d")
        py += 26

    # 3. Benefits (x: 1170 to w - 40)
    draw_rounded_rect(draw, (1170, 880, w - 40, 1070), 10, fill="#fefce8", outline="#fef08a", width=1)
    draw.text((1400, 905), "DEVOPS & OPERATIONAL BENEFITS", font=f_card_bold, fill="#854d0e", anchor="mm")
    bens = [
        "[+] Automated Continuous Integration with 13 Unit Tests",
        "[+] Fully Idempotent Ansible Deployment Automation",
        "[+] Zero Data Loss with Dedicated Docker Volume",
        "[+] Immediate Citizen Complaint Escalation & Resolution",
        "[+] Lightweight, Secure & Containerized Deployment"
    ]
    by = 930
    for b in bens:
        draw.text((1185, by), b, font=f_card_body, fill="#713f12")
        by += 26

    # Downscale for super antialiasing to original size (837, 552)
    final_img = img.resize((837, 552), Image.Resampling.LANCZOS)
    final_img.convert("RGB").save(os.path.join(NEW_MEDIA_DIR, "image2.png"), quality=95)
    print("Saved image2.png")

# ==========================================
# DIAGRAM 2: image8.png (1536 x 853) -> Docker Flow
# ==========================================
def generate_image8():
    w, h = 1536, 853
    img = Image.new("RGB", (w, h), "#ffffff")
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype("segoeuib.ttf", 36)
    f_sub = ImageFont.truetype("segoeui.ttf", 20)
    f_step_num = ImageFont.truetype("segoeuib.ttf", 26)
    f_step_title = ImageFont.truetype("segoeuib.ttf", 22)
    f_body = ImageFont.truetype("segoeui.ttf", 18)
    f_code = ImageFont.truetype("consola.ttf", 17)

    # Top Banner
    draw_rounded_rect(draw, (40, 20, w - 40, 100), 16, fill="#0f2b48")
    draw.text((w // 2, 45), "Docker Flow - Smart Water Monitoring System", font=f_title, fill="#ffffff", anchor="mm")
    draw.text((w // 2, 80), "Container Build, Volume Mapping, Image Packaging & Container Run Workflow", font=f_sub, fill="#38bdf8", anchor="mm")

    steps = [
        {
            "step": "Application Code", "bg": "#fef2f2", "border": "#fecaca", "badge_col": "#991b1b",
            "box_left": ["Directory: WaterMonitoring/", "app.py (Flask routes & SQLite handlers)", "templates/ (AquaWatch UI views)", "static/ (CSS styles, JS gauges)", "requirements.txt (Flask, pytest)", "test_app.py (13 unit test cases)"],
            "box_right": ["* Houses clean, modular Python codebase.", "* Decoupled static assets and HTML templates.", "* Ready for containerized packaging and CI/CD validation."]
        },
        {
            "step": "Dockerfile", "bg": "#eff6ff", "border": "#bfdbfe", "badge_col": "#1e40af",
            "box_left": ["FROM python:3.11-slim", "WORKDIR /app", "COPY . .", "RUN pip install -r requirements.txt", "CMD [\"python\", \"app.py\"]"],
            "box_right": ["* Defines reproducible build steps using slim Python image.", "* Installs application and test dependencies.", "* Configures container startup command listening on 0.0.0.0:5000."]
        },
        {
            "step": "Docker Image", "bg": "#fefce8", "border": "#fef08a", "badge_col": "#854d0e",
            "box_left": ["Image Name: water-monitoring-ci", "Tag: latest", "Base: Debian GNU/Linux (Bookworm)", "Includes Pytest and Flask dependencies", "Built via: docker build -t water-monitoring-ci ."],
            "box_right": ["* Self-contained image artifact generated in Jenkins pipeline.", "* Pytest executes inside image to validate routes before deployment.", "* Ready for immediate, identical execution across all environments."]
        },
        {
            "step": "Docker Container", "bg": "#f0fdf4", "border": "#bbf7d0", "badge_col": "#166534",
            "box_left": ["Container Name: water-monitoring-ansible", "Port Mapping: 5002:5000", "Volume Mount: water_monitoring_data:/app/data", "Managed by: Ansible Playbook (/water-deploy.yml)", "Status: Up, Healthy"],
            "box_right": ["* Active runtime instance launched via Ansible community.docker module.", "* Binds internal port 5000 to accessible host port 5002.", "* Attaches persistent named volume water_monitoring_data."]
        },
        {
            "step": "Flask Application", "bg": "#faf5ff", "border": "#e9d5ff", "badge_col": "#6b21a8",
            "box_left": ["Endpoint: http://localhost:5002", "Public Portal: Live water metrics, Citizen complaint filing", "Admin Dashboard: /admin/login (Credentials: admin/admin123)", "Telemetry Engine: Simulated water quality gauges", "Database Engine: SQLite at /app/data/water_monitoring.db"],
            "box_right": ["* Fully functional and responsive web interface accessible to citizens.", "* Municipal officers manage and update complaint statuses in real-time.", "* All sensor telemetry and citizen feedback permanently preserved."]
        }
    ]

    sy = 120
    step_h = 125
    for idx, s in enumerate(steps):
        draw_rounded_rect(draw, (40, sy, w - 40, sy + step_h), 12, fill=s["bg"], outline=s["border"], width=2)
        
        # Step Title column (x: 60 to 300)
        draw_rounded_rect(draw, (60, sy + 15, 300, sy + step_h - 15), 8, fill="#ffffff", outline=s["border"], width=1)
        draw.text((180, sy + 45), f"Step {idx + 1}", font=f_step_num, fill=s["badge_col"], anchor="mm")
        draw.text((180, sy + 80), s["step"], font=f_step_title, fill="#0f172a", anchor="mm")

        # Code / Configuration Box (x: 320 to 860)
        draw_rounded_rect(draw, (320, sy + 12, 860, sy + step_h - 12), 8, fill="#ffffff", outline="#cbd5e1", width=1)
        cy = sy + 20
        for cl in s["box_left"][:5]:
            draw.text((335, cy), cl, font=f_code, fill="#0f172a")
            cy += 20

        # Description Column (x: 880 to w - 60)
        dy = sy + 22
        for bl in s["box_right"]:
            draw.text((890, dy), bl, font=f_body, fill="#334155")
            dy += 28

        # Draw connecting arrow to next step
        if idx < 4:
            draw_arrow(draw, (w // 2, sy + step_h), (w // 2, sy + step_h + 18), fill="#475569", width=3, arrow_size=8)
        
        sy += step_h + 20

    img.save(os.path.join(NEW_MEDIA_DIR, "image8.png"), quality=95)
    print("Saved image8.png")

# ==========================================
# DIAGRAM 3: image16.png (1450 x 596) -> Storage Flow
# ==========================================
def generate_image16():
    w, h = 1450, 596
    img = Image.new("RGB", (w, h), "#ffffff")
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype("segoeuib.ttf", 32)
    f_sub = ImageFont.truetype("segoeui.ttf", 18)
    f_step_title = ImageFont.truetype("segoeuib.ttf", 22)
    f_body = ImageFont.truetype("segoeui.ttf", 17)
    f_code = ImageFont.truetype("consola.ttf", 16)

    # Top Banner
    draw_rounded_rect(draw, (40, 15, w - 40, 85), 14, fill="#0f2b48")
    draw.text((w // 2, 38), "Storage Flow - Smart Water Monitoring System", font=f_title, fill="#ffffff", anchor="mm")
    draw.text((w // 2, 68), "Persistent Data Architecture: Flask -> SQLite -> Volume -> Host Storage", font=f_sub, fill="#38bdf8", anchor="mm")

    steps = [
        ("Flask App", "Flask routes (/complaint, /admin) handle user submissions and telemetry updates.", "#fef2f2", "#fecaca", "#991b1b"),
        ("SQLite Engine", "Flask executes parameterized SQL operations against SQLite database engine.", "#eff6ff", "#bfdbfe", "#1e40af"),
        ("water_monitoring.db", "Stores 'water_readings' (pH, TDS, turbidity) and 'complaints' (WC-XXXXX tickets).", "#fefce8", "#fef08a", "#854d0e"),
        ("/app/data", "Container internal path housing the database file at /app/data/water_monitoring.db.", "#f0fdf4", "#bbf7d0", "#166534"),
        ("water_monitoring_data", "Dedicated Docker named volume mounted to /app/data inside water-monitoring-ansible.", "#faf5ff", "#e9d5ff", "#6b21a8"),
        ("Persistent Storage", "Data survives container deletion, Ansible redeployment, and host daemon restarts.", "#ecfdf5", "#a7f3d0", "#065f46")
    ]

    sy = 105
    step_h = 65
    for idx, (title, desc, bg, border, badge_col) in enumerate(steps):
        draw_rounded_rect(draw, (60, sy, w - 60, sy + step_h), 10, fill=bg, outline=border, width=2)
        
        # Step box on left
        draw_rounded_rect(draw, (80, sy + 10, 380, sy + step_h - 10), 6, fill="#ffffff", outline=border, width=1)
        draw.text((230, sy + step_h // 2), title, font=f_step_title, fill=badge_col, anchor="mm")

        # Description on right
        draw.text((410, sy + step_h // 2), desc, font=f_body, fill="#1e293b", anchor="lm")

        # Arrow down
        if idx < 5:
            draw_arrow(draw, (230, sy + step_h), (230, sy + step_h + 14), fill="#64748b", width=2, arrow_size=6)

        sy += step_h + 15

    img.save(os.path.join(NEW_MEDIA_DIR, "image16.png"), quality=95)
    print("Saved image16.png")

# ==========================================
# DIAGRAM 4: image18.png (1145 x 763) -> Complaint Lifecycle Flow
# ==========================================
def generate_image18():
    w, h = 1145, 763
    img = Image.new("RGB", (w, h), "#ffffff")
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype("segoeuib.ttf", 30)
    f_sub = ImageFont.truetype("segoeui.ttf", 17)
    f_step_title = ImageFont.truetype("segoeuib.ttf", 20)
    f_card_bold = ImageFont.truetype("segoeuib.ttf", 16)
    f_body = ImageFont.truetype("segoeui.ttf", 15)
    f_code = ImageFont.truetype("consola.ttf", 14)

    # Top Banner
    draw_rounded_rect(draw, (30, 15, w - 30, 85), 14, fill="#0f2b48")
    draw.text((w // 2, 38), "Complaint Lifecycle Flow - AquaWatch Water System", font=f_title, fill="#ffffff", anchor="mm")
    draw.text((w // 2, 68), "Citizen Complaint Registration, Processing, Persistence & Municipal Resolution", font=f_sub, fill="#38bdf8", anchor="mm")

    # Flow in two rows of 3 boxes
    # Row 1: y: 110 to 390
    row1 = [
        {
            "num": "Step 1", "title": "Citizen / Resident", "bg": "#fef2f2", "border": "#fecaca", "hdr_col": "#991b1b",
            "lines": ["* Citizen notices water quality issue", "* (Low pressure, high TDS, leakage)", "* Opens AquaWatch portal", "* Accessible at http://localhost:5002", "* Clicks 'Report Issue'"]
        },
        {
            "num": "Step 2", "title": "Fill Complaint Form", "bg": "#eff6ff", "border": "#bfdbfe", "hdr_col": "#1e40af",
            "lines": ["* Enters Citizen Name & Contact", "* Selects Location / Ward Number", "* Chooses Issue Category:", "  - Water Quality / Contamination", "  - Pipeline Leakage / Low Pressure", "* Enters Detailed Description"]
        },
        {
            "num": "Step 3", "title": "Ticket Generation", "bg": "#fefce8", "border": "#fef08a", "hdr_col": "#854d0e",
            "lines": ["* Flask validates input fields", "* Generates Unique Tracking ID", "  (e.g., WC-00001, WC-00002)", "* Initial Status: 'Pending'", "* Flash success notification displayed", "* Citizen gets tracking token"]
        }
    ]

    box_w = 330
    box_gap = (w - 60 - 3 * box_w) // 2
    for idx, c in enumerate(row1):
        bx0 = 30 + idx * (box_w + box_gap)
        bx1 = bx0 + box_w
        by0, by1 = 110, 390
        draw_rounded_rect(draw, (bx0, by0, bx1, by1), 12, fill=c["bg"], outline=c["border"], width=2)
        # Header banner
        draw_rounded_rect(draw, (bx0, by0, bx1, by0 + 40), 12, fill="#ffffff")
        draw.text((bx0 + box_w // 2, by0 + 15), c["num"], font=f_card_bold, fill=c["hdr_col"], anchor="mm")
        draw.text((bx0 + box_w // 2, by0 + 30), c["title"], font=f_step_title, fill="#0f172a", anchor="mm")

        # Lines
        ly = by0 + 60
        for l in c["lines"]:
            draw.text((bx0 + 20, ly), l, font=f_body, fill="#334155")
            ly += 26

        if idx < 2:
            draw_arrow(draw, (bx1 + 2, (by0 + by1) // 2), (bx1 + box_gap - 2, (by0 + by1) // 2), fill="#64748b", width=3, arrow_size=8)

    # Arrow from Row 1 Step 3 down to Row 2 Step 4
    draw_arrow(draw, (30 + 2 * (box_w + box_gap) + box_w // 2, 392), (30 + 2 * (box_w + box_gap) + box_w // 2, 428), fill="#64748b", width=3, arrow_size=8)

    # Row 2: y: 430 to 710 (Right to Left or Left to Right)
    # Let's do Left to Right: Step 4 (Backend Processing) -> Step 5 (Persistent Storage) -> Step 6 (Admin Dashboard Resolution)
    # Arrow curving down
    draw_arrow(draw, (30 + 2 * (box_w + box_gap) + box_w // 2, 392), (w - 30 - box_w // 2, 428), fill="#64748b", width=3, arrow_size=8)

    row2 = [
        {
            "num": "Step 4", "title": "Backend Processing", "bg": "#f0fdf4", "border": "#bbf7d0", "hdr_col": "#166534",
            "lines": ["* Flask POST route /complaint", "* Parameterized SQL queries", "* Prevents SQL injection", "* Automatic timestamp generation", "* Status committed in transaction", "* Instant audit log entry"]
        },
        {
            "num": "Step 5", "title": "Persistent Database", "bg": "#faf5ff", "border": "#e9d5ff", "hdr_col": "#6b21a8",
            "lines": ["* SQLite table 'complaints'", "* Stored in /app/data/water_monitoring.db", "* Mounted via Docker Volume", "* water_monitoring_data", "* 100% resilient across container", "* redeployments and restarts"]
        },
        {
            "num": "Step 6", "title": "Admin Resolution", "bg": "#ecfdf5", "border": "#a7f3d0", "hdr_col": "#065f46",
            "lines": ["* Municipal Officer logs in", "* Dashboard URL: /admin/login", "* Views all tickets & sensor metrics", "* Evaluates complaint validity", "* Updates status: 'In Progress' / 'Resolved'", "* Citizen sees live updated status"]
        }
    ]

    for idx, c in enumerate(row2):
        bx0 = 30 + idx * (box_w + box_gap)
        bx1 = bx0 + box_w
        by0, by1 = 430, 710
        draw_rounded_rect(draw, (bx0, by0, bx1, by1), 12, fill=c["bg"], outline=c["border"], width=2)
        # Header banner
        draw_rounded_rect(draw, (bx0, by0, bx1, by0 + 40), 12, fill="#ffffff")
        draw.text((bx0 + box_w // 2, by0 + 15), c["num"], font=f_card_bold, fill=c["hdr_col"], anchor="mm")
        draw.text((bx0 + box_w // 2, by0 + 30), c["title"], font=f_step_title, fill="#0f172a", anchor="mm")

        # Lines
        ly = by0 + 60
        for l in c["lines"]:
            draw.text((bx0 + 20, ly), l, font=f_body, fill="#334155")
            ly += 26

        if idx < 2:
            draw_arrow(draw, (bx1 + 2, (by0 + by1) // 2), (bx1 + box_gap - 2, (by0 + by1) // 2), fill="#64748b", width=3, arrow_size=8)

    # Status summary footer
    draw_rounded_rect(draw, (30, 725, w - 30, 755), 6, fill="#0f2b48")
    draw.text((w // 2, 740), "Complaint Status Pipeline: [PENDING] -> [INVESTIGATION IN PROGRESS] -> [FIELD RESOLUTION VERIFIED]", font=f_card_bold, fill="#38bdf8", anchor="mm")

    img.save(os.path.join(NEW_MEDIA_DIR, "image18.png"), quality=95)
    print("Saved image18.png")

if __name__ == "__main__":
    generate_image2()
    generate_image8()
    generate_image16()
    generate_image18()
    print("All diagrams generated successfully!")
