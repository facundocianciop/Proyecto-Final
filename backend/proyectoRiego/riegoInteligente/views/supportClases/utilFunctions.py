from json import loads

def armarJson(request):
    received_json_data = str(request.body)
    datos = loads(received_json_data)
    return datos
