from django.contrib import admin

from .models import (

    Project,

    Material,

    StockTransaction,

    MaterialTransfer

)


# PROJECT ADMIN

@admin.register(Project)

class ProjectAdmin(admin.ModelAdmin):

    list_display = (

        'project_code',

        'project_name',

        'location',

        'created_date'

    )

    search_fields = (

        'project_code',

        'project_name'

    )


# MATERIAL ADMIN

@admin.register(Material)

class MaterialAdmin(admin.ModelAdmin):

    list_display = (

        'material_code',

        'material_name',

        'category',

        'size',

        'unit',

        'min_stock',

        'status'

    )

    search_fields = (

        'material_code',

        'material_name',

        'category'

    )

    list_filter = (

        'category',

        'status'

    )


# STOCK TRANSACTION ADMIN

@admin.register(StockTransaction)

class StockTransactionAdmin(admin.ModelAdmin):

    list_display = (

        'transaction_no',

        'project',

        'material',

        'transaction_type',

        'quantity',

        'status',

        'created_by',

        'approved_by',

        'transaction_date'

    )

    search_fields = (

        'transaction_no',

        'material__material_code',

        'material__material_name'

    )

    list_filter = (

        'transaction_type',

        'status',

        'transaction_date'

    )


# MATERIAL TRANSFER ADMIN

@admin.register(MaterialTransfer)

class MaterialTransferAdmin(admin.ModelAdmin):

    list_display = (

        'transfer_no',

        'from_project',

        'to_project',

        'material',

        'quantity',

        'approved_by',

        'transfer_date'

    )

    search_fields = (

        'transfer_no',

        'material__material_code'

    )

    list_filter = (

        'transfer_date',

    )