from django.contrib import admin
from .models import Student, Invoice


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'roll_number', 'name', 'department', 'status')
    search_fields = ('name', 'roll_number', 'email', 'phone')
    list_filter = ('department', 'status')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice_number', 'student', 'amount', 'paid', 'issued_at')
    search_fields = ('invoice_number', 'student__roll_number')
    list_filter = ('paid',)
