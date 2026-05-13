from asyncpg.pool import Pool




company_id = ''


async def get_data(pool: Pool, tag_name: str=''):
    
    query = """

    
    select c."name" as "Contato", c.phone as "Número", t."name" as "Tag" from contacts c
    inner join companies c2 on c.company_id=c2.id 
    inner join contact_vs_tags cvt on cvt.contact_id=c.id 
    inner join tags t on t.id=cvt.tag_id and t.company_id=c2.id 
    where c2.id = $1


    """
    
    params = [company_id]
    
    if tag_name:
        query += ' and t.name = $2'
        params.append(tag_name)
    
    async with pool.acquire() as c:
        rows = await c.fetch(
            query,
            *params
        )
        
        return [dict(r) for r in rows]
        