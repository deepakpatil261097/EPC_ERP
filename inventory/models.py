from django.db import models


class Project(models.Model):
    project_code = models.CharField(max_length=50)
    project_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.project_name


class Material(models.Model):
    material_name = models.CharField(max_length=100)
    material_code = models.CharField(max_length=50)
    unit = models.CharField(max_length=20)

    def __str__(self):
        return self.material_name


class StockTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('IN', 'IN'),
        ('OUT', 'OUT'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.project} - {self.material}"

    @staticmethod
    def get_current_stock(project, material):
        transactions = StockTransaction.objects.filter(
            project=project,
            material=material
        )

        total_in = sum(
            t.quantity for t in transactions if t.transaction_type == 'IN'
        )

        total_out = sum(
            t.quantity for t in transactions if t.transaction_type == 'OUT'
        )

        return total_in - total_out