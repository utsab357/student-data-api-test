from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import StudentViewSet, InvoiceViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'invoices', InvoiceViewSet, basename='invoice')

urlpatterns = [
    path('', include(router.urls)),
]
