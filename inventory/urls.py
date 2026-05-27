from django.urls import path

from .views import (

    login_page,
    home,

    inventory_dashboard,

    materials_page,
    add_material,
    upload_materials,
    export_materials_excel,

    transactions_page,
    add_transaction,

    transfer_material,

    summary_page,

    projects_page,
    add_project,

)

urlpatterns = [

    # LOGIN

    path(
        '',
        login_page
    ),

    # HOME

    path(
        'home/',
        home
    ),

    # INVENTORY DASHBOARD

    path(
        'inventory-dashboard/',
        inventory_dashboard
    ),

    # MATERIALS

    path(
        'materials/',
        materials_page
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
        'export-materials-excel/',
        export_materials_excel
    ),

    # TRANSACTIONS

    path(
        'transactions/',
        transactions_page
    ),

    path(
        'add-transaction/',
        add_transaction
    ),

    # TRANSFER

    path(
        'transfer-material/',
        transfer_material
    ),

    # SUMMARY

    path(
        'summary/',
        summary_page
    ),

    # PROJECTS

    path(
        'projects/',
        projects_page
    ),

    path(
        'add-project/',
        add_project
    ),

]