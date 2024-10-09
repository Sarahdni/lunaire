import unittest
from datetime import datetime
from src.cycle_calculator import calculate_cycle

class TestCycleCalculator(unittest.TestCase):
    def test_calculate_cycle(self):
        # Test avec une chaîne de caractères
        start_date_str = "01/01/2023"
        cycle_length = 28
        period_length = 5
        num_months = 1

        phases = calculate_cycle(start_date_str, cycle_length, period_length, num_months)

        self.assertEqual(len(phases), 4)  # 4 phases in a cycle
        self.assertEqual(phases[0][0], "Menstrual")
        self.assertEqual(phases[1][0], "Follicular")
        self.assertEqual(phases[2][0], "Ovulatory")
        self.assertEqual(phases[3][0], "Luteal")

        # Vérifiez que les phases couvrent tout le cycle
        self.assertEqual((phases[-1][2] - phases[0][1]).days, cycle_length)

        # Test avec un objet datetime
        start_date_dt = datetime(2023, 1, 1)
        phases = calculate_cycle(start_date_dt, cycle_length, period_length, num_months)

        self.assertEqual(len(phases), 4)  # 4 phases in a cycle
        self.assertEqual(phases[0][0], "Menstrual")
        self.assertEqual(phases[1][0], "Follicular")
        self.assertEqual(phases[2][0], "Ovulatory")
        self.assertEqual(phases[3][0], "Luteal")

        # Vérifiez que les phases couvrent tout le cycle
        self.assertEqual((phases[-1][2] - phases[0][1]).days, cycle_length)

if __name__ == '__main__':
    unittest.main()