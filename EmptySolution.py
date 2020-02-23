"""
Please write you name here: Roy Langa
"""

from re import split, sub


def parse_break_note(note, shift_start_time):
    """

    :param note: Details on when a shift break starts and ends
    :type note: str
    :param shift_start_time: When the shift starts
    :type shift_start_time: str
    :return: A tuple with the starting and ending hours with format %H:%M
        (e.g. ("18:00", "18:30"))
    :rtype: tuple
    """
    time_period = note.replace(' ', '').split('-')
    shift_start_hour = int(shift_start_time.split(':')[0])
    break_start = format_time_string(time_period[0]).split(':')
    break_start_hour = int(break_start[0])
    break_end = format_time_string(time_period[1]).split(':')

    # Convert the break times to 24hr format based on what hour the shift begins
    if break_start_hour < shift_start_hour:
        return f'{break_start_hour + 12}:{break_start[1]}', f'{int(break_end[0]) + 12}:{break_end[1]}'
    else:
        return f'{break_start[0]}:{break_start[1]}', f'{break_end[0]}:{break_end[1]}'


def format_time_string(t):
    """
    Converts a time string to %H:%M format

    :param t: The time value extracted from a shift note.
        (e.g. '15' or '3PM' or '18.20')
    :type t: str
    :return: A time string with format  %H:%M
    :rtype: str
    """
    # The hour and minute values are separated out. If there is no minute value, array length will be 1
    split_values = split('[:.]', sub('(AM|PM)', '', t))
    # if 'AM' in t:
    #     if len(split_values) == 2:
    #         # return f'{split_values[0] % 12}:{split_values[1].strip("AM")}'
    #         return f'{split_values[0]}:{split_values[1].strip("AM")}'
    #     else:
    #         return f'{split_values[0]}:00'
    # elif 'PM' in t:
    #     hour = 12 if split_values[0] == '12' else split_values[0]  # + 12
    #     if len(split_values) == 2:
    #         return f'{hour}:{split_values[1].strip("PM")}'
    #     else:
    #         return f'{hour}:00'
    # else:
    if len(split_values) == 2:
        return f'{split_values[0]}:{split_values[1]}'
    else:
        return f'{split_values[0]}:00'


def get_total_time_period(start, end):
    """
    Calculates the period elapsed between two time points
    :param start: The start of the time period in 24hr format.
        (e.g. '17.10')
    :type start: str
    :param end: The end of the time period in 24hr format.
        (e.g. '18.20')
    :type end: str
    :return: A time string with format  %H:%M (e.g. '0:50', '1:20')
    :rtype: str
    """
    start_time = [int(t) for t in start.split(':')]
    end_time = [int(t) for t in end.split(':')]
    total_hours = end_time[0] - start_time[0]
    total_minutes = end_time[1] - start_time[1]

    if end_time[1] < start_time[1]:
        total_minutes = 60 - abs(total_minutes)
        # Subtract 1 from total hours because a the minute difference is not a full hour
        total_hours -= 1
        return (total_hours * 60) + total_minutes
    else:
        return (total_hours * 60) + total_minutes


def process_shifts(path_to_csv):
    """

    :param path_to_csv: The path to the work_shift.csv
    :type path_to_csv: str
    :return: A dictionary with time as key (string) with format %H:%M
        (e.g. "18:00") and cost as value (Number)
    For example, it should be something like :
    {
        "17:00": 50,
        "22:00: 40,
    }
    In other words, for the hour beginning at 17:00, labour cost was
    50 pounds
    :rtype: dict
    """

    with open(path_to_csv, 'r') as shiftcsv:
        shiftcsv.readline()  # Pass over the header line
        result = dict()
        # break_notes, end_time, pay_rate, start_time
        for s in shiftcsv:
            shift = s.split(",")

            # print(shift)
            # rate * (min/60)
            hourly_rate = float(shift[2])
            shift_start = shift[3].split(':')
            shift_end = shift[1].split(':')
            rate_calculation_for_minutes = lambda m: hourly_rate * ((60 - int(m)) / 60)

            if f'{shift_start[0]}:00' in result:
                result[f'{shift_start[0]}:00'] += rate_calculation_for_minutes(shift_start[1])
            else:
                result[f'{shift_start[0]}:00'] = rate_calculation_for_minutes(shift_start[1])

            if f'{shift_end[0]}:00' in result:
                result[f'{shift_end[0]}:00'] += rate_calculation_for_minutes(shift_end[1])
            else:
                result[f'{shift_end[0]}:00'] = rate_calculation_for_minutes(shift_end[1])

            # iterate through the shift hours excluding the shift start and end hours
            for h in range(int(shift_start[0])+1, int(shift_end[0])):
                if f'{h}:00' in result:
                    result[f'{h}:00'] += hourly_rate
                else:
                    result[f'{h}:00'] = hourly_rate

            print(parse_break_note(shift[0], shift[3])) #TODO: subtract shift break from result
        # print(result)
        return result


def process_sales(path_to_csv):
    """

    :param path_to_csv: The path to the transactions.csv
    :type path_to_csv: str
    :return: A dictionary with time (string) with format %H:%M as key and
    sales as value (string),
    and corresponding value with format %H:%M (e.g. "18:00"),
    and type float)
    For example, it should be something like :
    {
        "17:00": 250,
        "22:00": 0,
    },
    This means, for the hour beginning at 17:00, the sales were 250 dollars
    and for the hour beginning at 22:00, the sales were 0.

    :rtype: dict
    """
    with open(path_to_csv, 'r') as salescsv:
        salescsv.readline()  # Pass over the header line
        result = dict()
        # amount, time
        for s in salescsv:
            sale = s.strip().split(",")
            hour = sale[1].split(':')[0]
            if hour in result:
                result[f'{hour}:00'] += float(sale[0])
            else:
                result[f'{hour}:00'] = float(sale[0])
    return result


def compute_percentage(shifts, sales):
    """

    :param shifts:
    :type shifts: dict
    :param sales:
    :type sales: dict
    :return: A dictionary with time as key (string) with format %H:%M and
    percentage of labour cost per sales as value (float),
    If the sales are null, then return -cost instead of percentage
    For example, it should be something like :
    {
        "17:00": 20,
        "22:00": -40,
    }
    :rtype: dict
    """
    return

def best_and_worst_hour(percentages):
    """

    Args:
    percentages: output of compute_percentage
    Return: list of strings, the first element should be the best hour,
    the second (and last) element should be the worst hour. Hour are
    represented by string with format %H:%M
    e.g. ["18:00", "20:00"]

    """

    return

def main(path_to_shifts, path_to_sales):
    """
    Do not touch this function, but you can look at it, to have an idea of
    how your data should interact with each other
    """

    shifts_processed = process_shifts(path_to_shifts)
    sales_processed = process_sales(path_to_sales)
    percentages = compute_percentage(shifts_processed, sales_processed)
    best_hour, worst_hour = best_and_worst_hour(percentages)
    return best_hour, worst_hour

if __name__ == '__main__':
    # You can change this to test your code, it will not be used
    path_to_sales = ""
    path_to_shifts = ""
    best_hour, worst_hour = main(path_to_shifts, path_to_sales)


# Please write you name here: Roy Langa
