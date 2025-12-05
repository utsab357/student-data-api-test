from django.core.management.base import BaseCommand
from students.models import Student, Invoice
import random
from decimal import Decimal

try:
    from faker import Faker
    faker = Faker()
except Exception:
    faker = None

class Command(BaseCommand):
    help = 'Populate database with 200 students and 0-3 invoices each'

    def handle(self, *args, **options):
        departments = ['CSE', 'ECE', 'ME', 'IT']
        total_students = 200
        created_students = 0
        created_invoices = 0
        for i in range(1, total_students + 1):
            roll = f'R{i:04d}'
            dept = departments[(i-1) % len(departments)]
            name = faker.name() if faker else f'Student {i}'
            phone = faker.phone_number() if faker else f'+1000000{i:04d}'
            email = faker.email() if faker else f'student{i}@example.com'
            address = faker.address() if faker else f'Address {i}'
            dob = faker.date_of_birth(minimum_age=18, maximum_age=30) if faker else None
            enrollment_date = faker.date_between(start_date='-4y', end_date='today') if faker else None
            gpa = round(random.uniform(2.0, 4.0), 2)
            s, created = Student.objects.get_or_create(
                roll_number=roll,
                defaults={
                    'name': name,
                    'address': address,
                    'department': dept,
                    'phone': phone,
                    'email': email,
                    'date_of_birth': dob,
                    'enrollment_date': enrollment_date or None,
                    'gpa': Decimal(str(gpa)),
                }
            )
            if created:
                created_students += 1
            # create 0-3 invoices
            num_invoices = random.randint(0, 3)
            for seq in range(1, num_invoices + 1):
                invoice_num = f'INV-{s.roll_number}-{seq}'
                amount = Decimal(str(round(random.uniform(1000.0, 50000.0), 2)))
                paid = random.choice([True, False])
                inv, icreated = Invoice.objects.get_or_create(
                    invoice_number=invoice_num,
                    defaults={
                        'student': s,
                        'amount': amount,
                        'paid': paid,
                    }
                )
                if icreated:
                    created_invoices += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created_students} students and {created_invoices} invoices'))
