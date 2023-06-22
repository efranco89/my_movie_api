from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

class Movie(BaseModel):
  id: Optional[int] = None
  title: str = Field(min_length=5,max_length=15)
  overview: str = Field(min_length=15,max_length=255)
  year: int  = Field(le=2022)
  rating: float = Field(ge=0.0, le=10.0)
  category: str = Field(min_length=5, max_length=25)
  
  class Config:
    schema_extra = {
      "example": {
        "id": 1,
        "title": "my film",
        "overview": "Nostrud sit commodo exercitation ullamco consectetur esse cupidatat eu.",
        "year": 2022,
        "rating": 7.8,
        "category": "Action"
      }
    }

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

@app.get("/movies", tags=['movies'], response_model=List[Movie])
def get_movies() -> List[Movie]:
  return JSONResponse(content= movies)

@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
  for movie in movies:
    if movie["id"] == id:
      return JSONResponse(content=movie)
  return JSONResponse(content=[])
    
@app.get("/movies/", tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15))-> List[Movie]:
  movie = list(filter(lambda movie : movie['category']== category, movies))
  return JSONResponse(content=movie)

@app.post('/movies', tags=['movies'], response_model=dict)
def create_movies(movie: Movie) -> dict:
  movies.append(movie)
  return JSONResponse(content={"message": "The movie has been created"})

@app.put('/movies/{id}', tags=['movies'], response_model=dict)
def update_movie(id: int, movie: Movie) -> dict:
  for item in movies: 
    if item["id"] == id: 
      item['title'] = movie.title
      item['overview'] = movie.overview
      item['year'] = movie.year
      item['rating'] = movie.rating
      item['category'] = movie.category
  return JSONResponse(content={"message": "The movie has been updated"})

@app.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movie(id: int) -> dict:
  for movie in movies: 
    if movie["id"] == id:
      movies.remove(movie)
  return JSONResponse(content={"message": "The movie has been deletes"})
