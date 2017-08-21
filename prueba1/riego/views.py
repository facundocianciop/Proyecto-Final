from django.http import HttpResponse,JsonResponse
from riego.models import Sector
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder



def index(request):
    return HttpResponse("Hello, world. You're at the riego index.")
def sector(request):
    s= Sector.objects.get(numeroSector=1)
    #json= serialize('json', Sector.objects.all(), cls=DjangoJSONEncoder) CON ESTO RETORNA TODOS LOS OBJETOS SECTOR
    json=serialize('json',[s])#ASI ES PARA UN SOLO OBJETO
    return JsonResponse(json,safe=False)