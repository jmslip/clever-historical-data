from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, FormParser, JSONParser, MultiPartParser
from datetime import date
from base64 import b64decode
import csv
import json

from cleverbot.utils.cleverbotgeneric import cleverbot_generic

param_data_inicio = 'data_inicio'
param_data_fim = 'data_fim'


@api_view(http_method_names=['GET'])
@parser_classes([JSONParser])
def historico(request):
    data_fim = date.today()
    data_inicio = ''

    if param_data_inicio not in request.query_params:
        return Response(cleverbot_generic.gera_resposta(cleverbot_generic.err_falta_param, param_data_inicio))
    else:
        data_inicio = request.query_params[param_data_inicio]
    
    if param_data_fim in request.query_params:
        data_fim = request.query_params[param_data_fim]

    return Response({param_data_inicio: data_inicio, param_data_fim: data_fim})


@api_view(http_method_names=['POST'])
@parser_classes([JSONParser])
def importar(request):
    binario = request.data["binario"]
    file = b64decode(binario)

    print(file)

    

    
    return Response({})