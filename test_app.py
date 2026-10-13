"""
test_app.py — Automated tests for Smart Water Monitoring and Complaint Management System
Run with: python -m pytest test_app.py
"""

import os
import sys
import tempfile
import pytest

# ── Point imports at the project root ──────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))


@pytest.fixture
def app_with_temp_db():
    """
    Create a fresh Flask test client backed by a temporary SQLite database.
    The temporary database is deleted after each test session.
    """
    # Create a temp file for the isolated test database
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)

    # Patch the DATABASE path BEFORE importing app so init_db uses the temp DB
    os.environ["DATABASE_PATH"] = db_path
    os.environ["ADMIN_USERNAME"] = "admin"
    os.environ["ADMIN_PASSWORD"] = "admin123"
    os.environ["FLASK_SECRET_KEY"] = "test-secret-key"

    # Import app after env vars are set
    import importlib
    import app as app_module
    importlib.reload(app_module)           # reload so DATABASE is re-evaluated

    app_module.app.config["TESTING"] = True
    app_module.app.config["WTF_CSRF_ENABLED"] = False
    app_module.init_db()

    with app_module.app.test_client() as client:
        yield client, app_module

    # Cleanup temp database
    try:
        os.unlink(db_path)
    except OSError:
        pass


# ── 1. Flask application initializes successfully ──────────────────────────────
def test_app_initializes(app_with_temp_db):
    client, app_module = app_with_temp_db
    assert app_module.app is not None


# ── 2. Home page returns HTTP 200 ─────────────────────────────────────────────
def test_home_page(app_with_temp_db):
    client, _ = app_with_temp_db
    response = client.get("/")
    assert response.status_code == 200
    assert b"Water" in response.data


# ── 3. Monitoring page returns HTTP 200 ───────────────────────────────────────
def test_monitoring_page(app_with_temp_db):
    client, _ = app_with_temp_db
    response = client.get("/monitoring")
    assert response.status_code == 200
    assert b"Monitoring" in response.data or b"monitoring" in response.data


# ── 4. Complaint reporting page returns HTTP 200 ──────────────────────────────
def test_report_page(app_with_temp_db):
    client, _ = app_with_temp_db
    response = client.get("/report")
    assert response.status_code == 200
    assert b"Complaint" in response.data or b"complaint" in response.data


