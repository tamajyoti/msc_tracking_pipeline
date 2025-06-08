# 🚛 msc_tracking_pipeline

A data tracking pipeline built with Prefect and PostgreSQL, designed to schedule, run, and monitor ETL workflows seamlessly inside Docker containers.

---

## 📌 What This Project Does

This project provides an end-to-end ETL orchestration pipeline using:

- **Prefect** for workflow orchestration and scheduling
- **PostgreSQL** as the metadata and task result store
- **Docker Compose** for local development and service orchestration

It includes:
- A FastAPI or Python-based flow (`flow.py`) that performs data operations
- A Prefect Server to monitor and schedule flows
- A PostgreSQL database for storing Prefect metadata and custom data

---

## 🔧 Services Used

- **Prefect Server**: UI + API for flow scheduling, logs, and task status
- **Prefect Agent**: Executes the flows in the background
- **PostgreSQL**: Task metadata and data persistence
- **Docker Compose**: Service orchestration

---

## 🚀 How to Run It on Your Machine

### ✅ Prerequisites
#### To run the project locally follow the steps below

1. Create a .env file in the root directory, similar .env.sample
2. Ensure the DB_HOST name is added to all the depends on section of docker-compose
2. Run ```docker-compose -f docker-compose.prefect.yml up --build```
