from fastapi import FastAPI
from .database import init_db
from .routes import router

app = FastAPI(title="Caching Service")

# Initialize database
@app.on_event("startup")
def on_startup():
    init_db()

# Include routes
app.include_router(router)
