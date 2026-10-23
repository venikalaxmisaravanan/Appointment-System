# Appointment System

**Roll Number:** 24MIS0117

A web application developed as part of an academic project
to demonstrate application versioning and CI/CD deployment.

## Version 1 — Book an Appointment

Version 1 implements the appointment booking feature.

### Features

- Enter patient name
- Select appointment date
- Select appointment time
- Enter appointment reason
- Validate required fields
- Prevent booking appointments in the past
- Store appointments in SQLite
- Display booking confirmation
- Health endpoint for deployment checks

## Technology Stack

- Python
- Flask
- HTML and CSS
- SQLite
- Git and GitHub
- Jenkins
- Docker
- DockerHub
- Kubernetes

## Project Structure

```text
AppointmentSystem/
├── app.py
├── requirements.txt
├── Dockerfile
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    └── style.css