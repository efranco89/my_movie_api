from fastapi import APIRouter
from fastapi.responses import JSONResponse
from jwt_manager import create_token
from pydantic import BaseModel

user_router = APIRouter()

class User(BaseModel):
  email: str
  password: str
  
@user_router.post("/login", tags=['users'])
def login(user: User):
  if user.email == 'admin@gmail.com' and user.password == "admin":
    token: str = create_token(user.dict())
    return JSONResponse(status_code= 200, content=token)