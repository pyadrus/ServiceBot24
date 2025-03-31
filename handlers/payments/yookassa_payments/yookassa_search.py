# -*- coding: utf-8 -*-

from aiogram import types, F
from aiogram.types import FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger  # Логирование с помощью loguru
from yookassa import Payment

from db.settings_db import save_payment_info, add_user_if_not_exists, is_user_in_db
from handlers.payment_yookassa import payment_yookassa_com
from handlers.payments.products_goods_services import TelegramMaster_Search_GPT
from keyboards.user_keyboards import start_menu
from messages.messages import message_payment
from system.dispatcher import bot, dp, ADMIN_CHAT_ID

# Оплата TelegramMaster-Search-GPT

product = "TelegramMaster-Search-GPT"


@dp.callback_query(F.data == "payment_yookassa_Search_GPT")
async def payment_yookassa_TelegramMaster_Search_GPT(callback_query: types.CallbackQuery):
    """Отправка ссылки для оплаты TelegramMaster_Commentator"""
    try:
        payment_url, payment_id = payment_yookassa_com(
            description_text=f"Оплата: {product}",  # Текст описания товара
            product_price=TelegramMaster_Search_GPT  # Цена товара в рублях
        )
        messages = message_payment(product, payment_url)
        # Создаем клавиатуру с кнопкой для проверки оплаты и возврата в меню
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='✅ Проверить оплату (Юкасса)',
                                  callback_data=f"check_pay_TMSearchGPT_{payment_id}")],
            [InlineKeyboardButton(text='🏠 В начальное меню', callback_data='start_menu_keyboard')],
        ])
        await bot.send_message(chat_id=callback_query.from_user.id, text=messages, reply_markup=keyboard,
                               parse_mode="HTML")
    except Exception as e:
        logger.exception(e)


@dp.callback_query(F.data.startswith("check_pay_TMSearchGPT"))
async def check_pay_TelegramMaster_Search_GPT(callback_query: types.CallbackQuery):
    """"Проверка платежа TelegramMaster_Commentator"""
    split_data = callback_query.data.split("_")
    logger.info(split_data[2])
    payment_info = Payment.find_one(split_data[2])  # Проверьте статус платежа с помощью API yookassa
    logger.info(payment_info)

    if payment_info.status == "succeeded":  # Обработка статуса платежа
        payment_status = "succeeded"
        date = payment_info.captured_at

        # Запись в базу данных пользователя, который оплатил счет в рублях
        save_payment_info(callback_query.from_user.id, callback_query.from_user.first_name,
                          callback_query.from_user.last_name, callback_query.from_user.username, payment_info.id,
                          product, date, payment_status)

        # Создайте файл, который вы хотите отправить
        caption = (f"Платеж на сумму {TelegramMaster_Search_GPT} руб прошел успешно‼️ \n\n"
                   f"Вы можете скачать программу {product}\n\n"
                   f"Для возврата в начальное меню нажмите /start")

        inline_keyboard_markup = start_menu()  # Отправляемся в главное меню
        document = FSInputFile("setting/password/TelegramMaster_Search_GPT/password.txt")

        await bot.send_document(chat_id=callback_query.from_user.id, document=document, caption=caption,
                                reply_markup=inline_keyboard_markup)

        result = is_user_in_db(callback_query.from_user.id)

        if result is None:
            add_user_if_not_exists(callback_query.from_user.id)

            await bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Пользователь:\n"
                                                               f"ID {callback_query.from_user.id},\n"
                                                               f"Username: @{callback_query.from_user.username},\n"
                                                               f"Имя: {callback_query.from_user.first_name},\n"
                                                               f"Фамилия: {callback_query.from_user.last_name},\n\n"
                                                               f"Приобрел TelegramMaster_Commentator")
    else:
        await bot.send_message(callback_query.message.chat.id, "Payment failed.")


def register_yookassa_TelegramMaster_Search_GPT():
    """Регистрируем handlers для бота"""
    # Оплата TelegramMaster_Search_GPT
    dp.callback_query.register(check_pay_TelegramMaster_Search_GPT)
    dp.callback_query.register(payment_yookassa_TelegramMaster_Search_GPT)
