from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.login_page,
        name='login'
    ),

    path(
        'home/',
        views.home,
        name='home'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

]