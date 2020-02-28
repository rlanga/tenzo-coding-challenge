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


# for h in [x for x in range(int(shift_start[0]) + 1, int(shift_end[0])) if x not in range(int(break_times[0].split(':')[0]), int(break_times[1].split(':')[0]))]:
            #     print(h)