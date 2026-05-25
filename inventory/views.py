from django.shortcuts import (
    render,
    redirect
)

from django.contrib.auth import (
    authenticate,
    login
)

from .models import (
    Project,
    Material,
    StockTransaction
)


# LOGIN PAGE

def login_page(request):

    error = ""

    if request.method == "POST":

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )

        user = authenticate(

            request,
            username=username,
            password=password

        )

        if user is not None:

            login(request, user)

            return redirect('/home/')

        else:

            error = (
                "Invalid Username or Password"
            )

    return render(

        request,
        'inventory/login.html',
        {'error': error}

    )


# HOME PAGE

def home(request):

    if not request.user.is_authenticated:
        return redirect('/')

    return render(

        request,
        'inventory/home.html'

    )


# MATERIALS PAGE

def materials_page(request):

    if not request.user.is_authenticated:
        return redirect('/')

    materials = Material.objects.all()

    for material in materials:

        stock_data = (
            material.all_project_stock()
        )

        material.total_stock = sum(
            stock_data.values()
        )

    context = {

        'materials': materials

    }

    return render(

        request,
        'inventory/materials.html',
        context

    )


# ADD MATERIAL

def add_material(request):

    if not request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":

        material_code = request.POST.get(
            'material_code'
        )

        material_name = request.POST.get(
            'material_name'
        )

        size = request.POST.get(
            'size'
        )

        unit = request.POST.get(
            'unit'
        )

        Material.objects.create(

            material_code=material_code,
            material_name=material_name,
            size=size,
            unit=unit

        )

        return redirect('/materials/')

    materials = Material.objects.all()

    for material in materials:

        stock_data = (
            material.all_project_stock()
        )

        material.total_stock = sum(
            stock_data.values()
        )

    context = {

        'materials': materials

    }

    return render(

        request,
        'inventory/add_material.html',
        context

    )


# TRANSACTIONS PAGE

def transactions_page(request):

    if not request.user.is_authenticated:
        return redirect('/')

    transactions = (
        StockTransaction.objects.all()
    )

    for transaction in transactions:

        transaction.current_stock = (

            StockTransaction.get_current_stock(

                transaction.project,
                transaction.material

            )

        )

    context = {

        'transactions': transactions

    }

    return render(

        request,
        'inventory/transactions.html',
        context

    )


# ADD TRANSACTION

def add_transaction(request):

    if not request.user.is_authenticated:
        return redirect('/')

    error = ""

    projects = Project.objects.all()

    materials = Material.objects.all()

    transactions = (
        StockTransaction.objects.all().order_by('-id')[:10]
    )

    if request.method == "POST":

        transaction_type = request.POST.get(
            'transaction_type'
        )

        project_id = request.POST.get(
            'project'
        )

        material_id = request.POST.get(
            'material'
        )

        quantity = float(
            request.POST.get(
                'quantity'
            )
        )

        project = Project.objects.get(
            id=project_id
        )

        material = Material.objects.get(
            id=material_id
        )

        current_stock = (
            StockTransaction.get_current_stock(
                project,
                material
            )
        )

        if (
            transaction_type == "OUT"
            and
            quantity > current_stock
        ):

            error = (
                f"Available Stock is "
                f"{current_stock}"
            )

        else:

            StockTransaction.objects.create(

                project=project,
                material=material,
                transaction_type=transaction_type,
                quantity=quantity

            )

            return redirect(
                '/transactions/'
            )

    context = {

        'projects': projects,
        'materials': materials,
        'transactions': transactions,
        'error': error,

    }

    return render(

        request,
        'inventory/add_transaction.html',
        context

    )


# PROJECTS PAGE

def projects_page(request):

    if not request.user.is_authenticated:
        return redirect('/')

    projects = Project.objects.all()

    context = {

        'projects': projects

    }

    return render(

        request,
        'inventory/projects.html',
        context

    )


# ADD PROJECT

def add_project(request):

    if not request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":

        project_code = request.POST.get(
            'project_code'
        )

        project_name = request.POST.get(
            'project_name'
        )

        location = request.POST.get(
            'location'
        )

        Project.objects.create(

            project_code=project_code,
            project_name=project_name,
            location=location

        )

        return redirect('/projects/')

    return render(

        request,
        'inventory/add_project.html'

    )


# STOCK SUMMARY

def summary_page(request):

    if not request.user.is_authenticated:
        return redirect('/')

    projects = Project.objects.all()

    materials = Material.objects.all()

    total_materials = 0

    total_inventory_qty = 0

    summary_data = []

    selected_project = request.GET.get(
        'project'
    )

    search = request.GET.get(
        'search'
    )

    for material in materials:

        if selected_project:

            project = Project.objects.get(
                id=selected_project
            )

            stock = (
                StockTransaction.get_current_stock(
                    project,
                    material
                )
            )

            if stock > 0:

                if search:

                    if (
                        search.lower()
                        not in material.material_code.lower()

                        and

                        search.lower()
                        not in material.material_name.lower()
                    ):

                        continue

                total_materials += 1

                total_inventory_qty += stock

                summary_data.append({

                    'project':
                    project.project_name,

                    'material_code':
                    material.material_code,

                    'material':
                    material.material_name,

                    'size':
                    material.size,

                    'stock':
                    stock,

                    'unit':
                    material.unit,

                })

        else:

            stock_data = (
                material.all_project_stock()
            )

            for project_name, stock in stock_data.items():

                if search:

                    if (
                        search.lower()
                        not in material.material_code.lower()

                        and

                        search.lower()
                        not in material.material_name.lower()
                    ):

                        continue

                total_materials += 1

                total_inventory_qty += stock

                summary_data.append({

                    'project':
                    project_name,

                    'material_code':
                    material.material_code,

                    'material':
                    material.material_name,

                    'size':
                    material.size,

                    'stock':
                    stock,

                    'unit':
                    material.unit,

                })

    context = {

        'projects': projects,

        'summary_data':
        summary_data,

        'total_materials':
        total_materials,

        'total_inventory_qty':
        total_inventory_qty,

        'selected_project':
        selected_project,

        'search':
        search,

    }

    return render(

        request,
        'inventory/summary.html',
        context

    )