from django.urls import path
from . import views

urlpatterns = [
    path('mortgage', views.MortgageCalculatorView.as_view(), name='mortgage_calculator'),
]
