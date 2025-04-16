from datetime import date, timedelta
from math import ceil

def format_number_with_commas(number):
    """Formats an integer with commas as thousands separators."""
    return "{:,}".format(number)

def round_to_nearest_ten(number):
    """Rounds a number to the nearest 10."""
    return round(number / 10) * 10

def create_cumulative_step_calendar_string_formatted(yearly_goal):
    """
    Creates a .ics calendar string with formatted cumulative pro-rata
    step goal event titles for each day of the year.

    Args:
        yearly_goal (int): The total number of steps to achieve in the year.

    Returns:
        str: A string containing the .ics calendar data.
    """
    today = date.today()
    current_year = today.year
    start_of_year = date(current_year, 1, 1)
    end_of_year = date(current_year, 12, 31)
    days_in_year = (end_of_year - start_of_year).days + 1

    calendar_string = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Yearly Pro-Rata Step Goal Calendar {current_year}//EN
"""

    current_date = start_of_year
    day_of_year = 1
    while current_date <= end_of_year:
        cumulative_goal_exact = (yearly_goal / days_in_year) * day_of_year
        cumulative_goal_rounded = round_to_nearest_ten(cumulative_goal_exact)
        formatted_goal = format_number_with_commas(cumulative_goal_rounded)

        event_start_str = current_date.strftime("%Y%m%d")
        event_end_str = (current_date + timedelta(days=1)).strftime("%Y%m%d")
        timestamp_str = today.strftime("%Y%m%dT%H%M%SZ")  # UTC timestamp

        event_string = f"""BEGIN:VEVENT
UID:{current_date.strftime("%Y%m%d")}@reiwaproratastepgoalcalendar
DTSTAMP:{timestamp_str}
DTSTART;VALUE=DATE:{event_start_str}
DTEND;VALUE=DATE:{event_end_str}
SUMMARY:{formatted_goal}
END:VEVENT
"""
        calendar_string += event_string
        current_date += timedelta(days=1)
        day_of_year += 1

    calendar_string += "END:VCALENDAR"

    return calendar_string

if __name__ == "__main__":
    yearly_step_goal = 3000000

    ics_string = create_cumulative_step_calendar_string_formatted(yearly_step_goal)
    print(ics_string)