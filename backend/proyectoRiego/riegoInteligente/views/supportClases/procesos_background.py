import time

from riegoInteligente.models import *
from riegoInteligente.views.supportClases.views_constants import *
from riegoInteligente.views.supportClases.informacionClimatica.informacionClimatica import obtener_mediciones_finca


def obtener_mediciones_climaticas():

    # Iniciar proceso de obtencion de estado climatico para todas las fincas habilitadas

    estado_finca_habilitado = EstadoFinca.objects.get(nombreEstadoFinca=ESTADO_HABILITADO)
    historicos_habilitados = HistoricoEstadoFinca.objects.filter(estadoFinca=estado_finca_habilitado,
                                                                 fechaFinEstadoFinca__isnull=True)
    fincas_habilitadas = []
    for historico in historicos_habilitados:
        fincas_habilitadas.append(historico.finca)

    for finca in fincas_habilitadas:
        time.sleep(1)
        print finca.nombre
        obtener_mediciones_finca(finca.idFinca)
