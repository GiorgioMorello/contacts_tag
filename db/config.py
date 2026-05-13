import asyncpg
from asyncpg.pool import Pool
from sshtunnel import SSHTunnelForwarder

from settings.settings import SETTINGS


async def create_pool() -> Pool:
    return await asyncpg.create_pool(
        user=SETTINGS.DB_USER,
        password=SETTINGS.DB_PASSWORD,
        database=SETTINGS.DB_NAME,
        host='127.0.0.1',
        port=6543,

        min_size=2, # Mantem pelo menos duas conexões abertas
        max_size=5, # O pool pode abrir no máximo 5 conexões simultâneas 
    )
    
    
def create_tunnel():
    
    tunnel = SSHTunnelForwarder(
        (SETTINGS.SSH_HOST, SETTINGS.SSH_PORT),
        ssh_username=SETTINGS.SSH_USER,
        ssh_pkey=SETTINGS.SSH_PRIVATE_KEY,
        ssh_private_key_password=SETTINGS.SSH_PRIVATE_KEY_PASS,
        remote_bind_address=(SETTINGS.DB_HOST, SETTINGS.DB_PORT),
        local_bind_address=('127.0.0.1', 6543),
        
    )
    
    tunnel.start()
    
    return tunnel





# O asyncpg NÃO conecta diretamente no PostgreSQL remoto.
#
# Primeiro criamos um túnel SSH local:
#
#     127.0.0.1:6543
#
# Esse túnel funciona como um proxy/forwarder TCP.
#
# Tudo que chegar em:
#
#     localhost:6543
#
# será encaminhado criptografado via SSH para:
#
#     DB_HOST:DB_PORT
#
# Fluxo real:
#
# asyncpg
#    ↓
# 127.0.0.1:6543   (túnel SSH local)
#    ↓
# SSH Tunnel
#    ↓
# PostgreSQL remoto (DB_HOST:5432)
#
# Portanto, o asyncpg deve conectar no HOST/PORT LOCAL do túnel,
# e NÃO diretamente no host remoto do PostgreSQL.