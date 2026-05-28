from django.shortcuts import (

    render,
    redirect

)

from .models import (

    Department,
    Designation,
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

    context = {

        'total_employees':
        total_employees,

        'total_departments':
        total_departments,

        'total_designations':
        total_designations,

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

            personal_email=request.POST.get(
                'personal_email'
            ),

            mobile_no=request.POST.get(
                'mobile_no'
            ),

            personal_mobile=request.POST.get(
                'personal_mobile'
            ),

            employee_type=request.POST.get(
                'employee_type'
            ),

            ctc=request.POST.get(
                'ctc'
            ),

            notice_period=request.POST.get(
                'notice_period'
            ),

            reporting_manager=request.POST.get(
                'reporting_manager'
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

    }

    return render(

        request,
        'hrms/add_employee.html',
        context

    )