from core.server import server

import resources.historico

app = server.app

@app.before_first_request
def cria_banco():
    db.create_all()


if __name__ == '__main__':
    from core.db import db
    db.init_app(app)
    server.run()