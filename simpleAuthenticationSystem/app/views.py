from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
#home
def home(request):
    return render(request, "app/home.html")

#register (signUp)
def signUp(request):
    if request.method == "POST":
        username  = request.POST.get("username")
        firstname = request.POST.get("firstname")
        lastname  = request.POST.get("lastname")
        email     = request.POST.get("email")
        password  = request.POST.get("password")
        Cpassword = request.POST['confirmpassword']
        my_user = User.objects.create_user(username, email, password)
        my_user.first_name = firstname
        my_user.last_name  = lastname
        my_user.save()
        messages.success(request, "your account has being created successfully.")
        return redirect("signin")

    return render(request, "app/signup.html")

#signin
def signIn(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            username = user.first_name
            messages.success(request, "You login successfully")
            return redirect("home")
        else:
            messages.error(request, "Wrong Username or Password. try again !!")
            return redirect("signin")

    return render(request, "app/signin.html")

#Signout
def signOut(request):
    logout(request)
    messages.success(request, "logout successful")
    return redirect("home")
