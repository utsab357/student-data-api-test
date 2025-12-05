from django.db import models
from datetime import date


class Student(models.Model):
    DEPT_CSE = 'CSE'
    DEPT_ECE = 'ECE'
    DEPT_ME = 'ME'
    DEPT_IT = 'IT'
    DEPARTMENTS = [
        (DEPT_CSE, 'CSE'),
        (DEPT_ECE, 'ECE'),
        (DEPT_ME, 'ME'),
        (DEPT_IT, 'IT'),
    ]

    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_INACTIVE, 'Inactive'),
    ]

    name = models.CharField(max_length=200)
    roll_number = models.CharField(max_length=50, unique=True)
    address = models.TextField(blank=True)
    department = models.CharField(max_length=50, choices=DEPARTMENTS)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    enrollment_date = models.DateField(default=date.today)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.roll_number} - {self.name}"


class Invoice(models.Model):
    student = models.ForeignKey(Student, related_name='invoices', on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=150, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-issued_at']

    def __str__(self):
        return f"{self.invoice_number} ({self.student.roll_number})"
