
import os
import sqlite3
from datetime import date, datetime
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)

# Use a persistent data directory in Docker.
# When running locally, use the instance directory.
DATABASE_PATH = Path(
    os.environ.get("DATABASE_PATH", "instance/appointments.db")
)

DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_db_connection():
    """Create a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the appointments table if it does not exist."""
    with get_db_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                reason TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


@app.route("/", methods=["GET", "POST"])
def home():
    """Display the booking form and process new appointments."""

    if request.method == "POST":
        patient_name = request.form.get("patient_name", "").strip()
        appointment_date = request.form.get("appointment_date", "").strip()
        appointment_time = request.form.get("appointment_time", "").strip()
        reason = request.form.get("reason", "").strip()

        # Validate required fields.
        if not all(
            [patient_name, appointment_date, appointment_time, reason]
        ):
            return render_template(
                "index.html",
                error="Please complete all the fields.",
                today=date.today().isoformat(),
                appointments=get_appointments(),
            ), 400

        if len(patient_name) > 100 or len(reason) > 500:
            return render_template(
                "index.html",
                error=(
                    "Name must be at most 100 characters "
                    "and reason at most 500 characters."
                ),
                today=date.today().isoformat(),
                appointments=get_appointments(),
            ), 400

        # Validate date and time formats.
        try:
            selected_date = date.fromisoformat(appointment_date)
            datetime.strptime(appointment_time, "%H:%M")
        except ValueError:
            return render_template(
                "index.html",
                error="Please enter a valid appointment date and time.",
                today=date.today().isoformat(),
                appointments=get_appointments(),
            ), 400

        # Prevent appointments in the past.
        if selected_date < date.today():
            return render_template(
                "index.html",
                error="Appointment date cannot be in the past.",
                today=date.today().isoformat(),
                appointments=get_appointments(),
            ), 400

        # Store the appointment in SQLite.
        with get_db_connection() as connection:
            connection.execute(
                """
                INSERT INTO appointments (
                    patient_name,
                    appointment_date,
                    appointment_time,
                    reason,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    patient_name,
                    appointment_date,
                    appointment_time,
                    reason,
                    datetime.now().isoformat(timespec="seconds"),
                ),
            )

        return redirect(url_for("home", booked="1"))

    booked = request.args.get("booked") == "1"

    return render_template(
        "index.html",
        booked=booked,
        today=date.today().isoformat(),
        appointments=get_appointments(),
    )


def get_appointments():
    """Retrieve saved appointments, ordered by date and time."""
    with get_db_connection() as connection:
        appointments = connection.execute(
            """
            SELECT
                id,
                patient_name,
                appointment_date,
                appointment_time,
                reason
            FROM appointments
            ORDER BY appointment_date ASC, appointment_time ASC, id ASC
            """
        ).fetchall()

    return appointments


@app.route("/health")
def health():
    """Health endpoint for Docker and Kubernetes checks."""
    return {"status": "healthy"}, 200


initialize_database()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
