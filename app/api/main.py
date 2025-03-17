from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

from .routers import player , room
from ..database.connect import create_all_table



def lifespan(app:FastAPI):
    try :
        create_all_table()
    except :
        raise Exception('DB IS NOT  WORKING PROPERLY')
    yield



app = FastAPI(lifespan=lifespan)

app.include_router(player.player_app,tags=["player"],prefix="/v1")
app.include_router(room.room_endpoint,tags=["room"],prefix="/v1")