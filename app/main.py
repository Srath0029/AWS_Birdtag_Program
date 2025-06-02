# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth  # Add other routers like dashboard when ready

app = FastAPI(
    title="BirdTag API",
    description="Backend for BirdTag project using FastAPI and AWS",
    version="0.1.0"
)

# CORS settings (relax as needed during dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
# app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

# Healthcheck endpoint
@app.get("/health", tags=["Meta"])
def health_check():
    return {"status": "ok"}
