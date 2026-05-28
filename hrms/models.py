from django.db import models


# DEPARTMENT MASTER

class Department(models.Model):

    STATUS_CHOICES = [

        ('Active', 'Active'),

        ('Inactive', 'Inactive')

    ]

    department_code = models.CharField(

        max_length=50,

        unique=True

    )

    department_name = models.CharField(

        max_length=255

    )

    description = models.TextField(

        blank=True,

        null=True

    )

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='Active'

    )

    created_date = models.DateTimeField(

        auto_now_add=True

    )

    def __str__(self):

        return f"{self.department_code} - {self.department_name}"


# DESIGNATION MASTER

class Designation(models.Model):

    STATUS_CHOICES = [

        ('Active', 'Active'),

        ('Inactive', 'Inactive')

    ]

    designation_code = models.CharField(

        max_length=50,

        unique=True

    )

    designation_name = models.CharField(

        max_length=255

    )

    description = models.TextField(

        blank=True,

        null=True

    )

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='Active'

    )

    created_date = models.DateTimeField(

        auto_now_add=True

    )

    def __str__(self):

        return f"{self.designation_code} - {self.designation_name}"


# EMPLOYEE MASTER

class Employee(models.Model):

    STATUS_CHOICES = [

        ('Active', 'Active'),

        ('Inactive', 'Inactive'),

        ('Resigned', 'Resigned')

    ]

    employee_code = models.CharField(

        max_length=50,

        unique=True

    )

    first_name = models.CharField(

        max_length=255

    )

    last_name = models.CharField(

        max_length=255,

        blank=True,

        null=True

    )

    email = models.EmailField(

        blank=True,

        null=True

    )

    personal_email = models.EmailField(

        blank=True,

        null=True

    )

    mobile_no = models.CharField(

        max_length=20,

        blank=True,

        null=True

    )

    personal_mobile = models.CharField(

        max_length=20,

        blank=True,

        null=True

    )

    employee_type = models.CharField(

        max_length=50,

        blank=True,

        null=True

    )

    ctc = models.DecimalField(

        max_digits=12,

        decimal_places=2,

        blank=True,

        null=True

    )

    notice_period = models.CharField(

        max_length=100,

        blank=True,

        null=True

    )

    reporting_manager = models.CharField(

        max_length=255,

        blank=True,

        null=True

    )

    department = models.ForeignKey(

        Department,

        on_delete=models.SET_NULL,

        blank=True,

        null=True

    )

    designation = models.ForeignKey(

        Designation,

        on_delete=models.SET_NULL,

        blank=True,

        null=True

    )

    joining_date = models.DateField(

        blank=True,

        null=True

    )

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='Active'

    )

    created_date = models.DateTimeField(

        auto_now_add=True

    )

    def __str__(self):

        return f"{self.employee_code} - {self.first_name}"