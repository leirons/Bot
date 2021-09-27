from aiogram import (
    filters,executor,
    types,Bot,Dispatcher
)
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .handlers import send_email_in_the_future,process_message,process_subject,process_email,\
    SendMailForm,SendMailFormInTheFuture,send_email,process_email2,process_message2,process_subject2,process_date,\
    create_temp_mail,process_email_name,CreateTempMail,process_email_domain,choose_messages_from_temp_mail,\
    read_messages_from_temp_mail


def register_handlers(dp):
    dp.register_message_handler(send_email, commands=['send_mail'], state='*')
    dp.register_message_handler(process_subject,state=SendMailForm.subject)
    dp.register_message_handler(process_message,state=SendMailForm.message)
    dp.register_message_handler(process_email,state=SendMailForm.to_mail)

    dp.register_message_handler(send_email_in_the_future,commands=['send_mail_in_the_future'],state='*')
    dp.register_message_handler(process_subject2, state=SendMailFormInTheFuture.subject)
    dp.register_message_handler(process_message2, state=SendMailFormInTheFuture.message)
    dp.register_message_handler(process_email2, state=SendMailFormInTheFuture.to_mail)
    dp.register_message_handler(process_date, state=SendMailFormInTheFuture)

    dp.register_message_handler(create_temp_mail,commands=['create_temp_mail'],state='*')
    dp.register_message_handler(process_email_name,state=CreateTempMail.name)
    dp.register_message_handler(process_email_domain,state=CreateTempMail.domain)

    dp.register_message_handler(choose_messages_from_temp_mail,commands=['read_messages_from_temp_mail'])
    dp.register_callback_query_handler(read_messages_from_temp_mail)

    return dp


def run_pooling():
    """Run bot in pooling mod"""
    print("Bot started")
    bot = Bot(token='1848337311:AAEwV7k_B2p01wdxT9CDFTtiUn0B1GfeM9Y')
    storage = MemoryStorage()
    dp = register_handlers(dp=Dispatcher(bot,storage=storage))
    executor.start_polling(dispatcher=dp,skip_updates=True)









