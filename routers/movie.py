from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional, List
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from middelwares.jwt_bearer import JWTBearer
from models.movie import Movie as MovieModel
from pydantic import BaseModel
from config.database import Session

movie_router = APIRouter()

class Movie(BaseModel):
  id: Optional[int] = None
  title: str = Field(min_length=5,max_length=255)
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

@movie_router.get("/", tags=['home'])
def message():
  return HTMLResponse("<h1> Hello World </h1>")

@movie_router.get("/movies", tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
  db = Session()
  movies_from_db = db.query(MovieModel).all()
  return JSONResponse(status_code=200, content= jsonable_encoder(movies_from_db))

@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
  db = Session()
  movie = db.query(MovieModel).filter_by(id = id).first()
  if movie: 
    return JSONResponse(status_code= 200, content=jsonable_encoder(movie))
  else:
    return JSONResponse(status_code=404, content={'message': 'Not Found'})
    
@movie_router.get("/movies/", tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15))-> List[Movie]:
  db = Session()
  movie = db.query(MovieModel).filter_by(category = category).all()
  if movie: 
    return JSONResponse(status_code= 200, content=jsonable_encoder(movie))
  else:
    return JSONResponse(status_code=404, content={'message': 'Not Found'})

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movies(movie: Movie) -> dict:
  db = Session()  
  new_movie = MovieModel(**movie.dict())
  db.add(new_movie)
  db.commit()
  return JSONResponse(status_code=201, content={"message": "The movie has been created"})

@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
  db = Session()
  item = db.query(MovieModel).filter_by(id = id).first()
  if movie:
    item.title = movie.title
    item.overview = movie.overview
    item.year = movie.year
    item.rating = movie.rating
    item.category = movie.category
    db.commit()
    return JSONResponse(status_code=200,content={"message": "The movie has been updated"})
  else:
    return JSONResponse(status_code=404, content={'message': 'Not Found'})

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
  
  db = Session()
  item = db.query(MovieModel).filter_by(id = id).first()
  if item: 
    db.delete(item)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "The movie has been deleted"})
  else:
    return JSONResponse(status_code=404, content={'message': 'Not Found'})