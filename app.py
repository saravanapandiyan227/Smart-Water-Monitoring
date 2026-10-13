"""
Smart Water Monitoring and Complaint Management System
Flask Backend Application
"""

import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

app = Flask(__name__)

# --- Configuration ---
# Secret key: use environment variable in production, fallback for development only
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")

# Admin password: use environment variable in production
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")

# Database path: stored in /app/data inside Docker, data/ locally
DATABASE = os.environ.get("DATABASE_PATH", os.path.join(os.path.dirname(__file__), "data", "water_monitoring.db"))

# Water quality thresholds (illustrative values for demonstration only)
# These are NOT official water safety certification criteria.
THRESHOLDS = {
    "ph_min": 6.5,
    "ph_max": 8.5,
    "turbidity_warning": 4.0,   # NTU
    "turbidity_critical": 10.0, # NTU
    "water_level_warning": 40,  # %
    "water_level_critical": 20, # %
    "temp_max_warning": 30.0,   # °C
    "temp_max_critical": 35.0,  # °C
}

# Complaint categories and priorities
COMPLAINT_CATEGORIES = [
    "Water Leakage",
    "Low Water Pressure",
    "No Water Supply",
    "Water Quality Issue",
    "Pipeline Damage",
    "Overflowing Water Tank",
    "Contaminated Water",
    "Other",
]
PRIORITIES = ["Low", "Medium", "High", "Critical"]
STATUSES = ["Pending", "Assigned", "In Progress", "Resolved", "Closed"]


# ─────────────────────────────────────────────
#  DATABASE HELPERS
# ─────────────────────────────────────────────

def get_db():
    """Open a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables and seed sample water readings if the table is empty."""
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

    conn = get_db()
    cur = conn.cursor()

    # --- Table: water_complaints ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS water_complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_type TEXT NOT NULL,
            location TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
            updated_at DATETIME NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
    """)

    # --- Table: water_readings ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS water_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            water_level REAL NOT NULL,
            ph_level REAL NOT NULL,
            turbidity REAL NOT NULL,
            temperature REAL NOT NULL,
            water_status TEXT NOT NULL,
            recorded_at DATETIME NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
    """)

    # Seed sample readings only when table is empty
    cur.execute("SELECT COUNT(*) FROM water_readings")
    count = cur.fetchone()[0]
    if count == 0:
        sample_readings = [
            (82.5, 7.2, 1.8, 24.3, "Normal",   "2026-10-13 08:00:00"),
            (79.0, 7.4, 2.1, 25.1, "Normal",   "2026-10-13 09:00:00"),
            (75.5, 7.1, 3.5, 26.0, "Normal",   "2026-10-13 10:00:00"),
            (70.0, 6.8, 5.2, 27.4, "Warning",  "2026-10-13 10:30:00"),
            (68.3, 7.3, 2.9, 25.8, "Normal",   "2026-10-13 11:00:00"),
        ]
        cur.executemany(
            "INSERT INTO water_readings (water_level, ph_level, turbidity, temperature, water_status, recorded_at) VALUES (?,?,?,?,?,?)",
            sample_readings,
        )

    conn.commit()
    conn.close()


def compute_water_status(water_level, ph_level, turbidity, temperature):
    """
    Determine water quality status from readings using illustrative thresholds.
    This is for demonstration purposes only — not official water safety criteria.
    Returns: 'Normal', 'Warning', or 'Critical'
    """
    if (
        turbidity >= THRESHOLDS["turbidity_critical"]
        or water_level <= THRESHOLDS["water_level_critical"]
        or temperature >= THRESHOLDS["temp_max_critical"]
        or ph_level < 6.0
        or ph_level > 9.0
    ):
        return "Critical"
    if (
        turbidity >= THRESHOLDS["turbidity_warning"]
        or water_level <= THRESHOLDS["water_level_warning"]
        or temperature >= THRESHOLDS["temp_max_warning"]
        or ph_level < THRESHOLDS["ph_min"]
        or ph_level > THRESHOLDS["ph_max"]
    ):
        return "Warning"
    return "Normal"


