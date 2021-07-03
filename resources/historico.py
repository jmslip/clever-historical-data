from flask_restplus import Resource
import base64
import csv
import tempfile

from peewee import IntegrityError

from core.models import HistoricalData, Ativo as AtivoModel
from service.historico import HistoricoService
from utils.clever_generics import CleverGenerics
from core.server import server

app = server.app
api = server.api
clever_generics = CleverGenerics()

parametros = ['simbolo', 'tipo', 'data_inicio', 'data_fim']
parametros_obrigatorios = ['simbolo']
parametros_obrigatorios_post = ['binario']

@api.route('/historico')
class Historico(Resource):
    @staticmethod
    def get():
        response = api.payload
        
        err = clever_generics.valida_parametros_obrigatorios(request=response, parametros=parametros_obrigatorios)

        if err is not None:
            return err

        simbolo = response['simbolo']

        tipo = 'recente'

        if 'tipo' in response:
            tipo = response['tipo']

        if tipo == 'recente':
            return HistoricoService().recente(simbolo)
        elif tipo == 'passado':
            err = clever_generics.valida_parametros_obrigatorios(request=response, parametros=parametros)

            if err is not None:
                return err

            data_inicio = response['data_inicio']
            data_fim = response['data_fim']

            return HistoricoService().passado(ativo=simbolo, from_date=data_inicio, to_date=data_fim)

        else:
            return clever_generics.gera_resposta(clever_generics.err04)

    
    def post(self):
        request = api.payload

        err = clever_generics.valida_parametros_obrigatorios(request=request, parametros=parametros_obrigatorios_post)
        if err is not None:
            return err

        binario = request['binario']
        arquivo_csv = binario.encode('utf8')

        filename = tempfile.TemporaryDirectory().name

        with open(filename, 'wb') as file_to_save:
            file_decode = base64.decodebytes(arquivo_csv)
            file_to_save.write(file_decode)

        historico_model = HistoricalData
        with open(filename, 'r') as ficheiro:
            reader = csv.reader(ficheiro, delimiter=';')
            for row in reader:
                if row[0] == 'data_historico':
                    continue
                historico_model = HistoricalData(
                    data_historico = clever_generics.formata_datestr(strdata=row[0], pattern="%d/%m/%Y", typefor='bd'),
                    variacao = row[1],
                    ativo = AtivoModel().select().where(AtivoModel.id == int(row[2])).get()
                )

                try:
                    historico_model.save()
                except IntegrityError as e:
                    print("Erro ao salvar histórico: ", e)
                    error = e.args
                    for err in error:
                        if 'duplicate key' in err:
                            return clever_generics.gera_resposta(clever_generics.err05)
                    return clever_generics.gera_resposta(clever_generics.err04)
        
        return clever_generics.gera_resposta("Importado com sucesso!!!")
        