# ── 5. A valid complaint can be submitted ─────────────────────────────────────
def test_submit_valid_complaint(app_with_temp_db):
    client, _ = app_with_temp_db
    response = client.post(
        "/submit_complaint",
        data={
            "complaint_type": "Water Leakage",
            "location": "Block A, Main Street",
            "description": "There is a severe water leakage near the main pipeline.",
            "priority": "High",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    # Should redirect to track page showing the complaint ID
    assert b"WC-" in response.data


# ── 6. Submitted complaint is stored in SQLite ────────────────────────────────
def test_complaint_stored_in_db(app_with_temp_db):
    client, app_module = app_with_temp_db
    client.post(
        "/submit_complaint",
        data={
            "complaint_type": "No Water Supply",
            "location": "Sector 5, Tower B",
            "description": "No water supply for the past 12 hours in the entire block.",
            "priority": "Critical",
        },
        follow_redirects=True,
    )
    conn = app_module.get_db()
    row = conn.execute(
        "SELECT * FROM water_complaints WHERE complaint_type = 'No Water Supply'"
    ).fetchone()
    conn.close()
    assert row is not None
    assert row["location"] == "Sector 5, Tower B"
    assert row["priority"] == "Critical"
    assert row["status"] == "Pending"


# ── 7. A complaint can be retrieved using its ID ──────────────────────────────
def test_retrieve_complaint_by_id(app_with_temp_db):
    client, app_module = app_with_temp_db
    # Insert a complaint directly
    conn = app_module.get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO water_complaints (complaint_type, location, description, priority, status) VALUES (?,?,?,?,?)",
        ("Pipeline Damage", "Zone 3 Pump Station", "Damaged pipe causing water loss.", "Medium", "Pending"),
    )
    complaint_id = cur.lastrowid
    conn.commit()
    conn.close()

    response = client.post(
        "/track",
        data={"complaint_id": f"WC-{complaint_id:05d}"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Pipeline Damage" in response.data


# ── 8. Tracking page displays complaint status ────────────────────────────────
def test_track_complaint_status(app_with_temp_db):
    client, app_module = app_with_temp_db
    conn = app_module.get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO water_complaints (complaint_type, location, description, priority, status) VALUES (?,?,?,?,?)",
        ("Low Water Pressure", "Apartment 12B", "Pressure is very low in the morning.", "Low", "In Progress"),
    )
    complaint_id = cur.lastrowid
    conn.commit()
    conn.close()

    response = client.post(
        "/track",
        data={"complaint_id": str(complaint_id)},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"In Progress" in response.data


# ── 9. Admin login works with valid credentials ───────────────────────────────
def test_admin_login_valid(app_with_temp_db):
    client, _ = app_with_temp_db
    response = client.post(
        "/admin/login",
        data={"username": "admin", "password": "admin123"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    # Should land on admin dashboard
    assert b"Dashboard" in response.data or b"dashboard" in response.data or b"Admin" in response.data


# ── 10. Unauthorized access to admin dashboard is rejected ────────────────────
def test_admin_dashboard_unauthorized(app_with_temp_db):
    client, _ = app_with_temp_db
    response = client.get("/admin", follow_redirects=False)
    # Must redirect to login page (302)
    assert response.status_code == 302
    assert "/admin/login" in response.headers.get("Location", "")


# ── 11. Admin dashboard returns HTTP 200 after authentication ─────────────────
def test_admin_dashboard_authorized(app_with_temp_db):
    client, _ = app_with_temp_db
    # Login first
    client.post(
        "/admin/login",
        data={"username": "admin", "password": "admin123"},
        follow_redirects=True,
    )
    response = client.get("/admin")
    assert response.status_code == 200
    assert b"Admin" in response.data


# ── 12. Authorized admin can update a complaint status ────────────────────────
def test_admin_update_status(app_with_temp_db):
    client, app_module = app_with_temp_db

    # Insert complaint
    conn = app_module.get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO water_complaints (complaint_type, location, description, priority, status) VALUES (?,?,?,?,?)",
        ("Water Quality Issue", "Main Campus Block C", "Water appears discolored and smells odd.", "High", "Pending"),
    )
    complaint_id = cur.lastrowid
    conn.commit()
    conn.close()

    # Login as admin
    client.post(
        "/admin/login",
        data={"username": "admin", "password": "admin123"},
        follow_redirects=True,
    )

    # Update status
    response = client.post(
        "/update_status",
        data={"complaint_id": str(complaint_id), "new_status": "Assigned"},
        follow_redirects=True,
    )
    assert response.status_code == 200


# ── 13. Status update is actually saved in SQLite ─────────────────────────────
def test_status_update_persisted(app_with_temp_db):
    client, app_module = app_with_temp_db

    # Insert complaint
    conn = app_module.get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO water_complaints (complaint_type, location, description, priority, status) VALUES (?,?,?,?,?)",
        ("Contaminated Water", "Ward 7 North", "Foul smell and color in tap water.", "Critical", "Pending"),
    )
    complaint_id = cur.lastrowid
    conn.commit()
    conn.close()

    # Login
    client.post(
        "/admin/login",
        data={"username": "admin", "password": "admin123"},
        follow_redirects=True,
    )

    # Update to Resolved
    client.post(
        "/update_status",
        data={"complaint_id": str(complaint_id), "new_status": "Resolved"},
        follow_redirects=True,
    )

    # Verify in DB
    conn = app_module.get_db()
    row = conn.execute(
        "SELECT status FROM water_complaints WHERE id = ?", (complaint_id,)
    ).fetchone()
    conn.close()
    assert row["status"] == "Resolved"
