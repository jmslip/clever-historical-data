from core.server import server
from flask_migrate import Migrate

import resources.historico
import resources.ativo

app = server.app

if __name__ == '__main__':    
    from core import models
    
    models.initialize()
    server.run()
