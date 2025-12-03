from fastapi import FastAPI

from routers import users
from routers import movies

app = FastAPI()

app.include_router(users.router)
app.include_router(movies.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
