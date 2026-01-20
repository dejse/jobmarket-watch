"""FastAPI main application"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from database import init_database
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler to initialize database on startup"""
    # Startup
    print("Initializing database...")
    init_database()
    print("Database initialized successfully!")
    yield
    # Shutdown (cleanup if needed)


# Initialize FastAPI app
app = FastAPI(
    title="Job Market Watch Austria",
    description="Dashboard for tracking job market trends in Austrian cities",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routes
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
