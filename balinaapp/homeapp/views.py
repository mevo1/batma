from django.shortcuts import redirect, render
from django.contrib.auth.models import User

# Create your views here.
def profile(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    return render(request, "homeapp/profile.html")