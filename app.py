import os
import sqlite3
from datetime import date, datetime
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)

DATABASE_PATH = Path(
    os.environ.get("DATABASE_PATH", "instance/appointments.db")
)


def get_db_connection():
    """Create a connection to the SQLite database."""

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """Create the appointments table if it does not already exist."""

    with get_db_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                reason TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


@app.route("/", methods=["GET", "POST"])
def home():
    """Display appointments and handle new appointment bookings."""

    error = None

    if request.method == "POST":
        patient_name = request.form.get(
            "patient_name", ""
        ).strip()

        appointment_date = request.form.get(
            "appointment_date", ""
        ).strip()

        appointment_time = request.form.get(
            "appointment_time", ""
        ).strip()

        reason = request.form.get(
            "reason", ""
        ).strip()

        # Validate required fields.
        if not all(
            [
                patient_name,
                appointment_date,
                appointment_time,
                reason,
            ]
        ):
            error = "Please fill in all the fields."

        elif len(patient_name) > 100:
            error = "Patient name must not exceed 100 characters."

        elif len(reason) > 500:
            error = "Reason must not exceed 500 characters."

        else:
            try:
                selected_date = date.fromisoformat(
                    appointment_date
                )

                datetime.strptime(
                    appointment_time, "%H:%M"
                )

                if selected_date < date.today():
                    error = "Appointment date cannot be in the past."

            except ValueError:
                error = (
                    "Please enter a valid appointment date and time."
                )

        # Save the appointment when validation succeeds.
        if error is None:
            with get_db_connection() as connection:
                connection.execute(
                    """
                    INSERT INTO appointments (
                        patient_name,
                        appointment_date,
                        appointment_time,
                        reason
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        patient_name,
                        appointment_date,
                        appointment_time,
                        reason,
                    ),
                )

            return redirect(url_for("home", booked="1"))

    # Retrieve appointments for the table.
    with get_db_connection() as connection:
        appointments = connection.execute(
            """
            SELECT
                id,
                patient_name,
                appointment_date,
                appointment_time,
                reason,
                created_at
            FROM appointments
            ORDER BY appointment_date, appointment_time, id
            """
        ).fetchall()

    return render_template(
        "index.html",
        appointments=appointments,
        today=date.today().isoformat(),
        booked=request.args.get("booked") == "1",
        cancelled=request.args.get("cancelled") == "1",
        error=error,
    )


@app.route("/cancel/<int:appointment_id>", methods=["POST"])
def cancel_appointment(appointment_id):
    """Cancel an existing appointment using its unique ID."""

    with get_db_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM appointments WHERE id = ?",
            (appointment_id,),
        )

        appointment_found = cursor.rowcount > 0

    if appointment_found:
        return redirect(url_for("home", cancelled="1"))

    return redirect(url_for("home", not_found="1"))


@app.route("/health")
def health():
    """Health endpoint for Docker and Kubernetes checks."""

    return {"status": "healthy"}, 200


initialize_database()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )