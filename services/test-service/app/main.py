from fastapi import FastAPI

app = FastAPI()


@app.get("/hi")
def say_hi():
    return {"message": "hi"}
