from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from .api import TempMail
import random


def make_keyboard_for_messages(emails):
    temp = TempMail()
    if emails.domain not in temp.get_list_of_active_domains:
        temp.domain = random.choice(temp.get_list_of_active_domains)
        emails.domain = temp.domain

    temp.domain = emails.domain
    temp.login = emails.email
    lists = temp.get_list_of_emails()
    markup = InlineKeyboardMarkup()
    for i in range(len(lists)):
        markup.add((InlineKeyboardButton(f"{lists[i]['subject']}",callback_data=f'{i}')))
    return markup
