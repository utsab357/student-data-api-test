import csv
from io import StringIO
from decimal import Decimal
import random
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Student, Invoice
from .serializers import StudentSerializer, InvoiceSerializer
from django.db.models import Sum


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['department', 'roll_number', 'status']
    search_fields = ['name', 'roll_number', 'email', 'phone']
    ordering_fields = ['created_at', 'enrollment_date', 'name']

    @action(detail=True, methods=['get'])
    def export_invoices(self, request, pk=None):
        student = self.get_object()
        invoices = student.invoices.all()
        sio = StringIO()
        writer = csv.writer(sio)
        writer.writerow(['invoice_number', 'amount', 'paid', 'issued_at'])
        for inv in invoices:
            writer.writerow([inv.invoice_number, f"{inv.amount}", inv.paid, inv.issued_at])
        resp = HttpResponse(sio.getvalue(), content_type='text/csv')
        resp['Content-Disposition'] = f'attachment; filename="{student.roll_number}_invoices.csv"'
        return resp

    @action(detail=False, methods=['get'])
    def summary(self, request):
        dept = request.query_params.get('department')
        students_qs = Student.objects.all()
        if dept:
            students_qs = students_qs.filter(department=dept)
        total_students = students_qs.count()
        counts = {}
        for code, _ in Student.DEPARTMENTS:
            counts[code] = students_qs.filter(department=code).count()
        unpaid = Invoice.objects.filter(student__in=students_qs, paid=False).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        data = {
            'total_students': total_students,
            'count_per_department': counts,
            'total_unpaid_invoice_amount': f"{unpaid}",
        }
        return Response(data)

    @action(detail=False, methods=['get'])
    def export(self, request):
        dept = request.query_params.get('department')
        qs = Student.objects.all()
        if dept:
            qs = qs.filter(department=dept)
        sio = StringIO()
        writer = csv.writer(sio)
        writer.writerow(['roll_number', 'name', 'department', 'email', 'phone', 'enrollment_date', 'status'])
        for s in qs:
            writer.writerow([s.roll_number, s.name, s.department, s.email or '', s.phone, s.enrollment_date, s.status])
        resp = HttpResponse(sio.getvalue(), content_type='text/csv')
        resp['Content-Disposition'] = 'attachment; filename="students_export.csv"'
        return resp


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.select_related('student').all()
    serializer_class = InvoiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['paid', 'student__roll_number']
    search_fields = ['invoice_number', 'student__name', 'student__roll_number']
    ordering_fields = ['issued_at', 'amount']
