from playhouse.pool import PooledPostgresqlDatabase
from urllib import parse
import os

class DB:

    def configure(self):
        parse.uses_netloc.append('postgres')
        url = parse.urlparse(os.getenv('DATABASE_URL'))
        return PooledPostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
