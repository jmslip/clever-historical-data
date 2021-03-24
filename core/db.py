from peewee import PostgresqlDatabase

from instance.config import DB_ADDR, DB_NAME, DB_PASS, DB_PORT, DB_USER

class DB:

    def configure(self):
        return PostgresqlDatabase(DB_NAME, user=DB_USER, password=DB_PASS, host=DB_ADDR)
