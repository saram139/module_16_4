from fastapi import FastAPI, HTTPException, Path
from typing import Annotated
from pydantic import BaseModel

# uvicorn module_16_4:app --reload

app = FastAPI()

users = []

class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/users")
async def get_users():
    return users


@app.post("/user/{username}/{age}")
async def post_user(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")],
                    age: Annotated[int, Path(ge=18, le=120, description="Enter age", example='24')]):
    user_id = max((i.id for i in users), default=0) + 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description="Enter ID", example='1')], 
                      username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="UrbanProfi")],
                      age: Annotated[int, Path(ge=18, le=120, description="Enter age", example='28')]):
    try:
        user = users[user_id-1]
        user.username = username
        user.age = age
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')
    return user


@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description="Enter ID", example='2')]):
    for i, user in enumerate(users):
        if user.id == user_id:
            delete_user = users.pop(i)
            return delete_user
    raise HTTPException(status_code=404, detail='User was not found')

