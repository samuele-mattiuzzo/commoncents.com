from django.urls import path
from . import views

app_name = 'calculators'

urlpatterns = [
    path('affordability', views.AffordabilityCalculatorView.as_view(), name='affordability_calculator'),
    path('overpayment', views.OverpaymentCalculatorView.as_view(), name='overpayment_calculator'),
]
