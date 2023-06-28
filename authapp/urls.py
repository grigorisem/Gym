from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name = 'home'),
    path('signup', views.signup, name='signup'),
    path('login', views.handlelogin, name='handlelogin'),
    path('logout', views.handlelogout, name='handlelogout'),
    path('join', views.enroll, name='enroll'),
    path('profile', views.profile, name='profile'),
    path('report', views.report, name='report'),
    path('delete/<int:id>', views.destroy),
    path('pdf', views.pdfcreate, name='pdf'),
]