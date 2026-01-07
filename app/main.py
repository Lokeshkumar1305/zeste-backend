from fastapi import FastAPI
from app.routes.users import router as users_router
from app.db import connect_to_mongo, close_mongo_connection

# Create FastAPI app instance
app = FastAPI(
    title="Zeste Backend API",
    description="A simple FastAPI backend with MongoDB",
    version="1.0.0"
)

# Include routers
app.include_router(users_router)

# Startup event: connect to MongoDB
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

# Shutdown event: close MongoDB connection
@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Zeste Backend API"}