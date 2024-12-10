from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404,render
from .models import Indicator, Coins
import json
import numpy as np
import pandas as pd
from .get_binance_data import get_binance_data
from django.contrib.auth.decorators import login_required

data = None



def indicators_page(request):
    chart_html = None # Grafiği HTML olarak render et, chartın içine at.
    coins = Coins.objects.all()       
    return render(request, 'customizationapp/indicator.html', {"coins": coins})

# GRAPH
def main_graph(request):
    global data
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            symbol = data.get("symbol")
            interval = data.get("interval")
            period = data.get("period")
            
            data = get_binance_data(symbol,interval,period)
            print("data")
            print(type(data["open"]))

            formatted_data = {
            "time": data["time"].dt.strftime("%Y-%m-%d %H:%M:%S").tolist(),
            "open": data["open"].tolist(),
            "high": data["high"].tolist(),
            "low": data["low"].tolist(),
            "close": data["close"].tolist(),
            }
            
            return JsonResponse(formatted_data)

        except Exception as e:
            return JsonResponse({"message": (str(e)),"info":"errorr"})

def update_graph(request,id):
    global data
    local_vars = {}
    
    if request.method == "POST":
        try:
            indicator = get_object_or_404(Indicator, id=id)

            time = data["time"]
            close = data["close"]
            open = data["open"]
            high = data["high"]
            low = data["low"]
            volume = data["volume"]

            exec(indicator.code, globals(), local_vars)

            if 'balina_indicator' in local_vars:
                result = local_vars['balina_indicator'](time,close,open,high,low,volume)
                result = result.replace([np.inf, -np.inf], None)
                #result = result.fillna(result.mean())
                result = result.iloc[:,0]

                data = {
                    "time": data["time"].dt.strftime("%Y-%m-%d %H:%M:%S").tolist(),
                    "result": result.tolist(),
                    "name": indicator.title
                }
                
                return JsonResponse(data, safe=False)
            else:
                return JsonResponse({"message": "Fonksiyon tanımlanmadı.","info":"errorr"})
            
        except Exception as e:
            return JsonResponse({"message": (str(e)),"info":"errorr"})



# INDICATORS
def list_indicators(request):
    indicators = Indicator.objects.filter(user=request.user).values()
    return JsonResponse(list(indicators), safe=False)

@csrf_exempt
def add_indicator(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            title = data.get("title")
            code = data.get("code")
            on_graph = data.get("on_graph", False)

            if Indicator.objects.filter(title=title, user_id=request.user.id).exists():
                return JsonResponse({"message": "There is an indicator with the same title!","info":"warning"})

            if not title or not code:
                return JsonResponse({"message": "Title and code are required.","info":"warning"})
            
            Indicator.objects.create(title=title, code=code, on_graph=on_graph, user_id=request.user.id)

            return JsonResponse({"message": "Indicator saved successfully.","info":"success"})
        except Exception as e:
            return JsonResponse({"message": (str(e)),"info":"errorr"})

@csrf_exempt
def update_indicator(request, id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            title = data.get("title")
            code = data.get("code")
            on_graph = data.get("on_graph", False)

            indicator = get_object_or_404(Indicator, id=id, user=request.user)

            if Indicator.objects.filter(title=title).exclude(id=id).exists():
                return JsonResponse({"message": "There is an indicator with the same title!","info":"warning"})

            if not title or not code:
                return JsonResponse({"message": "Title and code are required.","info":"warning"})

            indicator.title = title
            indicator.code = code
            indicator.on_graph = on_graph
            indicator.save()

            return JsonResponse({"message": "Indicator updated successfully.","info":"success"})
        except Exception as e:
            return JsonResponse({"message": (str(e)),"info":"errorr"})

def get_indicator(request, id):
    indicator = get_object_or_404(Indicator, id=id)
    return JsonResponse({
        "id": indicator.id,
        "title": indicator.title,
        "code": indicator.code,
        "on_graph": indicator.on_graph,
    })

def del_indicator(request, id):
    try:
        indicator = get_object_or_404(Indicator, id=id)
        indicator.delete()
        return JsonResponse({"message": "İndicator Deleted","info":"errorr"})
    except Exception as e:
        return JsonResponse({"message": (str(e)),"info":"errorr"})
    


