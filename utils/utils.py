import datetime
from re import compile


def is_date_format(string_to_test):
    '''Check if the variable is could be set as datetime type
    with the following format:
        dd/mm/yyyy
            If its the case, check if the date value are coherent.
                If its not the case a error message is sent.
                Otherwise, the datetime is return
    '''
    date_format = compile(r"^(\d?\d)\W(\d?\d)\W(\d{4})$")
    string_match = date_format.match(string_to_test)
    if string_match:
        try:
            date = datetime.date(
                int(string_match.group(3)),
                int(string_match.group(2)),
                int(string_match.group(1)))
        except ValueError as exception:
            return str(exception)
        return date
    else:
        return False


def datetime_to_str(date):
    '''Check the date type, if its a datime type:
    Return the date with the following format:
        dd/mm/yyyy

    '''
    if isinstance(date, datetime.date):
        str_date = (
            f"{date.day:0>2d}/"
            + f"{date.month:0>2d}/"
            + str(date.year)
            )
        return str_date
    return False


def date_str_to_format_date(date):
    '''Convert a date from text format to date format:
    Return the date with the following format:
        mm/dd/yyyy

    '''
    date = date.split("/")
    date = datetime.date(int(date[2]), int(date[1]), int(date[0]))
    return date


def date_compare_if_previous(date_1, date_2):
    '''Compares two dates:
    if date_2 is earlier than the first

    '''
    date_1 = date_str_to_format_date(date_1)
    date_2 = date_str_to_format_date(date_2)
    if date_1 == date_2 or date_1 < date_2:
        return False
    else:
        return True


def date_now():
    '''Returns today's date

    '''
    date_now = datetime.datetime.today().strftime('%d/%m/%Y')
    return date_now


def valid_name(name):
    '''Check the format of a string which should
    correspond to a name or a firstname.

    '''
    for elem in name:
        if not(
                elem.isalpha()
                or elem.isspace()
                or elem == "\'"
                or elem == "-"):
            return False
    return True
