from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.insights.router import router

app = FastAPI(root_path='/api/v1')
app.include_router(router, prefix="/insights", tags=["insights"])

# Avoid CORS issues during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

