from django.contrib import admin
from django.http import HttpResponse

from .models import (
    Project,
    Material,
    StockTransaction,
    ProjectStockSummary
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'project_code',
        'project_name',
        'location',
    )


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        'material_code',
        'material_name',
        'size',
        'unit',
        'total_stock',
        'site_wise_stock',
    )

    search_fields = (
        'material_name',
        'material_code',
        'size',
    )

    def total_stock(self, obj):

        transactions = StockTransaction.objects.filter(
            material=obj
        )

        total_in = sum(
            t.quantity for t in transactions
            if t.transaction_type == 'IN'
        )

        total_out = sum(
            t.quantity for t in transactions
            if t.transaction_type == 'OUT'
        )

        return total_in - total_out

    total_stock.short_description = 'Total Stock'

    def site_wise_stock(self, obj):

        stock_data = obj.all_project_stock()

        return ", ".join(
            f"{project}: {qty}"
            for project, qty in stock_data.items()
        )

    site_wise_stock.short_description = 'Site-wise Stock'


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):

    list_display = (
        'project',
        'material',
        'transaction_type',
        'quantity',
        'current_stock',
    )

    list_filter = (
        'project',
        'material',
        'transaction_type',
    )

    search_fields = (
        'project__project_name',
        'material__material_name',
    )

    def current_stock(self, obj):

        return StockTransaction.get_current_stock(
            obj.project,
            obj.material
        )

    current_stock.short_description = 'Current Stock'


@admin.register(ProjectStockSummary)
class ProjectStockSummaryAdmin(admin.ModelAdmin):

    change_list_template = None

    def changelist_view(self, request, extra_context=None):

        selected_project = request.GET.get('project')

        projects = Project.objects.all()

        html = """

        <html>

        <head>

        <title>Project Stock Summary</title>

        <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet"
        >

        </head>

        <body style="background-color:#f5f7fa;">

        <div class="container mt-4">

        <h1 class="mb-4">
        Project Stock Summary
        </h1>

        <form method="GET" class="mb-4">

        <div class="row">

        <div class="col-md-4">

        <select
        name="project"
        class="form-select"
        onchange="this.form.submit()"
        >

        <option value="">
        All Projects
        </option>

        """

        for project in projects:

            selected = ""

            if selected_project == str(project.id):
                selected = "selected"

            html += f"""

            <option
            value="{project.id}"
            {selected}
            >
            {project.project_name}
            </option>

            """

        html += """

        </select>

        </div>

        </div>

        </form>

        <div class="card shadow-sm">

        <div class="card-body">

        <table class="table table-bordered table-hover">

        <thead class="table-dark">

        <tr>

        <th>Project</th>
        <th>Material</th>
        <th>Size</th>
        <th>Current Stock</th>

        </tr>

        </thead>

        <tbody>

        """

        total_stock = 0
        total_materials = 0

        materials = Material.objects.all()

        for material in materials:

            if selected_project:

                project = Project.objects.get(
                    id=selected_project
                )

                stock = StockTransaction.get_current_stock(
                    project,
                    material
                )

                if stock > 0:

                    total_stock += stock
                    total_materials += 1

                    html += f"""

                    <tr>

                    <td>{project.project_name}</td>
                    <td>{material.material_name}</td>
                    <td>{material.size}</td>
                    <td>{stock}</td>

                    </tr>

                    """

            else:

                stock_data = material.all_project_stock()

                for project_name, stock in stock_data.items():

                    total_stock += stock
                    total_materials += 1

                    html += f"""

                    <tr>

                    <td>{project_name}</td>
                    <td>{material.material_name}</td>
                    <td>{material.size}</td>
                    <td>{stock}</td>

                    </tr>

                    """

        html += f"""

        </tbody>

        </table>

        </div>

        </div>

        <div class="row mt-4">

        <div class="col-md-6">

        <div class="card shadow-sm">

        <div class="card-body">

        <h5>Total Materials</h5>

        <h2>{total_materials}</h2>

        </div>

        </div>

        </div>

        <div class="col-md-6">

        <div class="card shadow-sm">

        <div class="card-body">

        <h5>Total Inventory Qty</h5>

        <h2>{total_stock}</h2>

        </div>

        </div>

        </div>

        </div>

        </div>

        </body>

        </html>

        """

        return HttpResponse(html)