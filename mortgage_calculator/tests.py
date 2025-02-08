from django.test import TestCase
from .utils import calculate_overpayment_schedule
import math


class MortgageCalculatorTests(TestCase):

    def setUp(self):
        self.cost_of_debt = 6000  # 1200 * 5
        self.interest_rate = 0.00
        self.mortgage_term = 5
        self.monthly_payment = 100
        self.one_off_overpayment = 0
        self.recurring_overpayment = 0

    def test_basic_mortgage_calculation(self):
        schedule = calculate_overpayment_schedule(
            self.cost_of_debt,
            self.interest_rate,
            self.mortgage_term,
            self.monthly_payment,
            self.one_off_overpayment,
            self.recurring_overpayment,
        )

        self.assertEqual(len(schedule), self.mortgage_term)

        self.assertEqual(schedule[0]["year"], 1)
        self.assertEqual(schedule[0]["remaining_balance"], self.cost_of_debt)
        self.assertAlmostEqual(schedule[0]["total_paid_standard"], 1200, delta=1)
        self.assertEqual(schedule[0]["total_paid_overpayment"], 0)
        self.assertEqual(schedule[0]["initial_lump_sum"], 0)

        self.assertEqual(schedule[4]["year"], self.mortgage_term)
        self.assertAlmostEqual(schedule[4]["ending_balance"], 0, delta=1)
        self.assertAlmostEqual(schedule[4]["total_paid_standard"], 6000, delta=1)
        self.assertAlmostEqual(schedule[4]["total_paid_overpayment"], 0, delta=1)
        self.assertEqual(schedule[4]["initial_lump_sum"], 0)

    def test_one_off_overpayment(self):
        one_year_overpayment = 600
        schedule = calculate_overpayment_schedule(
            self.cost_of_debt,
            self.interest_rate,
            self.mortgage_term,
            self.monthly_payment,
            one_year_overpayment,
            self.recurring_overpayment,
        )

        self.assertEqual(len(schedule), self.mortgage_term)

        self.assertEqual(schedule[0]["year"], 1)
        self.assertEqual(schedule[0]["remaining_balance"], 6000)
        self.assertAlmostEqual(schedule[0]["total_paid_standard"], 1200, delta=1)
        self.assertEqual(schedule[0]["initial_lump_sum"], 600)

        self.assertEqual(schedule[1]["year"], 2)
        self.assertEqual(schedule[1]["remaining_balance"], 4200)

    def test_recurring_overpayment(self):
        recurring_overpayment = 50

        schedule = calculate_overpayment_schedule(
            self.cost_of_debt,
            self.interest_rate,
            self.mortgage_term,
            self.monthly_payment,
            self.one_off_overpayment,
            recurring_overpayment,
        )

        self.assertEqual(len(schedule), self.mortgage_term - 1)

        self.assertEqual(schedule[0]["year"], 1)
        self.assertEqual(schedule[0]["remaining_balance"], 6000)
        self.assertAlmostEqual(schedule[0]["total_paid_standard"], 1200, delta=1)
        self.assertEqual(schedule[0]["total_paid_overpayment"], 600)

        self.assertEqual(schedule[1]["year"], 2)
        self.assertEqual(schedule[1]["remaining_balance"], 4200)

    def test_combined_overpayments(self):
        one_year_overpayment = 300
        recurring_overpayment = 25

        schedule = calculate_overpayment_schedule(
            self.cost_of_debt,
            self.interest_rate,
            self.mortgage_term,
            self.monthly_payment,
            one_year_overpayment,
            recurring_overpayment,
        )

        self.assertEqual(len(schedule), self.mortgage_term - 1)

        self.assertEqual(schedule[0]["year"], 1)
        self.assertEqual(schedule[0]["remaining_balance"], 6000)
        self.assertAlmostEqual(schedule[0]["total_paid_standard"], 1200, delta=1)
        self.assertEqual(schedule[0]["initial_lump_sum"], 300)
        self.assertEqual(schedule[0]["total_paid_overpayment"], 300)

        self.assertEqual(schedule[1]["year"], 2)
        self.assertEqual(schedule[1]["remaining_balance"], 4200)
