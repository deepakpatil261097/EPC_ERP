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

    # SEARCH

    search = request.GET.get(
        'search'
    )

    if search:

        employees = employees.filter(
            first_name__icontains=search
        )

    # DEPARTMENT FILTER

    department = request.GET.get(
        'department'
    )

    if department:

        employees = employees.filter(
            department_id=department
        )

    # DESIGNATION FILTER

    designation = request.GET.get(
        'designation'
    )

    if designation:

        employees = employees.filter(
            designation_id=designation
        )

    # STATUS FILTER

    status = request.GET.get(
        'status'
    )

    if status:

        employees = employees.filter(
            status=status
        )

    total_employees = (
        Employee.objects.count()
    )

    active_employees = (
        Employee.objects.filter(
            status='Active'
        ).count()
    )

    total_departments = (
        Department.objects.count()
    )

    new_joiners = (
        Employee.objects.order_by('-id')[:5].count()
    )

    departments = (
        Department.objects.all()
    )

    designations = (
        Designation.objects.all()
    )

    context = {

        'employees': employees,

        'total_employees':
        total_employees,

        'active_employees':
        active_employees,

        'total_departments':
        total_departments,

        'new_joiners':
        new_joiners,

        'departments':
        departments,

        'designations':
        designations,

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


# EMPLOYEE INFO

def employee_info(request, id):

    employee = Employee.objects.get(
        id=id
    )

    context = {

        'employee': employee

    }

    return render(

        request,
        'hrms/employee_info.html',
        context

    )
    # DEPARTMENT LIST

def department_list(request):

    departments = (
        Department.objects.all().order_by('-id')
    )

    context = {

        'departments': departments

    }

    return render(

        request,
        'hrms/department_list.html',
        context

    )


# ADD DEPARTMENT

def add_department(request):

    if request.method == "POST":

        Department.objects.create(

            department_code=request.POST.get(
                'department_code'
            ),

            department_name=request.POST.get(
                'department_name'
            ),

            description=request.POST.get(
                'description'
            ),

        )

        return redirect(
            '/hr/departments/'
        )

    return render(

        request,
        'hrms/add_department.html'

    )
    # DESIGNATION LIST

def designation_list(request):

    designations = (
        Designation.objects.all().order_by('-id')
    )

    context = {

        'designations': designations

    }

    return render(

        request,
        'hrms/designation_list.html',
        context

    )


# ADD DESIGNATION

def add_designation(request):

    if request.method == "POST":

        Designation.objects.create(

            designation_code=request.POST.get(
                'designation_code'
            ),

            designation_name=request.POST.get(
                'designation_name'
            ),

            description=request.POST.get(
                'description'
            ),

        )

        return redirect(
            '/hr/designations/'
        )

    return render(

        request,
        'hrms/add_designation.html'

    )
    # EDIT EMPLOYEE

def edit_employee(request, id):

    employee = Employee.objects.get(
        id=id
    )

    departments = (
        Department.objects.all()
    )

    designations = (
        Designation.objects.all()
    )

    if request.method == "POST":

        employee.employee_code = request.POST.get(
            'employee_code'
        )

        employee.first_name = request.POST.get(
            'first_name'
        )

        employee.last_name = request.POST.get(
            'last_name'
        )

        employee.email = request.POST.get(
            'email'
        )

        employee.personal_email = request.POST.get(
            'personal_email'
        )

        employee.mobile_no = request.POST.get(
            'mobile_no'
        )

        employee.personal_mobile = request.POST.get(
            'personal_mobile'
        )

        employee.employee_type = request.POST.get(
            'employee_type'
        )

        employee.ctc = request.POST.get(
            'ctc'
        )

        employee.notice_period = request.POST.get(
            'notice_period'
        )

        employee.reporting_manager = request.POST.get(
            'reporting_manager'
        )

        employee.department = Department.objects.get(
            id=request.POST.get(
                'department'
            )
        )

        employee.designation = Designation.objects.get(
            id=request.POST.get(
                'designation'
            )
        )

        employee.joining_date = request.POST.get(
            'joining_date'
        )

        employee.save()

        return redirect(
            f'/hr/employee-info/{employee.id}/'
        )

    context = {

        'employee': employee,

        'departments': departments,

        'designations': designations,

    }

    return render(

        request,
        'hrms/edit_employee.html',
        context

    )
    # EDIT EMPLOYEE

def edit_employee(request, id):

    employee = Employee.objects.get(
        id=id
    )

    departments = (
        Department.objects.all()
    )

    designations = (
        Designation.objects.all()
    )

    if request.method == "POST":

        employee.employee_code = request.POST.get(
            'employee_code'
        )

        employee.first_name = request.POST.get(
            'first_name'
        )

        employee.last_name = request.POST.get(
            'last_name'
        )

        employee.email = request.POST.get(
            'email'
        )

        employee.personal_email = request.POST.get(
            'personal_email'
        )

        employee.mobile_no = request.POST.get(
            'mobile_no'
        )

        employee.personal_mobile = request.POST.get(
            'personal_mobile'
        )

        employee.employee_type = request.POST.get(
            'employee_type'
        )

        employee.ctc = request.POST.get(
            'ctc'
        )

        employee.notice_period = request.POST.get(
            'notice_period'
        )

        employee.reporting_manager = request.POST.get(
            'reporting_manager'
        )

        employee.department = Department.objects.get(
            id=request.POST.get(
                'department'
            )
        )

        employee.designation = Designation.objects.get(
            id=request.POST.get(
                'designation'
            )
        )

        employee.joining_date = request.POST.get(
            'joining_date'
        )

        employee.save()

        return redirect(
            f'/hr/employee-info/{employee.id}/'
        )

    context = {

        'employee': employee,

        'departments': departments,

        'designations': designations,

    }

    return render(

        request,
        'hrms/edit_employee.html',
        context

    )
    # DELETE EMPLOYEE

def delete_employee(request, id):

    employee = Employee.objects.get(
        id=id
    )

    employee.delete()

    return redirect(
        '/hr/employees/'
    )