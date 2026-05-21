from django.contrib import admin
from .models import Project, Material, StockTransaction


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_code', 'project_name', 'location')


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        'material_code',
        'material_name',
        'unit',
    )


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