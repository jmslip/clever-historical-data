from datetime import timedelta, datetime
from typing import OrderedDict
import pandas as pd
import numpy as np
import array

from pandas.core.frame import DataFrame
from service.calculos_geral import CalculosGeral

from service.historico import HistoricoService
from utils.clever_generics import CleverGenerics


class Calculos(CalculosGeral):

    def __init__(self) -> None:
        super().__init__()

    def rd(self, ativos):
        from_date, to_date = self.get_from_and_to_date()

        return self.rd_default(ativos=ativos, from_date=from_date, to_date=to_date)