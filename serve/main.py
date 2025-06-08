from fastapi import FastAPI
from routers.router import router as tracking_router

app = FastAPI(
    title="MSC Tracking API",
    description="API to query container and bill of lading tracking information",
    version="1.0.0"
)

# Include API routers
app.include_router(tracking_router)