import datetime
import os, json

def save_current_date(date):
    """
    Save the current date to a file.

    Parameters:
    - date (datetime.date): The date to be saved.

    Returns:
    None
    """
    try:
        newDate = datetime.datetime.strptime(date.set_date, '%Y-%m-%d').date()
        save_current_date(newDate)
        print(f"Current date set to: {newDate}")
    except ValueError:
        print("Invalid date format. Please provide the date in the format YYYY-MM-DD.")

    date_str = date.strftime('%Y-%m-%d')
    with open('data/current_date.txt', 'w') as file:
        file.write(date_str)

def get_current_date():
    """
    Retrieve the current date from a file.

    Returns:
    datetime.date: The current date.
    """
    with open('data/current_date.txt', 'r') as file:
        date_str = file.read()
        if not date_str:
            return datetime.date.today()  # Return the current date as the default
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

def set_current_date(args):
    """
    Set the current date to a new date.

    Parameters:
    - args (Namespace): The command-line arguments.

    Returns:
    None
    """
    if args.set_date:
        try:
            new_date = datetime.datetime.strptime(args.set_date, '%Y-%m-%d').date()
            save_current_date(new_date)
            print(f"Current date set to: {new_date}")
        except ValueError:
            print("Invalid date format. Please provide the date in the format YYYY-MM-DD.")

import datetime

def advance_time(days_to_advance):
    """
    Advance the current date by the specified number of days.

    Parameters:
    - days_to_advance (int): The number of days to advance.

    Returns:
    None
    """
    try:
        current_date = datetime.date.today()
        new_date = current_date + datetime.timedelta(days=days_to_advance)
        print(f"Time advanced by {days_to_advance} days. Current date is now: {new_date}")
    except Exception as e:
        print(f"Error advancing time: {str(e)}")


def initialize_json_file(file_path):
    """
    Initialize a JSON file with an empty dictionary if it doesn't exist.

    Parameters:
    - file_path (str): The path to the JSON file.

    Returns:
    None
    """
    if not os.path.exists(file_path):
        with open(file_path, 'w') as json_file:
            json.dump({}, json_file, indent=2)
