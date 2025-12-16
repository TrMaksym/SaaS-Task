from fastapi import FastAPI

from routers import users, team, project, auth
from routers import tasks

app = FastAPI()

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(auth.router)
app.include_router(team.router)
app.include_router(project.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
