from django.test import TestCase
from .utils import calculate_overpayment_schedule
import math

class MortgageCalculatorTests(TestCase):

    def test_basic_mortgage_calculation(self):
        cost_of_debt = 227000
        interest_rate = 0.05
        mortgage_term = 15
        monthly_payment = 1867.75
        one_off_overpayment = 0
        recurring_overpayment = 0

        schedule = calculate_overpayment_schedule(
            cost_of_debt, interest_rate, mortgage_term, monthly_payment, one_off_overpayment, recurring_overpayment
        )

        self.assertEqual(len(schedule), mortgage_term)  # No Year 0

        self.assertEqual(schedule[0]['year'], 1)
        self.assertEqual(schedule[0]['remaining_balance'], 227000)
        self.assertAlmostEqual(schedule[0]['total_paid_standard'], 22413, delta=1)
        self.assertEqual(schedule[0]['total_paid_overpayment'], 0)
        self.assertEqual(schedule[0]['initial_lump_sum'], 0)

        self.assertEqual(schedule[14]['year'], 15)
        self.assertAlmostEqual(schedule[14]['ending_balance'], 0, delta=1)
        self.assertAlmostEqual(schedule[14]['total_paid_standard'], 336202, delta=1)
        self.assertAlmostEqual(schedule[14]['total_paid_overpayment'], 0, delta=1)
        self.assertEqual(schedule[14]['initial_lump_sum'], 0)


    def test_one_off_overpayment(self):
        cost_of_debt = 227000
        interest_rate = 0.05
        mortgage_term = 15
        monthly_payment = 1867.75
        one_off_overpayment = 12000
        recurring_overpayment = 0

        schedule = calculate_overpayment_schedule(
            cost_of_debt, interest_rate, mortgage_term, monthly_payment, one_off_overpayment, recurring_overpayment
        )

        self.assertEqual(len(schedule), mortgage_term)

        self.assertEqual(schedule[0]['year'], 1)
        self.assertEqual(schedule[0]['remaining_balance'], 215000)  # Corrected
        self.assertAlmostEqual(schedule[0]['total_paid_standard'], 22413, delta=1)
        self.assertEqual(schedule[0]['total_paid_overpayment'], 12000)
        self.assertEqual(schedule[0]['initial_lump_sum'], 12000)


    def test_recurring_overpayment(self):
        cost_of_debt = 227000
        interest_rate = 0.05
        mortgage_term = 15
        monthly_payment = 1867.75
        one_off_overpayment = 0
        recurring_overpayment = 1000

        schedule = calculate_overpayment_schedule(
            cost_of_debt, interest_rate, mortgage_term, monthly_payment, one_off_overpayment, recurring_overpayment
        )

        self.assertEqual(len(schedule), mortgage_term)

        self.assertEqual(schedule[0]['year'], 1)
        self.assertEqual(schedule[0]['remaining_balance'], 227000) # Corrected
        self.assertAlmostEqual(schedule[0]['total_paid_standard'], 22413, delta=1)
        self.assertEqual(schedule[0]['total_paid_overpayment'], 12000) # Corrected
        self.assertEqual(schedule[0]['initial_lump_sum'], 0)


    def test_combined_overpayments(self):
        cost_of_debt = 227000
        interest_rate = 0.05
        mortgage_term = 15
        monthly_payment = 1867.75
        one_off_overpayment = 12000
        recurring_overpayment = 1000

        schedule = calculate_overpayment_schedule(
            cost_of_debt, interest_rate, mortgage_term, monthly_payment, one_off_overpayment, recurring_overpayment
        )

        self.assertEqual(len(schedule), mortgage_term)

        self.assertEqual(schedule[0]['year'], 1)
        self.assertEqual(schedule[0]['remaining_balance'], 203300) # Corrected
        self.assertAlmostEqual(schedule[0]['total_paid_standard'], 22413, delta=1)
        self.assertEqual(schedule[0]['total_paid_overpayment'], 22700) # Corrected
        self.assertEqual(schedule[0]['initial_lump_sum'], 12000)

        self.assertEqual(schedule[1]['year'], 2)
        self.assertAlmostEqual(schedule[1]['remaining_balance'], 190500, delta=100)
        self.assertAlmostEqual(schedule[1]['total_paid_standard'], 44826, delta=1)
        self.assertAlmostEqual(schedule[1]['total_paid_overpayment'], 24000, delta=100) # Corrected
        self.assertEqual(schedule[1]['initial_lump_sum'], 0)
