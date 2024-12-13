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
        "secretkey": Api.secretkey,
        "user": request.user.id,
    })

def list_api(request):
    apis = Api.objects.filter(user=request.user).values()
    return JsonResponse(list(apis), safe=False)

@csrf_exempt
def update_api(request, id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            adress = data.get("address")
            secretkey = data.get("secretkey")

            api = get_object_or_404(Api, id=id, user=request.user)

            if Api.objects.filter(name=name).exclude(id=id).exists():
                return JsonResponse({"message": "There is an indicator with the same title!","info":"warning"})

            if not name or not adress or not secretkey:
                return JsonResponse({"message": "Title and code are required.","info":"warning"})

            api.name = name
            api.adress = adress
            api.secretkey = secretkey
            api.save()

            return JsonResponse({"message": "Indicator updated successfully.","info":"success"})
        except Exception as e:
            return JsonResponse({"message": (str(e)),"info":"errorr"})



@csrf_exempt
def add_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            adress = data.get("adress")
            secretkey = data.get("secretkey")
            print(data, name, adress,secretkey)
            if Api.objects.filter(name=name, user_id=request.user.id).exists():
                return JsonResponse({"message": "There is an indicator with the same title!","info":"warning"})

            if not name or not adress or not secretkey:
                return JsonResponse({"message": adress,"info":"warning"})
            if not adress or not secretkey:
                return JsonResponse({"message": "Title and code are required.","info":"warning"})
            Api.objects.create(name=name, adress=adress, secretkey=secretkey, user_id=request.user.id)

            return JsonResponse({"message": "Indicator saved successfully.","info":"success"})
        except Exception as e:
            return JsonResponse({"message": (str(e)),"info":"errorr"})

