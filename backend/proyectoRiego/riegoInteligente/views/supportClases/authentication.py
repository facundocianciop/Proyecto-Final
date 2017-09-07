from riegoInteligente.models import Sesion

from django.http import request
from datetime import datetime
from functools import wraps


def autorizar(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if not 'sid' in request.cookies:
            output = {
                'error': 'No se envio cookie.',
                'url': request.url
            }
            res = output
            res.status_code = 401
            return res

        try:
            sesion = Sesion.get(
                Sesion.sid == request.cookies.get('sid'),
                Sesion.fecha_fin_sesion == None)

        except Sesion.DoesNotExist:
            # Si no se encontro la sesion se devuelve nada, como si hubiera
            # finalizado
            output = {
                'error': 'No se encontro sesion con ese sid.',
                'url': request.url
            }
            res = output
            res.status_code = 401
            return res

        # Obtener los tiempos en segundos para comparar
        delta1 = datetime.now() - datetime.utcfromtimestamp(0)
        delta2 = sesion.fecha_ultimo_acceso - \
                 datetime.utcfromtimestamp(0)

        # Si expiro la sesion se la finaliza y se devuelve nada
        if (delta1.seconds - delta2.seconds) >= 3600:
            sesion.fecha_fin_sesion = datetime.now()
            sesion.save()

            output = {
                'error': 'La sesion expiro.',
                'url': request.url
            }
            res = output
            res.status_code = 401
            return res

        # Si no expiro se actualiza la fecha de ultimo acceso y se
        # devuelve la cuenta asociada a la sesion
        sesion.fecha_ultimo_acceso = datetime.now()
        sesion.save()

        return f(sesion, *args, **kws)

    return decorated_function


def finalizar_sesion(sid):
    try:
        sesion = Sesion.get(Sesion.sid == sid, Sesion.fecha_fin_sesion == None)
        # Si se encontro la sesion se finaliza y se devuelve que la sesion
        # finalizo correctamente
        sesion.fecha_fin_sesion = datetime.now()
        sesion.save()
        return True

    except Sesion.DoesNotExist:
        # Si no se encontro la sesion se devuelve nada ya que la sesion es
        # incorrecta o ya finalizo
        print('No se encontro la sesion')
        return None