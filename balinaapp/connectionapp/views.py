from django.shortcuts import render

def api_connection(request):
    return render(request, "connectionapp/api_connection.html")
