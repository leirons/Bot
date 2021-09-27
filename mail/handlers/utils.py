import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def check(email):
    return True if re.fullmatch(regex,email) else False


def get_email(u):
    pass