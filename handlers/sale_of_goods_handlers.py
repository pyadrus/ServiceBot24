import datetime  # Дата
import json
import sqlite3

from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from loguru import logger  # Логирование с помощью loguru
from yookassa import Configuration, Payment

from db.settings_db import checking_for_presence_in_the_user_database, database
from keyboards.user_keyboards import payment_keyboard, start_menu, start_menu_keyboard, payment_keyboard_password
from system.dispatcher import bot, dp, ACCOUNT_ID, SECRET_KEY, ADMIN_CHAT_ID


def payment_yookassa_telegram_master():
    """Оплата Юкасса"""

    Configuration.account_id = ACCOUNT_ID
    Configuration.secret_key = SECRET_KEY

    description_text = "Пароль обновления: ТelegramMaster 2.0"  # Текст описания товара
    price_goods = 150.00  # Сумма товара

    payment = Payment.create(
        {"amount": {"value": price_goods, "currency": "RUB"}, "capture": True,
         "confirmation": {"type": "redirect", "return_url": "https://t.me/h24service_bot"},
         "description": description_text,
         "metadata": {'order_number': '1'},
         "receipt": {"customer": {"email": "zh.vitaliy92@yandex.ru"},
                     "items": [
                         {
                             "description": description_text,  # Название товара
                             "quantity": "1",
                             "amount": {"value": price_goods, "currency": "RUB"},  # Сумма и валюта
                             "vat_code": "1"}]}})

    payment_data = json.loads(payment.json())
    payment_id = payment_data['id']
    payment_url = (payment_data['confirmation'])['confirmation_url']
    logger.info(f"Ссылка для оплаты: {payment_url}, ID оплаты {payment_id}")
    return payment_url, payment_id


def payment_yookassa():
    """Оплата Юкасса"""

    Configuration.account_id = ACCOUNT_ID
    Configuration.secret_key = SECRET_KEY

    description_text = "Покупка программы: ТelegramMaster 2.0"  # Текст описания товара
    price_goods = 1200.00  # Сумма товара

    payment = Payment.create(
        {"amount": {"value": price_goods, "currency": "RUB"}, "capture": True,
         "confirmation": {"type": "redirect", "return_url": "https://t.me/h24service_bot"},
         "description": description_text,
         "metadata": {'order_number': '1'},
         "receipt": {"customer": {"email": "zh.vitaliy92@yandex.ru"},
                     "items": [
                         {
                             "description": description_text,  # Название товара
                             "quantity": "1",
                             "amount": {"value": price_goods, "currency": "RUB"},  # Сумма и валюта
                             "vat_code": "1"}]}})

    payment_data = json.loads(payment.json())
    payment_id = payment_data['id']
    payment_url = (payment_data['confirmation'])['confirmation_url']
    logger.info(f"Ссылка для оплаты: {payment_url}, ID оплаты {payment_id}")
    return payment_url, payment_id


@dp.callback_query(F.data.startswith("check_payment"))
async def check_payment(callback_query: types.CallbackQuery, state: FSMContext):
    """"Проверка платежа TelegramMaster 2.0"""
    split_data = callback_query.data.split("_")
    logger.info(split_data[2])
    payment_info = Payment.find_one(split_data[2])  # Проверьте статус платежа с помощью API YooKassa
    logger.info(payment_info)
    product = "TelegramaMaster 2.0"
    if payment_info.status == "succeeded":  # Обработка статуса платежа
        payment_status = "succeeded"
        date = payment_info.captured_at
        logger.info(date)
        conn = sqlite3.connect('setting/user_data.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users_pay (user_id, first_name, last_name, username, payment_info,
                                                                product, date, payment_status)''')
        cursor.execute('''INSERT INTO users_pay (user_id, first_name, last_name, username, payment_info, 
                                                      product, date, payment_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (callback_query.from_user.id,
                        callback_query.from_user.first_name,
                        callback_query.from_user.last_name,
                        callback_query.from_user.username, payment_info.id, product, date, payment_status))
        conn.commit()

        # Создайте файл, который вы хотите отправить
        caption = (f"Платеж на сумму 1000 руб прошел успешно‼️ \n\n"
                   f"Вы можете скачать программу TelegramaMaster 2.0\n\n"
                   f"Для возврата в начальное меню нажмите /start")

        inline_keyboard_markup = start_menu()  # Отправляемся в главное меню
        document = FSInputFile("setting/password/TelegramMaster/TelegramMaster.zip")

        await bot.send_document(chat_id=callback_query.from_user.id, document=document, caption=caption,
                                reply_markup=inline_keyboard_markup)

        result = checking_for_presence_in_the_user_database(callback_query.from_user.id)

        if result is None:
            cursor.execute('INSERT INTO users (id) VALUES (?)', (callback_query.from_user.id,))
            conn.commit()

            await bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Пользователь:\n"
                                                               f"ID {callback_query.from_user.id},\n"
                                                               f"Username: @{callback_query.from_user.username},\n"
                                                               f"Имя: {callback_query.from_user.first_name},\n"
                                                               f"Фамилия: {callback_query.from_user.last_name},\n\n"
                                                               f"Приобрел TelegramMaster 2.0")
    else:
        await bot.send_message(callback_query.message.chat.id, "Payment failed.")


