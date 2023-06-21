from fastapi import FastAPI, Body
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
  },
  {
    "id": 2, 
    "title": "The eternal sunshine of a spotless mind",
    "overview": "Quis officia laborum anim ipsum cupidatat exercitation sint deserunt anim labore magna exercitation excepteur commodo.",
    "year": 2009,
    "rating": 7.8,
    "category": "Drama"
  }
]

@app.get("/", tags=['home'])
def message():
  return HTMLResponse("<h1> Hello World </h1>")

@app.get("/movies", tags=['movies'])
def get_movies():
  return movies

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
  for movie in movies:
    if movie["id"] == id:
      return movie 
    
@app.get("/movies/", tags=['movies'])
def get_movies_by_category(category: str):
  return list(filter(lambda movie : movie['category']== category, movies))

@app.post('/movies', tags=['movies'])
def create_movies(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
  movies.append({
    "id": id, 
    "title": title,
    "overview": overview,
    "year": year,
    "rating": rating,
    "category": category
  })
  return movies

@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
  for movie in movies: 
    if movie["id"] == id: 
      movie["title"] = title,
      movie["overview"] = overview,
      movie["year"] = year ,
      movie["rating"] = rating,
      movie["category"] = category
  return movies

@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
  for movie in movies: 
    if movie["id"] == id:
      movies.remove(movie)
  return movies
