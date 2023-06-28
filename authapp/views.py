from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Enrollment, MembershipPlan
from django.http import HttpResponse
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
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

def enroll(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Войдите в аккаунт")
        return redirect('/login')

    Membership=MembershipPlan.objects.all()
    context={"Membership":Membership}
    if request.method=="POST":
        FullName=request.POST.get('fullname')
        gender=request.POST.get('gender')
        PhoneNumber=request.POST.get('number')
        DOB=request.POST.get('DOB')
        member=request.POST.get('member')
        address=request.POST.get('address')
        query=Enrollment(FullName=FullName,Gender=gender,PhoneNumber=PhoneNumber,DOB=DOB,SelectMembershipPlan=member,Address=address)
        query.save()
        messages.success(request,"Спасибо за участие")
        return redirect('/')
    return render(request,"authapp/enrollment.html",context)

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Войдите в аккаунт")
        return redirect('/login')
    user_phone=request.user
    posts=Enrollment.objects.filter(PhoneNumber=user_phone)
    context={"posts":posts}
    return render(request,"authapp/profile.html",context)
def report(request):
    clients = Enrollment.objects.all()
    plannum = MembershipPlan.objects.all()
    if not request.user.is_authenticated:
        messages.warning(request,"Войдите в аккаунт")
        return redirect('/login')
    context = {
        'clients': clients,
        'plannum': plannum
    }

    return render(request, 'authapp/report.html', context)
def destroy(request, id):
    employee = Enrollment.objects.get(id=id)
    employee.delete()
    return redirect('/report')
def fetch_resources(uri, rel):
    path = os.path.join(uri.replace(settings.STATIC_URL, ""))
    return path

def pdfcreate(request):
    clients = Enrollment.objects.all()
    template_path = 'authapp/pdfReport.html'
    context = {'clients': clients}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="clients_report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Возникла ошибка при создании отчета')
    return response



