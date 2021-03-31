from datetime import date, datetime
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

from peewee import IntegrityError, InternalError

from service.historico import HistoricoService
from service.ativos import Ativos
from core.models import HistoricalData as HistoricoModel
from core.models import Ativo as AtivoModel
from core.models import close_connection
from utils.clever_generics import CleverGenerics


class Rotina():

    def __init__(self) -> None:
        self.dados_historicos = HistoricoService()
        self.ativos = Ativos()
        self.clever_generics = CleverGenerics()

    
    def atualiza_historico_por_data(self, from_date, to_date, ativo=None):
        if ativo is not None:
            ativos_atualizar = ativo
        else:
            ativos_atualizar = self.ativos.all_ativos_banco()

        for ativo in ativos_atualizar:
            dados = self.dados_historicos.passado_data(ativo=ativo['simbolo'], from_date=from_date, to_date=to_date)

            for item in dados:
                self.persiste_dados_historico_ativo(item)
        
        return True

    
    def atualiza_historico(self):
        all_ativos = self.ativos.all_ativos_banco()

        historicoModel = HistoricoModel()
        is_save = False
        existe_ativo_bd = False
        for ativo in all_ativos:
            dados = self.dados_historicos.recente(ativo=ativo['simbolo'])
            for simbolo, dado in dados.items():
                for data, valor in dado.items():
                    historico_ativo = (
                        AtivoModel.select()
                                .join(HistoricoModel)
                                .where(HistoricoModel.data_historico == data, AtivoModel.simbolo == simbolo)
                    )

                    for ativo_db in historico_ativo:
                        existe_ativo_bd = True

                    if not existe_ativo_bd:
                        is_save = True
                        historicoModel = HistoricoModel(
                            data_historico = data,
                            ultimo = valor['Close'],
                            variacao = valor['var'],
                            ativo = AtivoModel().select().where(AtivoModel.simbolo == simbolo).get()
                        )

            try:
                if is_save:
                    historicoModel.save()
            except IntegrityError as integrity:
                print(integrity)
                return self.clever_generics.gera_resposta(self.clever_generics.err04)
            except InternalError as internal:
                print(internal)
                return self.clever_generics.gera_resposta(self.clever_generics.err04)
            
            close_connection()



    def persiste_dados_historico_ativo(self, dados):
        historicoModel = HistoricoModel()
        existe_ativo_bd: bool = False
        is_save: bool

        for simbolo, dado in dados.items():
            for data, valor in dado.items():
                historico_ativo = (
                    AtivoModel.select()
                            .join(HistoricoModel)
                            .where(HistoricoModel.data_historico == data, AtivoModel.simbolo == simbolo)
                )

                for ativo_db in historico_ativo:
                    existe_ativo_bd = True

                if not existe_ativo_bd:
                    is_save = True
                    historicoModel = HistoricoModel(
                        data_historico = data,
                        ultimo = valor['Close'],
                        variacao = valor['var'],
                        ativo = AtivoModel().select().where(AtivoModel.simbolo == simbolo).get()
                    )

        try:
            if is_save:
                historicoModel.save()
        except IntegrityError as integrity:
            print(integrity)
            return self.clever_generics.gera_resposta(self.clever_generics.err04)
        except InternalError as internal:
            print(internal)
            return self.clever_generics.gera_resposta(self.clever_generics.err04)
        
        close_connection()
        return True


    def add_job(self, function, scheduler: BackgroundScheduler = None, trigger='cron', **kwargs) -> BackgroundScheduler:
        if scheduler is None:
            scheduler = BackgroundScheduler()        
        
        scheduler.add_job(func=function, trigger=trigger, day="*", hour='1', minute="30")

        return scheduler


    def get_ultima_data_historico(self, ativo: str = None) -> date:
        if ativo is not None:
            ativo = ativo.upper()
            ultima_data = HistoricoModel.select(HistoricoModel.data_historico).join(AtivoModel).where(AtivoModel.simbolo == ativo).order_by(HistoricoModel.data_historico.desc()).limit(1).get()
        else:
            ultima_data = HistoricoModel.select(HistoricoModel.data_historico).order_by(HistoricoModel.data_historico.desc()).limit(1).get()
        
        return ultima_data.data_historico


    def start_jobs(self, scheduler: BackgroundScheduler):
        scheduler.start()

        atexit.register(lambda: scheduler.shutdown())


    def inicia_jobs(self):
        scheduler = self.add_job(function=self.atualiza_historico)

        self.start_jobs(scheduler=scheduler)
    