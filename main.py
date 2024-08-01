from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    username: str
    age: int


users = []

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def main_page(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users, "user": None})

@app.get("/user/{user_id}", response_class=HTMLResponse)
def get_user(request: Request, user_id: int):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/user/{username}/{age}")
def add_user(username: str, age: int):
    if users:
        user_id = users[-1].id + 1
    else:
        user_id = 1

    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user

@app.put("/user/{user_id}/{username}/{age}")
def update_user(user_id: int, username: str, age: int):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")