@dp.callback_query(F.data == "delivery")
async def buy(callback_query: types.CallbackQuery, state: FSMContext):
    """Покупка TelegramMaster 2.0"""
    user_id = callback_query.from_user.id
    result = database(user_id)
    if result:
        # Пользователь уже делал покупку
        # Создайте файл, который вы хотите отправить
        document = FSInputFile('setting/password/TelegramMaster/TelegramMaster.zip')
        caption = (f"Вы можете скачать программу TelegramMaster 2.0\n\n"
                   f"Для возврата в начальное меню нажмите /start")  # Отправка ссылки на программу
        # Отправка файла
        inline_keyboard_markup = start_menu_keyboard()  # Отправляемся в главное меню
        await bot.send_document(chat_id=user_id, document=document, caption=caption,
                                reply_markup=inline_keyboard_markup)
    else:  # Пользователь не делал покупку
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        url, payment = payment_yookassa()
        payment_keyboard_key = payment_keyboard(url, payment)
        payment_mes = ("Купить ТelegramMaster 2.0. \n\n"
                       f"Цена на {current_date} — 1000 рублей.\n\n"
                       "Если по какой-либо причине бот не выдал пароль или произошла ошибка платежа, писать: "
                       "@PyAdminRU. 🤖🔒\n\n"
                       "Для возврата в начальное меню, нажмите: /start")
        await bot.send_message(callback_query.message.chat.id, payment_mes, reply_markup=payment_keyboard_key)


@dp.callback_query(F.data == "get_password")
async def get_password(callback: types.CallbackQuery):
    """Обработчик команды /get_password для получения пароля для пользователя"""
    try:
        logger.info(f'Пользователь {callback.from_user.id} {callback.from_user.username} запросил / запросила пароль '
                    f'от TelegramMaster 2.0')
        logger.info(callback.from_user.id)  # Проверка ID пользователя
        user = await bot.get_chat_member(chat_id="@master_tg_d", user_id=callback.from_user.id)  # Проверка подписки
        logger.info(f"User Status: {user.status}")
        if user.status in ['member', 'administrator', 'creator']:
            result = checking_for_presence_in_the_user_database(callback.from_user.id)
            if result:

                current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                url, payment = payment_yookassa_telegram_master()
                payment_keyboard_key = payment_keyboard_password(url, payment)
                payment_mes = ("Получить пароль от ТelegramMaster 2.0. \n\n"
                               f"Цена на {current_date} — 150 рублей.\n\n"
                               "Если по какой-либо причине бот не выдал пароль или произошла ошибка платежа, писать: "
                               "@PyAdminRU. 🤖🔒\n\n"
                               "Для возврата в начальное меню, нажмите: /start")
                await bot.send_message(callback.message.chat.id, payment_mes, reply_markup=payment_keyboard_key)

                await bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Пользователь:\n"
                                                                   f"ID {callback.from_user.id},\n"
                                                                   f"Username: @{callback.from_user.username},\n"
                                                                   f"Имя: {callback.from_user.first_name},\n"
                                                                   f"Фамилия: {callback.from_user.last_name},\n"
                                                                   f"Запросил пароль от TelegramMaster 2.0")
            else:
                text = (
                    "Для того чтобы воспользоваться всеми возможностями бота 🤖, вам необходимо подписаться на канал "
                    "🔗 @master_tg_d и купить TelegramMaster 2.0.\n\n"

                    "Это позволит вам получить самую свежую версию TelegramMaster 2.0 и воспользоваться всеми новыми "
                    "функциями.\n\n"

                    "Если вы ранее уже приобретали TelegramMaster 2.0, но бот 🤖 не выдаёт пароль, обратитесь к "
                    "🔗 @PyAdminRU.")
                await bot.send_message(chat_id=callback.message.chat.id, text=text)  # ID пользователя нет в базе данных
                await bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Пользователь:\n"
                                                                   f"ID {callback.from_user.id},\n"
                                                                   f"Username: @{callback.from_user.username},\n"
                                                                   f"Имя: {callback.from_user.first_name},\n"
                                                                   f"Фамилия: {callback.from_user.last_name},\n"
                                                                   f"Запросил пароль от TelegramMaster 2.0")
        else:
            text = ("Для того чтобы воспользоваться всеми возможностями бота 🤖, вам необходимо подписаться на канал "
                    "🔗 @master_tg_d и купить TelegramMaster 2.0.\n\n"

                    "Это позволит вам получить самую свежую версию TelegramMaster 2.0 и воспользоваться всеми новыми "
                    "функциями.\n\n"

                    "Если вы ранее уже приобретали TelegramMaster 2.0, но бот 🤖 не выдаёт пароль, обратитесь к "
                    "🔗 @PyAdminRU.")
            await bot.send_message(chat_id=callback.message.chat.id, text=text)  # ID пользователя нет в базе данных
            await bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Пользователь:\n"
                                                               f"ID {callback.from_user.id},\n"
                                                               f"Username: @{callback.from_user.username},\n"
                                                               f"Имя: {callback.from_user.first_name},\n"
                                                               f"Фамилия: {callback.from_user.last_name},\n"
                                                               f"Запросил пароль от TelegramMaster 2.0")
    except Exception as e:
        logger.exception(e)


