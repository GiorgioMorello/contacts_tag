from fastapi import FastAPI, Request, Query
from contextlib import asynccontextmanager
from db.config import create_pool, create_tunnel
from api import api_router

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


@app.get('/test')
async def tets():
    print('OK')
    return 'OK'



