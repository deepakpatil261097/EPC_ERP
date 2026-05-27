import pandas as pd

from django.shortcuts import (
    render,
    redirect
)

from django.contrib.auth import (
    authenticate,
    login
)

from django.http import (
    HttpResponse
)

from .models import (
    Project,
    Material,
    MaterialTransfer,
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

    total_projects = (
        Project.objects.count()
    )

    total_materials = (
        Material.objects.count()
    )

    total_transactions = (
        StockTransaction.objects.count()
    )

    total_in = (
        StockTransaction.objects.filter(
            transaction_type='IN'
        ).count()
    )

    total_out = (
        StockTransaction.objects.filter(
            transaction_type='OUT'
        ).count()
    )

    low_stock_count = 0

    materials = Material.objects.all()

    for material in materials:

        stock_data = (
            material.all_project_stock()
        )

        total_stock = sum(
            stock_data.values()
        )

        if total_stock <= material.min_stock:

            low_stock_count += 1

    context = {

        'total_projects':
        total_projects,

        'total_materials':
        total_materials,

        'total_transactions':
        total_transactions,

        'low_stock_count':
        low_stock_count,

        'total_in':
        total_in,

        'total_out':
        total_out,

    }

    return render(

        request,
        'inventory/home.html',
        context

    )


# INVENTORY DASHBOARD

def inventory_dashboard(request):

    if not request.user.is_authenticated:
        return redirect('/')

    total_materials = (
        Material.objects.count()
    )

    total_transactions = (
        StockTransaction.objects.count()
    )

    total_transfers = (
        MaterialTransfer.objects.count()
    )

    low_stock_count = 0

    materials = Material.objects.all()

    for material in materials:

        stock_data = (
            material.all_project_stock()
        )

        total_stock = sum(
            stock_data.values()
        )

        if total_stock <= material.min_stock:

            low_stock_count += 1

    context = {

        'total_materials':
        total_materials,

        'total_transactions':
        total_transactions,

        'total_transfers':
        total_transfers,

        'low_stock_count':
        low_stock_count,

    }

    return render(

        request,
        'inventory/inventory_dashboard.html',
        context

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


# EXPORT MATERIALS EXCEL

def export_materials_excel(request):

    if not request.user.is_authenticated:
        return redirect('/')

    materials = Material.objects.all()

    data = []

    for material in materials:

        stock_data = (
            material.all_project_stock()
        )

        total_stock = sum(
            stock_data.values()
        )

        data.append({

            'Material Code':
            material.material_code,

            'Material Name':
            material.material_name,

            'Category':
            material.category,

            'Size':
            material.size,

            'Unit':
            material.unit,

            'Min Stock':
            material.min_stock,

            'Total Stock':
            total_stock,

        })

    df = pd.DataFrame(data)

    response = HttpResponse(

        content_type=
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; filename=materials.xlsx'
    )

    df.to_excel(

        response,
        index=False

    )

    return response


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

        category = request.POST.get(
            'category'
        )

        size = request.POST.get(
            'size'
        )

        unit = request.POST.get(
            'unit'
        )

        min_stock = request.POST.get(
            'min_stock'
        )

        Material.objects.create(

            material_code=material_code,

            material_name=material_name,

            category=category,

            size=size,

            unit=unit,

            min_stock=min_stock

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


# UPLOAD MATERIALS EXCEL

def upload_materials(request):

    if not request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":

        excel_file = request.FILES[
            'excel_file'
        ]

        df = pd.read_excel(
            excel_file
        )

        for index, row in df.iterrows():

            Material.objects.create(

                material_code=row[
                    'material_code'
                ],

                material_name=row[
                    'material_name'
                ],

                category=row[
                    'category'
                ],

                size=row[
                    'size'
                ],

                unit=row[
                    'unit'
                ],

                min_stock=row[
                    'min_stock'
                ]

            )

        return redirect(
            '/materials/'
        )

    return render(

        request,
        'inventory/upload_materials.html'

    )


# MATERIAL TRANSFER

def transfer_material(request):

    if not request.user.is_authenticated:
        return redirect('/')

    error = ""

    projects = Project.objects.all()

    materials = Material.objects.all()

    if request.method == "POST":

        from_project_id = request.POST.get(
            'from_project'
        )

        to_project_id = request.POST.get(
            'to_project'
        )

        material_id = request.POST.get(
            'material'
        )

        quantity = float(
            request.POST.get(
                'quantity'
            )
        )

        from_project = Project.objects.get(
            id=from_project_id
        )

        to_project = Project.objects.get(
            id=to_project_id
        )

        material = Material.objects.get(
            id=material_id
        )

        current_stock = (
            StockTransaction.get_current_stock(
                from_project,
                material
            )
        )

        if quantity > current_stock:

            error = (
                f"Available Stock is "
                f"{current_stock}"
            )

        else:

            StockTransaction.objects.create(

                project=from_project,

                material=material,

                transaction_type='OUT',

                quantity=quantity

            )

            StockTransaction.objects.create(

                project=to_project,

                material=material,

                transaction_type='IN',

                quantity=quantity

            )

            MaterialTransfer.objects.create(

                from_project=from_project,

                to_project=to_project,

                material=material,

                quantity=quantity

            )

            return redirect(
                '/summary/'
            )

    context = {

        'projects': projects,

        'materials': materials,

        'error': error,

    }

    return render(

        request,
        'inventory/transfer_material.html',
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

                    'category':
                    material.category,

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

                    'category':
                    material.category,

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
    # INVENTORY ANALYTICS

def inventory_analytics(request):

    if not request.user.is_authenticated:
        return redirect('/')

    total_in = (
        StockTransaction.objects.filter(
            transaction_type='IN'
        ).count()
    )

    total_out = (
        StockTransaction.objects.filter(
            transaction_type='OUT'
        ).count()
    )

    total_materials = (
        Material.objects.count()
    )

    low_stock_count = 0

    materials = Material.objects.all()

    for material in materials:

        stock_data = (
            material.all_project_stock()
        )

        total_stock = sum(
            stock_data.values()
        )

        if total_stock <= material.min_stock:

            low_stock_count += 1

    category_data = []

    categories = (
        Material.objects.values_list(
            'category',
            flat=True
        ).distinct()
    )

    for category in categories:

        count = (
            Material.objects.filter(
                category=category
            ).count()
        )

        category_data.append({

            'category': category,
            'count': count

        })

    context = {

        'total_in':
        total_in,

        'total_out':
        total_out,

        'total_materials':
        total_materials,

        'low_stock_count':
        low_stock_count,

        'category_data':
        category_data,

    }

    return render(

        request,
        'inventory/inventory_analytics.html',
        context

    )