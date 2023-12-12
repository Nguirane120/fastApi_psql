
from typing import List
from fastapi import Header, APIRouter, HTTPException
from app.api.models import MovieIn, MovieOut
from app.api import db_manager


fake_movie_db = [
    {
        'name': 'Star Wars: Episode IX - The Rise of Skywalker',
        'plot': 'The surviving members of the resistance face the First Order once again.',
        'genres': ['Action', 'Adventure', 'Fantasy'],
        'casts': ['Daisy Ridley', 'Adam Driver']
    }
]

movies = APIRouter()


@movies.get('/', response_model=List[MovieOut])
async def retrieve_movies():
    return await db_manager.get_all_movies()


@movies.post('/', status_code=201)
async def add_movie(payload: MovieIn):
    movie_id = await db_manager.add_movie(payload)
    response = {
        'id': movie_id,
        **payload.model_dump()
    }

    return response

@movies.get('/{id}')
async def retrieve_movie(id: int):
    try:
        movie = await db_manager.get_movie(id)
        if movie is None:
            raise HTTPException(status_code=404, detail="Movie not found")
        return movie
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@movies.put('/{id}')
async def update_movie(id: int, payload: MovieIn):
    movie = await db_manager.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    update_data = payload.model_dump(exclude_unset=True)
    movie_in_db = MovieIn(**movie)

    updated_movie = movie_in_db.model_copy(update=update_data)

    return await db_manager.update_movie(id, updated_movie)


@movies.delete('/{id}')
async def delete_movie(id: int):
    movie = await db_manager.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    await db_manager.delete_movie(id)
    return {"message":"movie deleted"}