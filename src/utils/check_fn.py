def check_date_format(date_str):
    if date_str.isdigit():
        if 1 <= int(date_str)  <= 31:
            return True
    return False
