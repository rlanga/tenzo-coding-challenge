import unittest
import EmptySolution


class TenzoCases(unittest.TestCase):
    def test_shifts_processed_successfully(self):
        expected_result = {"17:00": 50, "22:00": 40}
        self.assertEqual(EmptySolution.process_shifts('work_shifts.csv'), expected_result)

    def test_can_parse_break_note(self):
        self.assertEqual(('16:00', '16:10'), EmptySolution.parse_break_note('4 - 4.10PM', '09:00'))

    def test_sales_processed_successfully(self):
        expected_result = {"17:00": 50, "22:00": 40}
        self.assertEqual(EmptySolution.process_sales('transactions.csv'), expected_result)

    def test_can_calculate_time_period_less_than_an_hour(self):
        self.assertEqual('0:50', EmptySolution.get_total_time_period('15:40', '16:30'))

    def test_can_calculate_time_period_greater_than_an_hour(self):
        self.assertEqual('1:10', EmptySolution.get_total_time_period('15:40', '16:50'))

if __name__ == '__main__':
    unittest.main()