def get_latest_reading():
    """Fetch the most recent water reading from the database."""
    conn = get_db()
    reading = conn.execute(
        "SELECT * FROM water_readings ORDER BY id DESC LIMIT 1"
    ).fetchone()
    conn.close()
    return reading


def get_complaint_stats():
    """Return a dict of complaint statistics."""
    conn = get_db()
    stats = {}
    stats["total"] = conn.execute("SELECT COUNT(*) FROM water_complaints").fetchone()[0]
    for status in ["Pending", "In Progress", "Resolved"]:
        stats[status.lower().replace(" ", "_")] = conn.execute(
            "SELECT COUNT(*) FROM water_complaints WHERE status = ?", (status,)
        ).fetchone()[0]
    stats["assigned"] = conn.execute(
        "SELECT COUNT(*) FROM water_complaints WHERE status = 'Assigned'"
    ).fetchone()[0]
    stats["closed"] = conn.execute(
        "SELECT COUNT(*) FROM water_complaints WHERE status = 'Closed'"
    ).fetchone()[0]
    conn.close()
    return stats


# ─────────────────────────────────────────────
#  ROUTES — PUBLIC
# ─────────────────────────────────────────────

@app.route("/")
def index():
    """Home page with a water monitoring summary."""
    reading = get_latest_reading()
    stats = get_complaint_stats()
    return render_template("index.html", reading=reading, stats=stats)


@app.route("/monitoring")
def monitoring():
    """Full water monitoring dashboard with all recent readings."""
    conn = get_db()
    readings = conn.execute(
        "SELECT * FROM water_readings ORDER BY id DESC LIMIT 20"
    ).fetchall()
    conn.close()
    latest = readings[0] if readings else None
    return render_template("monitoring.html", readings=readings, latest=latest, thresholds=THRESHOLDS)


@app.route("/report", methods=["GET"])
def report():
    """Complaint reporting form."""
    return render_template(
        "report.html",
        categories=COMPLAINT_CATEGORIES,
        priorities=PRIORITIES,
    )


