from django.db import models


# PROJECT MODEL

class Project(models.Model):

    project_code = models.CharField(
        max_length=50
    )

    project_name = models.CharField(
        max_length=100
    )

    location = models.CharField(
        max_length=100
    )

    def __str__(self):

        return self.project_name


# MATERIAL MODEL

class Material(models.Model):

    CATEGORY_CHOICES = (

        ('Pipe', 'Pipe'),

        ('Valve', 'Valve'),

        ('Fitting', 'Fitting'),

        ('Instrument', 'Instrument'),

        ('Electrical', 'Electrical'),

        ('Consumable', 'Consumable'),

    )

    material_name = models.CharField(
        max_length=100
    )

    material_code = models.CharField(
        max_length=50
    )

    category = models.CharField(

        max_length=50,

        choices=CATEGORY_CHOICES,

        default='Pipe'

    )

    size = models.CharField(
        max_length=50
    )

    unit = models.CharField(
        max_length=20
    )

    min_stock = models.FloatField(
        default=0
    )

    def __str__(self):

        return (
            f"{self.material_name}"
            f" - "
            f"{self.size}"
        )

    def current_stock(self, project):

        return StockTransaction.get_current_stock(
            project,
            self
        )

    def all_project_stock(self):

        projects = Project.objects.all()

        stock_data = {}

        for project in projects:

            stock = (
                StockTransaction.get_current_stock(
                    project,
                    self
                )
            )

            if stock > 0:

                stock_data[
                    project.project_name
                ] = stock

        return stock_data


# PROJECT STOCK SUMMARY

class ProjectStockSummary(models.Model):

    class Meta:

        managed = False

        verbose_name = (
            "Project Stock Summary"
        )

        verbose_name_plural = (
            "Project Stock Summary"
        )


# STOCK TRANSACTION

class StockTransaction(models.Model):

    TRANSACTION_TYPES = (

        ('IN', 'IN'),

        ('OUT', 'OUT'),

    )

    project = models.ForeignKey(

        Project,

        on_delete=models.CASCADE

    )

    material = models.ForeignKey(

        Material,

        on_delete=models.CASCADE

    )

    transaction_type = models.CharField(

        max_length=10,

        choices=TRANSACTION_TYPES

    )

    quantity = models.FloatField()

    def __str__(self):

        return (
            f"{self.project}"
            f" - "
            f"{self.material}"
        )

    @staticmethod
    def get_current_stock(

        project,
        material

    ):

        transactions = (
            StockTransaction.objects.filter(

                project=project,
                material=material

            )
        )

        total_in = sum(

            t.quantity
            for t in transactions

            if t.transaction_type == 'IN'

        )

        total_out = sum(

            t.quantity
            for t in transactions

            if t.transaction_type == 'OUT'

        )

        return total_in - total_out