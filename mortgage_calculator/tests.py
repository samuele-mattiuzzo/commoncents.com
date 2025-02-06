from django.test import TestCase
from .utils import calculate_overpayment_schedule

class MortgageCalculatorTests(TestCase):

    def test_basic_mortgage_calculation(self):
        cost_of_debt = 227000
        interest_rate = 0.05  # 5%
        mortgage_term = 15 #Years
        monthly_payment = 1867.75 #Calculated using online calculator
        one_off_overpayment = 0
        recurring_overpayment = 0

        schedule = calculate_overpayment_schedule(
            cost_of_debt, interest_rate, mortgage_term, monthly_payment, one_off_overpayment, recurring_overpayment
        )

        self.assertEqual(len(schedule), mortgage_term + 1)  # +1 for year 0

        #Check the first year
        self.assertEqual(schedule[1]['remaining_balance'], 227000)
        self.assertEqual(schedule[1]['total_paid_standard'], 22413)
        self.assertEqual(schedule[1]['total_paid_overpayment'], 0)

        #Check the last year
        self.assertAlmostEqual(schedule[-1]['ending_balance'], 0, delta=1) #Use delta to check for near 0. Floating point calculations can have some small variations.


    def test_one_off_overpayment(self):
        cost_of_debt = 227000
        interest_rate = 0.05
        mortgage_term = 15 #Years
        monthly_payment = 1867.75 #Calculated using online calculator
        one_off_overpayment = 12000
        recurring_overpayment = 0

        schedule = calculate_overpayment_schedule(
            cost_of_debt, interest_rate, mortgage_term, monthly_payment, one_off_overpayment, recurring_overpayment
        )

        self.assertEqual(len(schedule), mortgage_term + 1)

        #Check the first year
        self.assertEqual(schedule[1]['remaining_balance'], 215000)
        self.assertEqual(schedule[1]['total_paid_standard'], 22413)
        self.assertEqual(schedule[1]['total_paid_overpayment'], 12000)


    def test_recurring_overpayment(self):
        cost_of_debt = 227000
        interest_rate = 0.05
        mortgage_term = 15 #Years
        monthly_payment = 1867.75 #Calculated using online calculator
        one_off_overpayment = 0
        recurring_overpayment = 1000

        schedule = calculate_overpayment_schedule(
            cost_of_debt, interest_rate, mortgage_term, monthly_payment, one_off_overpayment, recurring_overpayment
        )

        self.assertEqual(len(schedule), mortgage_term + 1)

        #Check the first year
        self.assertEqual(schedule[1]['remaining_balance'], 215300)
        self.assertEqual(schedule[1]['total_paid_standard'], 22413)
        self.assertEqual(schedule[1]['total_paid_overpayment'], 12000)

    def test_combined_overpayments(self):
        cost_of_debt = 227000
        interest_rate = 0.05
        mortgage_term = 15 #Years
        monthly_payment = 1867.75 #Calculated using online calculator
        one_off_overpayment = 12000
        recurring_overpayment = 1000

        schedule = calculate_overpayment_schedule(
            cost_of_debt, interest_rate, mortgage_term, monthly_payment, one_off_overpayment, recurring_overpayment
        )

        self.assertEqual(len(schedule), mortgage_term + 1)

        #Check the first year
        self.assertEqual(schedule[1]['remaining_balance'], 203300)
        self.assertEqual(schedule[1]['total_paid_standard'], 22413)
        self.assertEqual(schedule[1]['total_paid_overpayment'], 22700) #12000 + 10700

        # Check the second year
        self.assertAlmostEqual(schedule[2]['remaining_balance'], 190500, delta=100) #Use delta to check for near 0. Floating point calculations can have some small variations.
        self.assertEqual(schedule[2]['total_paid_standard'], 44826)
        self.assertAlmostEqual(schedule[2]['total_paid_overpayment'], 45400, delta=100) #Use delta to check for near 0. Floating point calculations can have some small variations.
