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

    def total_stock(self, obj):
        transactions = StockTransaction.objects.filter(material=obj)

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

    def changelist_view(self, request, extra_context=None):

        html = """
        <h1>Project Stock Summary</h1>

        <table border="1" cellpadding="10">
            <tr>
                <th>Project</th>
                <th>Material</th>
                <th>Size</th>
                <th>Current Stock</th>
            </tr>
        """

        projects = Project.objects.all()
        materials = Material.objects.all()

        for project in projects:

            for material in materials:

                stock = StockTransaction.get_current_stock(
                    project,
                    material
                )

                if stock > 0:

                    html += f"""
                    <tr>
                        <td>{project.project_name}</td>
                        <td>{material.material_name}</td>
                        <td>{material.size}</td>
                        <td>{stock}</td>
                    </tr>
                    """

        html += "</table>"

        return HttpResponse(html)