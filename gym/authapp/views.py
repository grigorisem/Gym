from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def home(request):
    return render(request, "authapp/index.html")
def signup(request):
    if request.method == "POST":
        username = request.POST.get('usernumber')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if len(username) > 11 or len(username) < 11:
            messages.info(request, "В номере телефона должно быть 11 чисел")
            return redirect('/signup')
        if pass1 != pass2:
            messages.info(request, "Пароли не совпадают")
            return redirect('/signup')

        try:
            if User.objects.get(username=username):
                messages.warning(request, "Номер телефона уже занят")
                return redirect('/signup')
        except Exception as identifier:
            pass

        try:
            if User.objects.get(email=email):
                messages.warning(request, "Почта уже занята")
                return redirect('/signup')

        except Exception as identifier:
            pass
        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        messages.success(request, "Аккаунт создан, войдите в аккаунт")
        return redirect('/login')
    return render(request, "authapp/signup.html")


def handlelogin(request):
    if request.method == "POST":
        username = request.POST.get('usernumber')
        pass1 = request.POST.get('pass1')
        myuser = authenticate(username=username, password=pass1)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Вы успешно вошли в аккаунт")
            return redirect('/')
        else:
            messages.error(request, "Логин или пароль неверен")
            return redirect('/login')
    return render(request, "authapp/handlelogin.html")

def handlelogout(request):
    logout(request)
    messages.success(request,"Вы успешно вышли из аккаунта")
    return redirect('/login')

