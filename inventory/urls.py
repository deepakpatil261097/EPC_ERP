from django.urls import path

from .views import (

    login_page,

    home,

    inventory_dashboard,

    materials_page,

    add_material,

    upload_materials,

    export_materials_excel,

    transfer_material,

    transactions_page,

    add_transaction,

    projects_page,

    add_project,

    summary_page,

    inventory_analytics

)

urlpatterns = [

    # LOGIN

    path(

        '',

        login_page,

        name='login'

    ),

    # HOME

    path(

        'home/',

        home,

        name='home'

    ),

    # INVENTORY DASHBOARD

    path(

        'inventory-dashboard/',

        inventory_dashboard,

        name='inventory_dashboard'

    ),

    # MATERIALS

    path(

        'materials/',

        materials_page,

        name='materials'

    ),

    # ADD MATERIAL

    path(

        'add-material/',

        add_material,

        name='add_material'

    ),

    # UPLOAD MATERIALS

    path(

        'upload-materials/',

        upload_materials,

        name='upload_materials'

    ),

    # EXPORT MATERIALS

    path(

        'export-materials-excel/',

        export_materials_excel,

        name='export_materials_excel'

    ),

    # STOCK MOVEMENTS

    path(

        'transactions/',

        transactions_page,

        name='transactions'

    ),

    # ADD TRANSACTION

    path(

        'add-transaction/',

        add_transaction,

        name='add_transaction'

    ),

    # MATERIAL TRANSFER

    path(

        'transfer-material/',

        transfer_material,

        name='transfer_material'

    ),

    # PROJECTS

    path(

        'projects/',

        projects_page,

        name='projects'

    ),

    # ADD PROJECT

    path(

        'add-project/',

        add_project,

        name='add_project'

    ),

    # SUMMARY

    path(

        'summary/',

        summary_page,

        name='summary'

    ),

    # INVENTORY ANALYTICS

    path(

        'inventory-analytics/',

        inventory_analytics,

        name='inventory_analytics'

    ),

]