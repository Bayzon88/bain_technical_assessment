from fastapi import FastAPI

from src.api.insights.router import router

app = FastAPI(root_path='/api/v1')
app.include_router(router, prefix="/insights", tags=["insights"])


@app.get("/health")
def health():
    return {"status": "ok"}

