from django.shortcuts import (

    render,
    redirect

)

from .models import (

    Department,
    Designation,
    Role,
    Employee

)


# HR DASHBOARD

def hr_dashboard(request):

    total_employees = (
        Employee.objects.count()
    )

    total_departments = (
        Department.objects.count()
    )

    total_designations = (
        Designation.objects.count()
    )

    total_roles = (
        Role.objects.count()
    )

    context = {

        'total_employees':
        total_employees,

        'total_departments':
        total_departments,

        'total_designations':
        total_designations,

        'total_roles':
        total_roles,

    }

    return render(

        request,
        'hrms/hr_dashboard.html',
        context

    )


# EMPLOYEE LIST

def employee_list(request):

    employees = (
        Employee.objects.all().order_by('-id')
    )

    context = {

        'employees': employees

    }

    return render(

        request,
        'hrms/employee_list.html',
        context

    )


# ADD EMPLOYEE

def add_employee(request):

    departments = (
        Department.objects.all()
    )

    designations = (
        Designation.objects.all()
    )

    roles = (
        Role.objects.all()
    )

    if request.method == "POST":

        Employee.objects.create(

            employee_code=request.POST.get(
                'employee_code'
            ),

            first_name=request.POST.get(
                'first_name'
            ),

            last_name=request.POST.get(
                'last_name'
            ),

            email=request.POST.get(
                'email'
            ),

            mobile_no=request.POST.get(
                'mobile_no'
            ),

            department=Department.objects.get(
                id=request.POST.get(
                    'department'
                )
            ),

            designation=Designation.objects.get(
                id=request.POST.get(
                    'designation'
                )
            ),

            role=Role.objects.get(
                id=request.POST.get(
                    'role'
                )
            ),

            joining_date=request.POST.get(
                'joining_date'
            ),

        )

        return redirect(
            '/hr/employees/'
        )

    context = {

        'departments': departments,

        'designations': designations,

        'roles': roles,

    }

    return render(

        request,
        'hrms/add_employee.html',
        context

    )