from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

movies = [
  {
    "id": 1, 
    "title": "Avatar",
    "overview": "Quis officia laborum anim ipsum cupidatat exercitation sint deserunt anim labore magna exercitation excepteur commodo.",
    "year": 2009,
    "rating": 7.8,
    "category": "Action"
  }
]

@app.get("/", tags=['home'])
def message():
  return HTMLResponse("<h1> Hello World </h1>")

@app.get("/movies", tags=['movies'])
def get_movies():
  return movies