@app.route("/submit_complaint", methods=["POST"])
def submit_complaint():
    """Validate and save a new water complaint."""
    complaint_type = request.form.get("complaint_type", "").strip()
    location = request.form.get("location", "").strip()
    description = request.form.get("description", "").strip()
    priority = request.form.get("priority", "").strip()

    errors = []
    if not complaint_type or complaint_type not in COMPLAINT_CATEGORIES:
        errors.append("Please select a valid complaint category.")
    if not location or len(location) < 5:
        errors.append("Please enter a valid location (at least 5 characters).")
    if not description or len(description) < 10:
        errors.append("Please enter a description (at least 10 characters).")
    if not priority or priority not in PRIORITIES:
        errors.append("Please select a valid priority.")

    if errors:
        return render_template(
            "report.html",
            categories=COMPLAINT_CATEGORIES,
            priorities=PRIORITIES,
            errors=errors,
            form_data=request.form,
        )

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO water_complaints (complaint_type, location, description, priority, status)
           VALUES (?, ?, ?, ?, 'Pending')""",
        (complaint_type, location, description, priority),
    )
    complaint_id = cur.lastrowid
    conn.commit()
    conn.close()

    flash(f"Complaint submitted successfully! Your Complaint ID is: WC-{complaint_id:05d}", "success")
    return redirect(url_for("track", complaint_id=f"WC-{complaint_id:05d}"))


@app.route("/track", methods=["GET", "POST"])
def track():
    """Track a complaint by its ID."""
    complaint = None
    error = None
    searched_id = None

    # Support pre-fill from redirect after submission
    prefill_id = request.args.get("complaint_id", "")

    if request.method == "POST":
        raw_id = request.form.get("complaint_id", "").strip()
        searched_id = raw_id
        numeric_id = None

        if raw_id.upper().startswith("WC-"):
            try:
                numeric_id = int(raw_id[3:])
            except ValueError:
                error = "Invalid Complaint ID format. Use WC-XXXXX."
        else:
            try:
                numeric_id = int(raw_id)
            except ValueError:
                error = "Invalid Complaint ID. Please enter a valid ID like WC-00001."

        if numeric_id is not None:
            conn = get_db()
            complaint = conn.execute(
                "SELECT * FROM water_complaints WHERE id = ?", (numeric_id,)
            ).fetchone()
            conn.close()
            if not complaint:
                error = f"No complaint found with ID '{raw_id}'. Please check your ID and try again."

    return render_template(
        "track.html",
        complaint=complaint,
        error=error,
        searched_id=searched_id,
        prefill_id=prefill_id,
    )


# ─────────────────────────────────────────────
#  ROUTES — ADMIN
# ─────────────────────────────────────────────

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Admin login page."""
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            session["admin_username"] = username
            flash("Welcome back, Admin!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            error = "Invalid username or password. Please try again."

    return render_template("admin_login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    """Admin logout."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("admin_login"))


@app.route("/admin")
def admin_dashboard():
    """Protected admin dashboard."""
    if not session.get("admin_logged_in"):
        flash("Please log in to access the admin dashboard.", "warning")
        return redirect(url_for("admin_login"))

    conn = get_db()
    complaints = conn.execute(
        "SELECT * FROM water_complaints ORDER BY created_at DESC"
    ).fetchall()
    readings = conn.execute(
        "SELECT * FROM water_readings ORDER BY id DESC LIMIT 5"
    ).fetchall()
    conn.close()

    stats = get_complaint_stats()
    latest_reading = get_latest_reading()

    return render_template(
        "admin.html",
        complaints=complaints,
        readings=readings,
        stats=stats,
        latest_reading=latest_reading,
        statuses=STATUSES,
    )


@app.route("/update_status", methods=["POST"])
def update_status():
    """Protected endpoint for admin to update a complaint's status."""
    if not session.get("admin_logged_in"):
        flash("Unauthorized. Please log in.", "danger")
        return redirect(url_for("admin_login"))

    complaint_id = request.form.get("complaint_id", "").strip()
    new_status = request.form.get("new_status", "").strip()

    if not complaint_id or not new_status:
        flash("Missing complaint ID or status.", "danger")
        return redirect(url_for("admin_dashboard"))

    if new_status not in STATUSES:
        flash("Invalid status value.", "danger")
        return redirect(url_for("admin_dashboard"))

    try:
        complaint_id_int = int(complaint_id)
    except ValueError:
        flash("Invalid complaint ID.", "danger")
        return redirect(url_for("admin_dashboard"))

    conn = get_db()
    existing = conn.execute(
        "SELECT id FROM water_complaints WHERE id = ?", (complaint_id_int,)
    ).fetchone()

    if not existing:
        conn.close()
        flash(f"Complaint ID {complaint_id} not found.", "danger")
        return redirect(url_for("admin_dashboard"))

    conn.execute(
        "UPDATE water_complaints SET status = ?, updated_at = datetime('now', 'localtime') WHERE id = ?",
        (new_status, complaint_id_int),
    )
    conn.commit()
    conn.close()

    flash(f"Complaint WC-{complaint_id_int:05d} status updated to '{new_status}'.", "success")
    return redirect(url_for("admin_dashboard"))


# ─────────────────────────────────────────────
#  API — optional lightweight JSON endpoint
# ─────────────────────────────────────────────

@app.route("/api/latest_reading")
def api_latest_reading():
    """Return latest water reading as JSON (for JS refresh)."""
    reading = get_latest_reading()
    if reading:
        return jsonify(dict(reading))
    return jsonify({"error": "No readings available"}), 404


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
