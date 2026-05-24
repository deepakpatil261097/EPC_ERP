from django.shortcuts import render

from .models import (
    Project,
    Material,
    StockTransaction
)


def dashboard(request):

    projects = Project.objects.all()
    materials = Material.objects.all()

    total_projects = projects.count()
    total_materials = materials.count()

    total_inventory_qty = 0

    summary_data = []

    selected_project = request.GET.get('project')

    for material in materials:

        if selected_project:

            project = Project.objects.get(id=selected_project)

            stock = StockTransaction.get_current_stock(
                project,
                material
            )

            if stock > 0:

                total_inventory_qty += stock

                summary_data.append({
                    'project': project.project_name,
                    'material': material.material_name,
                    'size': material.size,
                    'stock': stock,
                })

        else:

            stock_data = material.all_project_stock()

            total_stock = sum(stock_data.values())

            if total_stock > 0:

                total_inventory_qty += total_stock

                summary_data.append({
                    'project': 'All Projects',
                    'material': material.material_name,
                    'size': material.size,
                    'stock': total_stock,
                })

    context = {
        'projects': projects,
        'summary_data': summary_data,
        'total_projects': total_projects,
        'total_materials': total_materials,
        'total_inventory_qty': total_inventory_qty,
        'selected_project': selected_project,
    }

    return render(
        request,
        'inventory/dashboard.html',
        context
    )