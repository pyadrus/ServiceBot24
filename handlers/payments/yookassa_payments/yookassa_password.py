import json
import sqlite3

from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger  # Логирование с помощью loguru
from yookassa import Configuration, Payment

from db.settings_db import checking_for_presence_in_the_user_database
from handlers.payments.products_goods_services import password_TelegramMaster
from keyboards.user_keyboards import start_menu_keyboard
from system.dispatcher import bot, dp, ACCOUNT_ID, SECRET_KEY, ADMIN_CHAT_ID


def payment_yookassa_telegram_master():
    """Оплата yookassa"""

    Configuration.account_id = ACCOUNT_ID
    Configuration.secret_key = SECRET_KEY

    description_text = "Пароль обновления: TelegramMaster 2.0"  # Текст описания товара

    payment = Payment.create(
        {"amount": {"value": password_TelegramMaster,  # Сумма товара
                    "currency": "RUB"}, "capture": True,
         "confirmation": {"type": "redirect", "return_url": "https://t.me/h24service_bot"},
         "description": description_text,
         "metadata": {'order_number': '1'},
         "receipt": {"customer": {"email": "zh.vitaliy92@yandex.ru"},
                     "items": [
                         {
                             "description": description_text,  # Название товара
                             "quantity": "1",
                             "amount": {"value": password_TelegramMaster,  # Сумма товара
                                        "currency": "RUB"},  # Сумма и валюта
                             "vat_code": "1"}]}})

    payment_data = json.loads(payment.json())
    payment_id = payment_data['id']
    payment_url = (payment_data['confirmation'])['confirmation_url']
    logger.info(f"Ссылка для оплаты: {payment_url}, ID оплаты {payment_id}")
    return payment_url, payment_id


@dp.callback_query(F.data.startswith("payment_yookassa_password"))
async def payment_url_handler(callback_query: types.CallbackQuery):
    """Отправка ссылки для оплаты пароля от TelegramMaster 2.0"""
    payment_url, payment_id = payment_yookassa_telegram_master()

    messages = (
        "💳 <b>Оплата пароля от TelegramMaster 2.0</b>\n\n"
        f"Для оплаты перейдите по ссылке: {payment_url}\n\n"
        "🔔 <b>Важно:</b>\n"
        "1. Ссылка действительна <b>9 минут</b>. Если время истекло, зайдите в это меню заново.\n"
        "2. Оплата осуществляется через безопасную платежную систему <b>Юкасса</b>.\n"
        "3. После успешной оплаты вы получите пароль от архива с программой. Архив находится в закрепленном сообщении "
        "на канале https://t.me/+uE6L_wey4c43YWEy.\n\n"
        "🔄 После оплаты нажмите кнопку <b>«Проверить оплату»</b>, чтобы получить доступ к программе."
    )

    # Создаем клавиатуру с кнопкой для проверки оплаты и возврата в меню
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✅ Проверить оплату (Юкасса)', callback_data=f"payment_pass_{payment_id}")],
        [InlineKeyboardButton(text='🏠 В начальное меню', callback_data='start_menu_keyboard')],
    ])

    await bot.send_message(chat_id=callback_query.from_user.id, text=messages, reply_markup=keyboard, parse_mode="HTML")


@dp.callback_query(F.data.startswith("payment_pass"))
async def check_payments(callback_query: types.CallbackQuery, state: FSMContext):
    """Проверка платежа 'Пароль обновления: TelegramMaster 2.0'"""
    split_data = callback_query.data.split("_")
    logger.info(split_data[2])
    payment_info = Payment.find_one(split_data[2])  # Проверьте статус платежа с помощью API YooKassa
    logger.info(payment_info)
    product = "Пароль обновления: TelegramMaster 2.0"
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
        caption = (f"Платеж на сумму {password_TelegramMaster} руб прошел успешно‼️ \n\n"
                   f"Вы можете скачать программу TelegramMaster 2.0\n\n"
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


def register_yookassa_password():
    """Регистрируем handlers для бота"""
    dp.message.register(check_payments)
    dp.message.register(payment_url_handler)
