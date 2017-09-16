from json import loads
import string
import random

def armarJson(request):
    received_json_data = str(request.body)
    datos = loads(received_json_data)
    return datos
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
def armarJsonErrores(error,descripcion):
    json_error = {}
    json_error['error'] = error
    json_error['descripcion']=descripcion
    return json_error