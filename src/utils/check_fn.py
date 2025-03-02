import re

def check_day_payment_format(date_str):
    if date_str.isdigit():
        if 1 <= int(date_str)  <= 31:
            return True
    return False

def check_day_notice_format(date_str):
    if date_str.isdigit():
        if int(date_str) <= 28:
            return True
    return False

def check_time_format(time_string):
    # Регулярное выражение для формата времени чч:мм
    pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d$"
    match = re.match(pattern, time_string)
    return bool(match)
