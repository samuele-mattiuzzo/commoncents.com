import math


def calculate_overpayment_schedule(
    cost_of_debt,
    interest_rate,
    mortgage_term,
    monthly_payment,
    one_off_overpayment,
    recurring_overpayment,
):
    remaining_balance = cost_of_debt
    schedule = []
    total_paid_standard = 0
    total_paid_overpayment = 0
    year = 0

    # Apply one-off overpayment at the beginning of year 1 (capped at 10% of initial debt)
    max_overpayment_allowed_year_1 = math.ceil(cost_of_debt * 0.1)
    one_off_overpayment_applied = min(
        one_off_overpayment, max_overpayment_allowed_year_1
    )

    while remaining_balance > 0 and year < mortgage_term:
        year += 1
        starting_balance = remaining_balance

        if year == 1:  # Apply one-off payment on the first year
            remaining_balance -= one_off_overpayment_applied
            total_paid_overpayment += one_off_overpayment_applied

        total_paid_standard_year = 0
        total_paid_overpayment_year = 0

        for month in range(12):
            interest_payment = remaining_balance * interest_rate
            principal_payment = monthly_payment - interest_payment

            if principal_payment > remaining_balance:
                principal_payment = remaining_balance

            remaining_balance -= principal_payment  # Deduct principal payment
            total_paid_standard_year += monthly_payment
            total_paid_standard += monthly_payment

        # Overpayment calculations (after standard payments are done for the year)
        overpayment_allowance = math.ceil(
            starting_balance * 0.1
        )  # 10% rule, rounded up

        # Calculate recurring overpayment, considering one-off payment in year 1
        remaining_overpayment_allowance = overpayment_allowance
        initial_lump_sum = 0  # Reset initial lump sum
        if year == 1:
            # We subtract the one-off overpayment from the yearly overpayment, not the remaining balance
            remaining_overpayment_allowance -= one_off_overpayment_applied
            initial_lump_sum = one_off_overpayment_applied  # Store the initial lump sum

        monthly_overpayment_available = math.floor(
            remaining_overpayment_allowance / 12
        )  # Monthly available

        recurring_overpayment_to_use = min(
            recurring_overpayment, monthly_overpayment_available
        )

        total_paid_overpayment_year = recurring_overpayment_to_use * 12

        if total_paid_overpayment_year > overpayment_allowance:
            total_paid_overpayment_year = overpayment_allowance

        remaining_balance -= total_paid_overpayment_year  # Deduct the total overpayment
        total_paid_overpayment += (
            total_paid_overpayment_year  # Accumulate the total overpayments
        )

        ending_balance = remaining_balance if remaining_balance > 0 else 0

        schedule.append(
            {
                "year": year,
                "remaining_balance": math.ceil(
                    starting_balance
                ),  # Show the starting balance
                "ending_balance": math.ceil(ending_balance),
                "total_paid_standard": math.ceil(total_paid_standard),
                "total_paid_overpayment": math.ceil(
                    total_paid_overpayment_year
                ),  # Show the yearly overpayment
                "overpayment_allowance": math.ceil(overpayment_allowance),
                "monthly_overpayment_available": math.ceil(
                    monthly_overpayment_available
                ),
                "yearly_overpayment": math.ceil(total_paid_overpayment_year),
                "initial_lump_sum": math.ceil(
                    initial_lump_sum
                ),  # Add the initial lump sum
            }
        )

    return schedule
