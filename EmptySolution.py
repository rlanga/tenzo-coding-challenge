"""
Please write you name here: Roy Langa
"""

from re import split, sub


def parse_break_note(note, shift_start_time):
    """
    Parses a time value in a shift break note into 24h %H:%M string format
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

    ''' 
    Convert the break times to 24hr format based on what hour the shift begins
    e.g. if the shift starts before midnight (22:00) and the break is after midnight (02:00)
    '''
    if break_start_hour < shift_start_hour:
        return f'{break_start_hour + 12}:{break_start[1]}', f'{int(break_end[0]) + 12}:{break_end[1]}'
    else:
        return f'{break_start[0]}:{break_start[1]}', f'{break_end[0]}:{break_end[1]}'


def format_time_string(t):
    """
    Converts a time string to %H:%M format but does not do 24hr conversion
    :param t: The time value extracted from a shift note.
        (e.g. '15' or '3PM' or '18.20')
    :type t: str
    :return: A time string with format  %H:%M
    :rtype: str
    """
    # The hour and minute values are separated out. If there is a minute value, array length will be 2
    split_values = split('[:.]', sub('(AM|PM)', '', t))
    if len(split_values) == 2:
        return f'{split_values[0]}:{split_values[1]}'
    else:
        return f'{split_values[0]}:00'


def rate_calculation_for_minutes(minutes, hourly_rate):
    """
    Calculates the hourly rate when a shift doesn't start on top of the hour.
        Using the fraction of minutes per hour and multiplying that by the hourly rate
    :param minutes: The minutes value of the shift
    :type minutes: int
    :param hourly_rate: The hourly pay rate
    :type hourly_rate: float
    :return: The hourly rate calculated for minutes
    :rtype: float
    """
    return hourly_rate * (minutes / 60.0)


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

            hourly_rate = float(shift[2])
            shift_start = shift[3].split(':')
            shift_end = shift[1].split(':')

            # Process the shift start and end times as these might not always start on the hour
            if f'{shift_start[0]}:00' in result:
                # add the remaining minutes in the hour from commencement of the shift
                result[f'{shift_start[0]}:00'] += rate_calculation_for_minutes(60 - int(shift_start[1]), hourly_rate)
            else:
                result[f'{shift_start[0]}:00'] = rate_calculation_for_minutes(60 - int(shift_start[1]), hourly_rate)

            if shift_end[1] != '00':
                if f'{shift_end[0]}:00' in result:
                    result[f'{shift_end[0]}:00'] += rate_calculation_for_minutes(int(shift_end[1]), hourly_rate)
                else:
                    result[f'{shift_end[0]}:00'] = rate_calculation_for_minutes(int(shift_end[1]), hourly_rate)

            # iterate through the shift hours excluding the shift start and end hours
            for h in range(int(shift_start[0]) + 1, int(shift_end[0])):
                if f'{h}:00' in result:
                    result[f'{h}:00'] += hourly_rate
                else:
                    result[f'{h}:00'] = hourly_rate

            break_times = parse_break_note(shift[0], shift[3])
            break_start = break_times[0].split(":")
            break_end = break_times[1].split(":")

            if break_start[0] != break_end[0]:
                # subtract the remaining minutes in the hour which fall under the break period (60 - minutes-elapsed)
                if f'{break_start[0]}:00' in result:
                    result[f'{break_start[0]}:00'] -= \
                        rate_calculation_for_minutes(60 - int(break_start[1]), hourly_rate)
                else:
                    result[f'{break_start[0]}:00'] = \
                        0 - rate_calculation_for_minutes(60 - int(break_start[1]), hourly_rate)

                if break_end[1] != '00':
                    if f'{break_end[0]}:00' in result:
                        result[f'{break_end[0]}:00'] -= rate_calculation_for_minutes(int(break_end[1]), hourly_rate)
                    else:
                        result[f'{break_end[0]}:00'] = rate_calculation_for_minutes(int(break_end[1]), hourly_rate)

                # iterate through the break hours excluding the shift start and end hours
                for h in range(int(break_start[0]) + 1, int(break_end[0])):
                    if f'{h}:00' in result:
                        result[f'{h}:00'] -= hourly_rate
            else:
                if f'{break_start[0]}:00' in result:
                    result[f'{break_start[0]}:00'] -= rate_calculation_for_minutes(int(break_end[1]) -
                                                                                   int(break_start[1]), hourly_rate)
                else:
                    result[f'{break_start[0]}:00'] = \
                        0 - rate_calculation_for_minutes(int(break_end[1]) - int(break_start[1]), hourly_rate)
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
    result = {hour: 0 for hour in {*shifts.keys(), *sales.keys()}}
    for hour in result:
        if hour in sales:
            result[hour] = (shifts[hour] / sales[hour]) * 100
        else:
            result[hour] -= shifts[hour]
    return result


def best_and_worst_hour(percentages):
    """

    :param: percentages: output of compute_percentage
    :type percentages: dict
    :return: list of strings, the first element should be the best hour,
    the second (and last) element should be the worst hour. Hour are
    represented by string with format %H:%M
    e.g. ["18:00", "20:00"]
    :rtype: list
    """
    best = 0
    worst = 0
    # best hour is lowest percentage value
    # worst hour is highest percentage value if no negative value exists else lowest negative value

    hours_with_sales = {hour: percentages[hour] for hour in percentages if percentages[hour] > 0}
    if len(hours_with_sales.keys()) > 0:
        best = min(hours_with_sales, key=hours_with_sales.get)
        worst = max(hours_with_sales, key=hours_with_sales.get)

    # look for any hours where there were no sales and get the lowest value
    for hour in percentages:
        if percentages[hour] <= 0 and percentages[hour] < percentages[worst]:
            worst = hour

    return [best, worst]


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
    path_to_sales = "transactions.csv"
    path_to_shifts = "work_shifts.csv"
    best, worst = main(path_to_shifts, path_to_sales)
    print(f'{best} {worst}')

# Please write you name here: Roy Langa
