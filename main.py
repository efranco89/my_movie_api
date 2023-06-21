from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def message():
  return "Hello World From docker container does it reload? I added the reload instruction to uvicorn"