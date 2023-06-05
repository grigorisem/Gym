from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name = 'home'),
    path('signup', views.signup, name='signup'),
    path('login', views.handlelogin, name='handlelogin'),
    path('logout', views.handlelogout, name='handlelogout'),

]