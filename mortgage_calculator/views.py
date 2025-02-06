from django.shortcuts import render
from django.views.generic import TemplateView
from .utils import calculate_overpayment_schedule


class AffordabilityCalculatorView(TemplateView):
    template_name = 'mortgage_calculator/affordability.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_results'] = False
        return context

    def post(self, request, *args, **kwargs):
        income = float(request.POST.get('income'))
        expenses = float(request.POST.get('expenses'))
        deposit = float(request.POST.get('deposit'))
        interest_rate = float(request.POST.get('interest_rate')) / 100 / 12  # Monthly rate
        mortgage_term = int(request.POST.get('mortgage_term'))*12

        # Example affordability calculation (customize as needed)
        # Assuming a certain percentage of income can be used for mortgage payments
        affordable_percentage = 0.4  # Example: 40%

        max_affordable_payment = (income * affordable_percentage) / 12 - expenses
        max_loan = (max_affordable_payment * ((1 + interest_rate)**mortgage_term - 1)) / (interest_rate * (1 + interest_rate)**mortgage_term)
        monthly_payment = (max_loan * interest_rate * (1 + interest_rate)**mortgage_term) / ((1 + interest_rate)**mortgage_term - 1)

        context = {
            'income': income,
            'expenses': expenses,
            'deposit': deposit,
            'interest_rate': interest_rate,
            'mortgage_term': mortgage_term/12,
            'max_loan': round(max_loan, 2),
            'monthly_payment': round(monthly_payment, 2),
            'show_results': True,
        }
        return render(request, self.template_name, context)


class OverpaymentCalculatorView(TemplateView):
    template_name = 'mortgage_calculator/overpayment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_results'] = False
        return context

    def post(self, request, *args, **kwargs):
        cost_of_debt = float(request.POST.get('cost_of_debt'))
        mortgage_term = int(request.POST.get('mortgage_term'))
        interest_only = request.POST.get('mortgage_type') == 'interest_only'
        interest_rate = float(request.POST.get('interest_rate')) / 100 / 12
        monthly_repayment = float(request.POST.get('monthly_repayment')) if request.POST.get('monthly_repayment') else None
        one_off_overpayment = float(request.POST.get('one_off_overpayment')) if request.POST.get('one_off_overpayment') else 0
        recurring_overpayment = float(request.POST.get('recurring_overpayment')) if request.POST.get('recurring_overpayment') else 0

        if interest_only:
            monthly_payment = cost_of_debt * interest_rate
            total_repayment = monthly_payment * mortgage_term
        else:
            if monthly_repayment:
                monthly_payment = monthly_repayment
                # TODO: investigate financial library
                total_repayment = monthly_payment * mortgage_term
            else:
                monthly_payment = (cost_of_debt * interest_rate * (1 + interest_rate)**(mortgage_term*12)) / ((1 + interest_rate)**(mortgage_term*12) - 1)
                total_repayment = monthly_payment * mortgage_term*12

        # Overpayment calculations
        overpayment_schedule = calculate_overpayment_schedule(
            cost_of_debt, interest_rate, mortgage_term, monthly_payment, 
            one_off_overpayment, recurring_overpayment
        )

        context = {
            'cost_of_debt': cost_of_debt,
            'mortgage_term': mortgage_term,
            'interest_only': interest_only,
            'interest_rate': interest_rate,
            'monthly_payment': round(monthly_payment, 2),
            'total_repayment': round(total_repayment, 2),
            'one_off_overpayment': one_off_overpayment,
            'recurring_overpayment': recurring_overpayment,
            'overpayment_schedule': overpayment_schedule,
            'show_results': True,
        }
        return render(request, self.template_name, context)
