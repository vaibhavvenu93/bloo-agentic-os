from fastapi import FastAPI

app = FastAPI(
    title="BLOO",
    description="Agentic operating layer for company intelligence and execution.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "product": "BLOO",
        "status": "online",
        "mission": "Help small teams operate with more intelligence, leverage, and fewer dropped loops.",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
