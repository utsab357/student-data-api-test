from rest_framework import serializers
from .models import Student, Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    invoices = InvoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'name', 'roll_number', 'address', 'department', 'phone', 'email',
            'date_of_birth', 'enrollment_date', 'status', 'gpa', 'created_at', 'invoices'
        ]
        read_only_fields = ['created_at', 'invoices']

    def validate_roll_number(self, value):
        qs = Student.objects.filter(roll_number=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('roll_number must be unique')
        return value

    def validate_department(self, value):
        allowed = [d[0] for d in Student.DEPARTMENTS]
        if value not in allowed:
            raise serializers.ValidationError(f"department must be one of {allowed}")
        return value
