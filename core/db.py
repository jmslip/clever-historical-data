from playhouse.pool import PooledPostgresqlDatabase

from core.config import DB_ADDR, DB_NAME, DB_PASS, DB_USER

class DB:

    def configure(self):
        return PooledPostgresqlDatabase(DB_NAME, max_connections=8, stale_timeout=300, user=DB_USER, password=DB_PASS, host=DB_ADDR)
