from django.db import migrations, models
import django.db.models.deletion
import datetime


def today():
    return datetime.date.today()


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('roll_number', models.CharField(max_length=50, unique=True)),
                ('address', models.TextField(blank=True)),
                ('department', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('enrollment_date', models.DateField(default=today)),
                ('status', models.CharField(default='active', max_length=20)),
                ('gpa', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=150, unique=True)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('paid', models.BooleanField(default=False)),
                ('issued_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='students.student')),
            ],
            options={
                'ordering': ['-issued_at'],
            },
        ),
    ]
