import unittest
import EmptySolution


class TenzoCases(unittest.TestCase):
    def test_shifts_processed_successfully(self):
        expected_result = {
            '09:00': 30.0,
            '10:00': 50.0,
            '11:00': 50.0,
            '12:00': 64.0,
            '13:00': 74.0,
            '14:00': 74.0,
            '15:00': 44.0,
            '16:00': 26.67,
            '17:00': 54.0,
            '18:00': 60.0,
            '19:00': 66.0,
            '20:00': 66.0,
            '21:00': 66.0,
            '22:00': 59.0
        }
        self.assertEqual(EmptySolution.process_shifts('work_shifts.csv'), expected_result)

    def test_can_parse_break_note(self):
        self.assertEqual(('16:00', '16:10'), EmptySolution.parse_break_note('4 - 4.10PM', '09:00'))

    def test_sales_processed_successfully(self):
        expected_result = {
            '10:00': 130.88,
            '11:00': 320.65,
            '12:00': 514.65,
            '13:00': 406.08,
            '14:00': 177.77,
            '15:00': 63.43,
            '16:00': 75.42,
            '17:00': 142.34,
            '18:00': 748.62,
            '19:00': 421.08,
            '21:00': 240.54
        }
        self.assertEqual(EmptySolution.process_sales('transactions.csv'), expected_result)

    # def test_can_calculate_time_period_less_than_an_hour(self):
    #     self.assertEqual('0:50', EmptySolution.get_total_time_period('15:40', '16:30'))
    #
    # def test_can_calculate_time_period_greater_than_an_hour(self):
    #     self.assertEqual('1:10', EmptySolution.get_total_time_period('15:40', '16:50'))

    def test_can_calculate_percentages(self):
        shifts = EmptySolution.process_shifts('work_shifts.csv')
        sales = EmptySolution.process_sales('transactions.csv')
        self.assertEqual('{"17:00": 20, "22:00": -40,}', EmptySolution.compute_percentage(shifts, sales))


if __name__ == '__main__':
    unittest.main()
