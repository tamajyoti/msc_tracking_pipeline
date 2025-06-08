# 🚛 msc_tracking_pipeline

A data tracking pipeline built with Prefect and PostgreSQL, designed to schedule, run, and monitor ETL workflows seamlessly inside Docker containers.

---

## 🚀 How to Run It on Your Machine

### ✅ Prerequisites
#### To run the project locally follow the steps below

1. Create a .env file in the root directory, similar .env.sample
2. Ensure the DB_HOST name is added to all the depends on section of docker-compose
3. Run ```docker-compose -f docker-compose.prefect.yml up --build```
