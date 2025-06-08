from prefect import flow, task
from datetime import timedelta
from main import main as tracking_main

@task(retries=3, retry_delay_seconds=30)
def run_tracking_main():
    tracking_main()

@flow(name="Run Schedule Data Caller")
def tracking_flow():
    run_tracking_main()

if __name__ == "__main__":
    tracking_flow.serve(
        name="run-main-every-5min",
        interval=timedelta(minutes=5),  # every 5 minutes
        tags=["tracking"]
    )