from fastapi import FastAPI

app = FastAPI(title="Smart Travel Expense Manager")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Smart Travel Expense Manager API"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
