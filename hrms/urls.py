from django.urls import path

from .views import (

    hr_dashboard,

    employee_list,

    add_employee

)

urlpatterns = [

    path(
        '',
        hr_dashboard
    ),

    path(
        'employees/',
        employee_list
    ),

    path(
        'add-employee/',
        add_employee
    ),

]