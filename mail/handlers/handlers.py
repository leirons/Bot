import redis
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from .text import subject
from django.core.mail import send_mail
from .utils import check
from mail.models import User, Email, TempEmail
import datetime
from .api import TempMail
from .keyboards import make_keyboard_for_messages

r = redis.Redis()

t = TempMail()


class SendMailForm(StatesGroup):
    subject = State()
    message = State()
    to_mail = State()


async def send_email(m: Message):
    await SendMailForm.subject.set()
    await User.get_user_or_created(m.from_user.id)
    await m.reply(subject)


async def process_subject(message: Message, state: FSMContext):
    async with state.proxy() as data:
        print(await state.get_state())
        data['subject'] = message.text
    await SendMailForm.next()
    await message.reply("Enter a text to send")


async def process_message(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['message'] = message.text
    await SendMailForm.next()
    await message.reply("Enter a email")


async def process_email(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
        if not (check(data['email'])):
            await message.reply("Email is not valid,try again from begin")
            await state.finish()

        send_mail(
            data['subject'],
            data['message'],
            'grecigor11@gmail.com',
            [data['email']],
            fail_silently=False,
        )
        await message.answer('Message is sent')
        await state.finish()


class SendMailFormInTheFuture(StatesGroup):
    subject = State()
    message = State()
    to_mail = State()
    date = State()


async def send_email_in_the_future(m: Message):
    await SendMailFormInTheFuture.subject.set()
    await User.get_user_or_created(m.from_user.id)
    await m.reply(subject)


async def process_subject2(message: Message, state: FSMContext):
    async with state.proxy() as data:
        print(await state.get_state())
        data['subject'] = message.text
    await SendMailFormInTheFuture.next()
    await message.reply("Enter a text to send")


async def process_message2(message: Message, state: FSMContext):
    async with state.proxy() as data:
        print(await state.get_state())
        data['message'] = message.text
    await SendMailFormInTheFuture.next()
    await message.reply("Enter a email")


async def process_email2(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
        if not (check(data['email'])):
            await message.reply("Email is not valid,try again from begin")
            await state.finish()
        await SendMailFormInTheFuture.next()
        await message.reply("Enter date in format YYYY-MM-DD")


async def process_date(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
        data['user'] = message.from_user.id
        day, month, year = message.text.split('-')

        is_valid = True
        try:
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            is_valid = False
        if is_valid:
            u, c = await User.get_user_or_created(message.from_user.id)
            await Email.get_email_or_created(u=u, data=data, )
            await message.reply('Message is sent')
        else:
            await message.reply('Date is invalid - format dd-mm-yy')
            await state.finish()


class CreateTempMail(StatesGroup):
    name = State()
    domain = State()


async def create_temp_mail(m: Message):
    await CreateTempMail.name.set()
    await User.get_user_or_created(m.from_user.id)
    await m.reply('Enter name of your email')


async def process_email_name(m: Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = m.text
        await m.reply(f'Input domain, avaivable domains:\n{t.get_list_of_active_domains}\n')
        await CreateTempMail.next()


async def process_email_domain(m: Message, state: FSMContext):
    async with state.proxy() as data:
        data['domain'] = m.text
        u, created = await User.get_user_or_created(m.from_user.id)
        await TempEmail.create_temp_mail(u=u, domain=data['domain'], email=data['email'])
        await state.finish()


async def choose_messages_from_temp_mail(m: Message):
    u, created = await User.get_user_or_created(m.from_user.id)
    e = await TempEmail.get_temp_mail(u)
    objects = make_keyboard_for_messages(e)
    await m.reply(text='Выберите сообщение которое хотите прочитать', reply_markup=objects)


async def read_messages_from_temp_mail(q: CallbackQuery):
    u, c = await User.get_user_or_created(q.from_user.id)
    email = await TempEmail.get_temp_mail(u)
    temp = TempMail(login=email.email, domain=email.domain)
    data = temp.get_list_of_emails()[int(q.data)]
    m = temp.read_message(id=data['id']).json()
    await q.message.answer(text=f"from: {m['from']}\n subject: {m['subject']}\n text: {m['textBody']}")
