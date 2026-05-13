from fastapi import Request, Query, APIRouter
from db.consult import get_data
from typing import Optional



api_router = APIRouter(tags=['Clientes'])


@api_router.get('/contact-tag')
async def contact_tag(request: Request, tag_name: str = Query('')):
    db = request.app.state.db
    
    d = await get_data(db, tag_name)
    print(d)
    return d






