from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "TaskFlow API is running"}