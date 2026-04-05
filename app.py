from fastapi import FastAPI

app = FastAPI()

@app.post("/reset")
async def reset():
    return {"status": "ok"}