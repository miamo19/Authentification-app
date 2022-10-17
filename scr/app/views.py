from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .token import generatorToken

from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from authentification import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
def home(request):
    return render(request, "app/index.html")
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        cpasswd = request.POST['confirmpassword']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! change Username")
            return redirect("register")
        if User.objects.filter(email=email):
            messages.error(request, "email already exist! change email address")
            return redirect("register")
        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric only")
            return redirect("register")
        if password != cpasswd:
            messages.error(request, "Confirm password does not match password. try again!!")
            return redirect("register")
        my_user = User.objects.create_user(username, email, password)
        my_user.first_name = firstname
        my_user.last_name = lastname
        my_user.is_active = False
        my_user.save()
        messages.success(request, "Your account has being created successfully ")

#send a Welcome message to mail box
        subject = "Welcome to mia~code login system"
        message = "Hello "+ my_user.first_name + ' '+ my_user.last_name + ' we are happy you visited our site, \n\n\n Thanks for contacting us \n\n Hyacinthe system manager'
        from_email = settings.EMAIL_HOST_USER
        to_list = [my_user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)

#Email Confirmation
        current_site = get_current_site(request)
        email_subject = 'Mia~code Account Confirmation Address'
        messageConfirm = render_to_string("emailconfirm.html", {
            "name": my_user.first_name,
            "domain":current_site,
            "uid":urlsafe_base64_encode(force_bytes(my_user.pk)),
            'token': generatorToken.make_token(my_user)
        })
        email = EmailMessage(
            email_subject,
            messageConfirm,
            settings.EMAIL_HOST_USER,
            [my_user.email]
        )
        email.fail_silently = False
        email.send()

        return redirect("login")

    return render(request, "app/register.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username):
            messages.error(request, "Wrong username, try again")
            return redirect("login")

        user = authenticate(username=username, password=password)

        my_user = User.objects.get(username=username) #handle elif
        if user is not None:
            login(request, user)
            firstname = user.first_name
            return redirect('home')
#trying to login without activating account
        elif my_user.is_active == False:
            messages.error(request, 'You have not confirm your account. check your mail')

        else:
            messages.error(request, 'Something went wrong!! \n Wrong Username or Password, try again')
            return redirect("login")

    return render(request, "app/login.html")
def logout_user(request):
    logout(request)
    messages.success(request, "logout successful")
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generatorToken.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has being activated successfully. you can login now")
        return redirect("login")
    else:
        messages.error(request, "account activation has Failed!!! try again later")
        return redirect('home')
