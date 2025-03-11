from fastapi import FastAPI
from .routers import player
from ..database.connect import create_all_table



def lifespan(app:FastAPI):
    try :
        create_all_table()
    except :
        raise Exception('DB IS NOT  WORKING PROPERLY')
    yield



app = FastAPI(lifespan=lifespan)

app.include_router(player.player_app,tags=["player"],prefix="/v1")