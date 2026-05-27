from django.db import models


# PROJECT MODEL

class Project(models.Model):

    project_code = models.CharField(
        max_length=100
    )

    project_name = models.CharField(
        max_length=255
    )

    location = models.CharField(
        max_length=255
    )

    created_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.project_code


# MATERIAL MODEL

class Material(models.Model):

    STATUS_CHOICES = [

        ('Active', 'Active'),

        ('Inactive', 'Inactive')

    ]

    material_code = models.CharField(
        max_length=100
    )

    material_name = models.CharField(
        max_length=255
    )

    category = models.CharField(
        max_length=100
    )

    size = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    unit = models.CharField(
        max_length=50
    )

    min_stock = models.FloatField(
        default=0
    )

    created_date = models.DateTimeField(
        auto_now_add=True
    )

    updated_date = models.DateTimeField(
        auto_now=True
    )

    created_by = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='Active'

    )

    remarks = models.TextField(

        blank=True,

        null=True

    )

    def __str__(self):

        return (

            f"{self.material_code}"
            f" - "
            f"{self.material_name}"

        )

    # ALL PROJECT STOCK

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
                    project.project_code
                ] = stock

        return stock_data


# STOCK TRANSACTION MODEL

class StockTransaction(models.Model):

    TRANSACTION_TYPES = [

        ('GRN', 'GRN'),

        ('IN', 'IN'),

        ('OUT', 'OUT')

    ]

    STATUS_CHOICES = [

        ('Draft', 'Draft'),

        ('Pending', 'Pending'),

        ('Approved', 'Approved'),

        ('Rejected', 'Rejected')

    ]

    QC_STATUS_CHOICES = [

        ('Pending', 'Pending'),

        ('Approved', 'Approved'),

        ('Rejected', 'Rejected'),

        ('Partial', 'Partial')

    ]

    project = models.ForeignKey(

        Project,

        on_delete=models.CASCADE

    )

    material = models.ForeignKey(

        Material,

        on_delete=models.CASCADE

    )

    transaction_type = models.CharField(

        max_length=20,

        choices=TRANSACTION_TYPES

    )

    quantity = models.FloatField()

    transaction_no = models.CharField(

        max_length=50,

        unique=True,

        blank=True,

        null=True

    )

    transaction_date = models.DateTimeField(

        auto_now_add=True

    )

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='Pending'

    )

    created_by = models.CharField(

        max_length=100,

        blank=True,

        null=True

    )

    approved_by = models.CharField(

        max_length=100,

        blank=True,

        null=True

    )

    remarks = models.TextField(

        blank=True,

        null=True

    )

    # GRN / QC DETAILS

    grn_no = models.CharField(

        max_length=100,

        blank=True,

        null=True

    )

    vendor_name = models.CharField(

        max_length=255,

        blank=True,

        null=True

    )

    invoice_no = models.CharField(

        max_length=100,

        blank=True,

        null=True

    )

    received_qty = models.FloatField(

        default=0

    )

    approved_qty = models.FloatField(

        default=0

    )

    rejected_qty = models.FloatField(

        default=0

    )

    hold_qty = models.FloatField(

        default=0

    )

    qc_status = models.CharField(

        max_length=20,

        choices=QC_STATUS_CHOICES,

        default='Pending'

    )

    qc_done_by = models.CharField(

        max_length=100,

        blank=True,

        null=True

    )

    qc_date = models.DateTimeField(

        blank=True,

        null=True

    )

    def save(self, *args, **kwargs):

        if not self.transaction_no:

            last_id = (

                StockTransaction.objects.count()
                + 1

            )

            # GRN

            if self.transaction_type == 'GRN':

                self.transaction_no = (

                    f"GRN{last_id:05d}"

                )

            # MATERIAL ISSUE

            elif self.transaction_type == 'OUT':

                self.transaction_no = (

                    f"MIV{last_id:05d}"

                )

            # INTERNAL MATERIAL IN

            elif self.transaction_type == 'IN':

                self.transaction_no = (

                    f"MIN{last_id:05d}"

                )

            else:

                self.transaction_no = (

                    f"TXN{last_id:05d}"

                )

        super().save(*args, **kwargs)

    def __str__(self):

        return (

            f"{self.transaction_no} | "
            f"{self.transaction_type} | "
            f"{self.material.material_code}"

        )

    @staticmethod

    def get_current_stock(

        project,
        material

    ):

        total_in = (

            StockTransaction.objects.filter(

                project=project,

                material=material,

                status='Approved'

            ).aggregate(

                models.Sum('approved_qty')

            )['approved_qty__sum']

            or 0

        )

        total_out = (

            StockTransaction.objects.filter(

                project=project,

                material=material,

                transaction_type='OUT',

                status='Approved'

            ).aggregate(

                models.Sum('quantity')

            )['quantity__sum']

            or 0

        )

        return total_in - total_out


# MATERIAL TRANSFER MODEL

class MaterialTransfer(models.Model):

    from_project = models.ForeignKey(

        Project,

        on_delete=models.CASCADE,

        related_name='from_project'

    )

    to_project = models.ForeignKey(

        Project,

        on_delete=models.CASCADE,

        related_name='to_project'

    )

    material = models.ForeignKey(

        Material,

        on_delete=models.CASCADE

    )

    quantity = models.FloatField()

    transfer_date = models.DateTimeField(

        auto_now_add=True

    )

    transfer_no = models.CharField(

        max_length=50,

        unique=True,

        blank=True,

        null=True

    )

    approved_by = models.CharField(

        max_length=100,

        blank=True,

        null=True

    )

    remarks = models.TextField(

        blank=True,

        null=True

    )

    def save(self, *args, **kwargs):

        if not self.transfer_no:

            last_id = (

                MaterialTransfer.objects.count()
                + 1

            )

            self.transfer_no = (

                f"TRF{last_id:05d}"

            )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.transfer_no