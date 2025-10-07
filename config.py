"""
Configurações do banco de dados
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do NeonSQL (PostgreSQL)
# Credenciais configuradas diretamente para garantir funcionamento
NEON_CONFIG = {
    'host': 'ep-fancy-darkness-acgn9qcf-pooler.sa-east-1.aws.neon.tech',
    'port': 5432,
    'database': 'neondb',
    'user': 'neondb_owner',
    'password': 'npg_lROacu8Iib4U',
    'sslmode': 'require',
    'channel_binding': 'require'
}

# String de conexão completa
NEON_CONNECTION_STRING = (
    f"postgresql://{NEON_CONFIG['user']}:{NEON_CONFIG['password']}@"
    f"{NEON_CONFIG['host']}/{NEON_CONFIG['database']}?"
    f"sslmode={NEON_CONFIG['sslmode']}&channel_binding={NEON_CONFIG['channel_binding']}"
)

# Configuração para usar NeonSQL (True) ou SQLite (False)
USE_NEON_DB = True  # Configurado para usar NeonSQL
