from core.server import server

import resources.historico
import resources.ativo
import resources.rotina

app = server.app

if __name__ == '__main__':    
    from core import models
    from service.rotinas import Rotina
    
    Rotina().inicia_jobs()
    models.initialize()
    server.run()
