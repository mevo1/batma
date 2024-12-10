from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,get_object_or_404
from .models import Api
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def api_connection(request):
    return render(request, "connectionapp/api_connection.html")

@csrf_exempt
def get_api(request, id):
    api = get_object_or_404(Api, id=id)
    return JsonResponse({
        "name": Api.name,
        "address": Api.adress,
        "key": Api.secretkey,
        "user": request.user.id,
    })

def list_api(request):
    apis = Api.objects.filter(user=request.user).values()
    return JsonResponse(list(apis), safe=False)

@csrf_exempt
def add_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("api-name")
            adress = data.get("api-address")
            secretkey = data.get("api-secretkey")

            if Api.objects.filter(name=name, user_id=request.user.id).exists():
                return JsonResponse({"message": "There is an indicator with the same title!","info":"warning"})

            """if not name or not adress or not secretkey:
                return JsonResponse({"message": "Title and code are required.","info":"warning"})"""
            
            Api.objects.create(name=name, adress=adress, secretkey=secretkey, user_id=request.user.id)

            return JsonResponse({"message": "Indicator saved successfully.","info":"success"})
        except Exception as e:
            return JsonResponse({"message": (str(e)),"info":"errorr"})
