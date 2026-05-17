from fastapi import FastAPI, Request, Query
from contextlib import asynccontextmanager
from db.config import create_pool, create_tunnel
from api import api_router
from fastapi.middleware.cors import CORSMiddleware
from settings.settings import SETTINGS


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    print('Iniciando')
    
    ssh_tunnel = create_tunnel()

    db = await create_pool()
    
    app.state.db = db
    app.state.ssh_tunnel = ssh_tunnel
    
    yield
    
    print("Encerrando aplicação")
    
    await app.state.db.close()
    app.state.ssh_tunnel.stop()



app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=SETTINGS.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)




@app.get('/test')
async def tets():
    print('OK')
    return 'OK'



