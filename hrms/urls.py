from django.urls import path

from .views import (

    hr_dashboard,

    employee_list,

    add_employee,

    employee_info,

    edit_employee,

    delete_employee,

    department_list,

    add_department,

    designation_list,

    add_designation

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

    path(
        'employee-info/<int:id>/',
        employee_info
    ),

    path(
        'edit-employee/<int:id>/',
        edit_employee
    ),

    path(
        'delete-employee/<int:id>/',
        delete_employee
    ),

    path(
        'departments/',
        department_list
    ),

    path(
        'add-department/',
        add_department
    ),

    path(
        'designations/',
        designation_list
    ),

    path(
        'add-designation/',
        add_designation
    ),

]