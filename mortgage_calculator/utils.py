import math


def calculate_overpayment_schedule(cost_of_debt, interest_rate, mortgage_term, monthly_payment, one_off_overpayment, recurring_overpayment):
    remaining_balance = cost_of_debt
    schedule = []
    total_paid_standard = 0
    total_paid_overpayment = 0
    year = 0

    while remaining_balance > 0 and year < mortgage_term:
        year += 1
        starting_balance = remaining_balance

        total_paid_standard_year = 0
        total_paid_overpayment_year = 0

        for _ in range(12):
            interest_payment = remaining_balance * interest_rate
            principal_payment = monthly_payment - interest_payment

            if principal_payment > remaining_balance:
                principal_payment = remaining_balance

            remaining_balance -= principal_payment  # Deduct principal payment
            total_paid_standard_year += monthly_payment
            total_paid_standard += monthly_payment

            # Overpayment calculations (after standard payments are done for the month)
            max_overpayment_allowed = math.ceil(starting_balance * 0.1)  # 10% rule, rounded up
            max_monthly_overpayment = math.ceil(max_overpayment_allowed / 12)

            overpayment_this_month = 0
            if year == 1 and one_off_overpayment > 0:  # One-off payment (only in year 1)
                overpayment_this_month = min(one_off_overpayment, max_overpayment_allowed)
                one_off_overpayment = 0  # Only apply once
            elif recurring_overpayment > 0:
                overpayment_this_month = min(recurring_overpayment, max_monthly_overpayment)  # Use min of user input or max allowed

            remaining_balance -= overpayment_this_month  # Deduct overpayment
            total_paid_overpayment += overpayment_this_month
            total_paid_overpayment_year += overpayment_this_month

        ending_balance = remaining_balance if remaining_balance > 0 else 0
        recurring_overpayment_used = min(recurring_overpayment, max_monthly_overpayment) # Use min of user input or max allowed * 12 months

        schedule.append({
            'year': year,
            'starting_balance': math.ceil(starting_balance),
            'ending_balance': math.ceil(ending_balance),
            'total_paid_standard': math.ceil(total_paid_standard),
            'total_paid_overpayment': math.ceil(total_paid_overpayment),
            'max_overpayment_allowed': math.ceil(max_overpayment_allowed),
            'max_monthly_overpayment': math.ceil(max_monthly_overpayment),
            'recurring_overpayment_used': math.ceil(recurring_overpayment_used),  # Show the adjusted recurring overpayment

            #'recurring_overpayment_used': math.ceil(recurring_overpayment),  # User's recurring overpayment input
        })

    return schedule
