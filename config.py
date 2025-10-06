"""
Configurações do banco de dados
"""

import os

# Configurações do NeonSQL (PostgreSQL)
# As credenciais devem ser configuradas via variáveis de ambiente
NEON_CONFIG = {
    'host': os.getenv('NEON_HOST', 'localhost'),
    'port': int(os.getenv('NEON_PORT', 5432)),
    'database': os.getenv('NEON_DATABASE', 'neondb'),
    'user': os.getenv('NEON_USER', 'neondb_owner'),
    'password': os.getenv('NEON_PASSWORD', ''),
    'sslmode': os.getenv('NEON_SSLMODE', 'require'),
    'channel_binding': os.getenv('NEON_CHANNEL_BINDING', 'require')
}

# String de conexão completa
NEON_CONNECTION_STRING = (
    f"postgresql://{NEON_CONFIG['user']}:{NEON_CONFIG['password']}@"
    f"{NEON_CONFIG['host']}/{NEON_CONFIG['database']}?"
    f"sslmode={NEON_CONFIG['sslmode']}&channel_binding={NEON_CONFIG['channel_binding']}"
)

# Configuração para usar NeonSQL (True) ou SQLite (False)
USE_NEON_DB = True  # Configurado para usar NeonSQL

# Configurações do SQLite (mantido para backup)
SQLITE_CONFIG = {
    'db_path': 'avaliacoes.db'
}
