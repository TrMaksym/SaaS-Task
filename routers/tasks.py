from fastapi import APIRouter

router = APIRouter()

@router.get("/movies/")
async def read_movies():
    return {"message": "List of movies"}