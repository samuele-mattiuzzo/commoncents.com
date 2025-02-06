from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse


class MortgageCalculatorView(TemplateView):
    template_name = 'mortgage_calculator/calculator.html'

    def post(self, request, *args, **kwargs):
        loan_amount = float(request.POST.get('loan_amount'))
        interest_rate = float(request.POST.get('interest_rate')) / 100 / 12
        loan_term = int(request.POST.get('loan_term')) * 12

        monthly_payment = (loan_amount * interest_rate * (1 + interest_rate)**loan_term) / ((1 + interest_rate)**loan_term - 1)
        total_payment = monthly_payment * loan_term

        context = {
            'monthly_payment': round(monthly_payment, 2),
            'total_payment': round(total_payment, 2),
        }
        return render(request, 'mortgage_calculator/results.html', context)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) # handles the initial form display

# In your urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.MortgageCalculatorView.as_view(), name='mortgage_calculator'),
]
