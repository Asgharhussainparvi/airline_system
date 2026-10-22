from fastapi import FastAPI

from app.routers.customers import router as customers_router

app = FastAPI(
    title="AI-Powered Airline Ticketing System",
    description="Backend API for the Airline Ticketing FYP.",
    version="0.1.0",
)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Report whether the API process is responding."""
    return {"status": "ok"}


app.include_router(customers_router)