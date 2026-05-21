from django.contrib import admin
from .models import Project, Material, StockTransaction

admin.site.register(Project)
admin.site.register(Material)
admin.site.register(StockTransaction)