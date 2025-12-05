from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Student, Invoice
from decimal import Decimal

class StudentAPITests(APITestCase):
    def setUp(self):
        s1 = Student.objects.create(name='Alice', roll_number='R0001', department='CSE', phone='1234567890')
        s2 = Student.objects.create(name='Bob', roll_number='R0002', department='ECE', phone='2345678901')
        Invoice.objects.create(student=s1, invoice_number='INV-R0001-1', amount=Decimal('1500.00'), paid=False)
        Invoice.objects.create(student=s1, invoice_number='INV-R0001-2', amount=Decimal('2500.00'), paid=True)

    def test_list_students(self):
        url = reverse('student-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('results', data)

    def test_filter_by_department(self):
        url = reverse('student-list') + '?department=CSE'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['results'][0]['department'], 'CSE')

    def test_csv_export(self):
        url = reverse('student-export')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'text/csv')
        content = resp.content.decode()
        self.assertIn('roll_number', content.splitlines()[0])
