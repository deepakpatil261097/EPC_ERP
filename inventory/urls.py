from django.urls import path

from .views import (

    login_page,

    home,

    inventory_dashboard,

    materials_page,

    export_materials_excel,

    add_material,

    upload_materials,

    transfer_material,

    transactions_page,

    add_transaction,

    approve_transaction,

    reject_transaction,

    qc_pending_page,

    qc_approve_page,

    projects_page,

    add_project,

    summary_page,

    inventory_analytics

)

urlpatterns = [

    path(
        '',
        login_page
    ),

    path(
        'home/',
        home
    ),

    path(
        'inventory-dashboard/',
        inventory_dashboard
    ),

    path(
        'materials/',
        materials_page
    ),

    path(
        'export-materials-excel/',
        export_materials_excel
    ),

    path(
        'add-material/',
        add_material
    ),

    path(
        'upload-materials/',
        upload_materials
    ),

    path(
        'transfer-material/',
        transfer_material
    ),

    path(
        'transactions/',
        transactions_page
    ),

    path(
        'add-transaction/',
        add_transaction
    ),

    path(
        'approve-transaction/<int:id>/',
        approve_transaction
    ),

    path(
        'reject-transaction/<int:id>/',
        reject_transaction
    ),

    path(
        'qc-pending/',
        qc_pending_page
    ),

    path(
        'qc-approve/<int:id>/',
        qc_approve_page
    ),

    path(
        'projects/',
        projects_page
    ),

    path(
        'add-project/',
        add_project
    ),

    path(
        'summary/',
        summary_page
    ),

    path(
        'inventory-analytics/',
        inventory_analytics
    ),

]