from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import json
from .filtrado import ejecutarResponse


@csrf_exempt
def mensajeEndPoint(request):
    response = []
    if request.method == "POST":
        print('======')
        data = request.body
        text = json.loads(data)['text']
        print(text)
        response = ejecutarResponse(text,json.loads(data)['user_name'])
    else:
        print('xddddddd')
    data = []
    print(response)
    for i in range (len(response)):
        data.append(
            {
                "id": i,
                "body": response[i],
            }
        )
    return HttpResponse(json.dumps(data))
