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
        'materials/',
        views.materials_page,
        name='materials'
    ),

    path(
        'add-material/',
        views.add_material,
        name='add_material'
    ),

    path(
        'transactions/',
        views.transactions_page,
        name='transactions'
    ),

    path(
        'add-transaction/',
        views.add_transaction,
        name='add_transaction'
    ),

    path(
        'projects/',
        views.projects_page,
        name='projects'
    ),

    path(
        'add-project/',
        views.add_project,
        name='add_project'
    ),

    path(
        'summary/',
        views.summary_page,
        name='summary'
    ),

]