@dp.callback_query(F.data.startswith("payment_pass"))
async def check_payments(callback_query: types.CallbackQuery, state: FSMContext):
    """Проверка платежа 'Пароль обновления: ТelegramMaster 2.0'"""
    split_data = callback_query.data.split("_")
    logger.info(split_data[2])
    payment_info = Payment.find_one(split_data[2])  # Проверьте статус платежа с помощью API YooKassa
    logger.info(payment_info)
    product = "Пароль обновления: ТelegramMaster 2.0"
    if payment_info.status == "succeeded":  # Обработка статуса платежа
        payment_status = "succeeded"
        date = payment_info.captured_at
        logger.info(date)
        conn = sqlite3.connect('setting/user_data.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users_pay (user_id, first_name, last_name, username, payment_info,
                                                                product, date, payment_status)''')
        cursor.execute('''INSERT INTO users_pay (user_id, first_name, last_name, username, payment_info, 
                                                      product, date, payment_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (callback_query.from_user.id,
                        callback_query.from_user.first_name,
                        callback_query.from_user.last_name,
                        callback_query.from_user.username, payment_info.id, product, date, payment_status))
        conn.commit()

        # Создайте файл, который вы хотите отправить
        caption = (f"Платеж на сумму 150 руб прошел успешно‼️ \n\n"
                   f"Вы можете скачать программу TelegramaMaster 2.0\n\n"
                   f"Для возврата в начальное меню нажмите /start")

        inline_keyboard_markup = start_menu_keyboard()  # Отправляемся в главное меню
        document = FSInputFile("setting/password/TelegramMaster/password.txt")

        await bot.send_document(chat_id=callback_query.from_user.id, document=document, caption=caption,
                                reply_markup=inline_keyboard_markup)

        result = checking_for_presence_in_the_user_database(callback_query.from_user.id)

        if result is None:
            cursor.execute('INSERT INTO users (id) VALUES (?)', (callback_query.from_user.id,))
            conn.commit()

            await bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Пользователь:\n"
                                                               f"ID {callback_query.from_user.id},\n"
                                                               f"Username: @{callback_query.from_user.username},\n"
                                                               f"Имя: {callback_query.from_user.first_name},\n"
                                                               f"Фамилия: {callback_query.from_user.last_name},\n\n"
                                                               f"Приобрел пароль от TelegramMaster 2.0")
    else:
        await bot.send_message(callback_query.message.chat.id, "Payment failed.")


def buy_handler():
    """Регистрируем handlers для бота"""
    dp.message.register(buy)
    dp.message.register(check_payment)
    dp.message.register(get_password)
    dp.message.register(check_payments)
