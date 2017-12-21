from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout


def account_login(request):
    errors = {}
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get("next", "/")
            return redirect(next_url)
        else:
            errors["error"] = "Wrong username or password!"
    return render(request, "login.html", {"errors": errors})

def account_logout(request):
    logout(request)
    return redirect("/account/login/")
