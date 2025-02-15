# -*- coding: utf-8 -*-
import base64
import datetime  # Дата
import hashlib
import json
import uuid

import aiohttp
from aiogram import types, F
from aiogram.types import FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger  # Логирование с помощью loguru

from db.settings_db import checking_for_presence_in_the_user_database, save_payment_info, add_user_if_not_exists
from handlers.payments.products_goods_services import password_TelegramMaster
from keyboards.user_keyboards import start_menu
from setting import settings
from system.dispatcher import bot, dp, ADMIN_CHAT_ID


async def make_request(url: str, invoice_data: dict):
    encoded_data = base64.b64encode(
        json.dumps(invoice_data).encode("utf-8")
    ).decode("utf-8")
    signature = hashlib.md5(f"{encoded_data}{settings.CRYPTOMUS_API_KEY}".
                            encode("utf-8")).hexdigest()

    async with aiohttp.ClientSession(headers={
        "merchant": settings.CRYPTOMUS_MERCHANT_ID,
        "sign": signature,
    }) as session:
        async with session.post(url=url, json=invoice_data) as response:
            if not response.ok:
                raise ValueError(response.reason)

            return await response.json()


# Обработчик для создания счета и отправки кнопки "Проверить оплату"
@dp.callback_query(F.data == "payment_crypta_pas")
async def buy_handler(callback_query: types.CallbackQuery):
    """Оплата пароля TelegramMaster 2.0 криптой"""

    # Создаем счет для оплаты
    invoice_data = await make_request(
        url="https://api.cryptomus.com/v1/payment",
        invoice_data={
            "amount": f"{password_TelegramMaster}",
            "currency": "RUB",
            "order_id": str(uuid.uuid4())
        },
    )
    logger.info(f"Счет для оплаты криптовалютой: {invoice_data}")
    # Создаем кнопку "Проверить оплату"
    check_payment_button = InlineKeyboardButton(
        text="Проверить оплату",
        callback_data=f"check_paymentPAS_{invoice_data['result']['uuid']}"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[check_payment_button]])

    # Отправляем сообщение с кнопкой
    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=f"💳 <b>Счет для оплаты криптовалютой</b> 💳\n\n"
             f"🌐 Вы собираетесь получить пароль от <b>TelegramMaster 2.0</b>. Пожалуйста, воспользуйтесь ссылкой ниже для оплаты:\n"
             f"🔗 <a href='{invoice_data['result']['url']}'>Перейти к оплате</a>\n\n"
             f"⚠️ <b>Важная информация:</b> после завершения платежа нажмите кнопку 'Проверить оплату'.\n"
             f"❗️ Обратите внимание, что возврат денежных средств после оплаты криптовалютой невозможен.\n\n"
             f"💡 Если у вас возникнут вопросы, не стесняйтесь обращаться к нам. Спасибо за доверие! 🙌",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


# Обработчик для кнопки "Проверить оплату"
@dp.callback_query(F.data.startswith("check_paymentPAS_"))
async def check_payment_handler(callback_query: types.CallbackQuery):
    """Ручная проверка статуса оплаты"""
    invoice_uuid = callback_query.data.split("_")[2]  # Извлекаем UUID счета из callback_data
    logger.info(f"Проверка статуса оплаты по UUID: {invoice_uuid}")
    # Проверяем статус оплаты
    try:
        invoice_data = await make_request(
            url="https://api.cryptomus.com/v1/payment/info",
            invoice_data={"uuid": invoice_uuid},
        )

        if invoice_data['result']['payment_status'] in ('paid', 'paid_over'):
            # Если оплата прошла успешно
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            logger.info(date)
            invoice_json = json.dumps(invoice_data)  # Преобразуем словарь в строку JSON

            # Запись в базу данных пользователя, который оплатил счет в крипте
            save_payment_info(callback_query.from_user.id, callback_query.from_user.first_name,
                              callback_query.from_user.last_name, callback_query.from_user.username, invoice_json,
                              "Пароль обновления: TelegramMaster 2.0", date, "succeeded")

            # Отправляем файл и сообщение об успешной оплате
            caption = (f"Платеж на сумму {password_TelegramMaster} руб прошел успешно‼️ \n\n"
                       f"Вы можете скачать программу TelegramMaster 2.0\n\n"
                       f"Для возврата в начальное меню нажмите /start")

            inline_keyboard_markup = start_menu()  # Отправляемся в главное меню
            document = FSInputFile("setting/password/TelegramMaster/password.txt")

            await bot.send_document(chat_id=callback_query.from_user.id, document=document, caption=caption,
                                    reply_markup=inline_keyboard_markup)

            # Проверяем наличие пользователя в базе данных
            result = checking_for_presence_in_the_user_database(callback_query.from_user.id)

            if result is None:
                add_user_if_not_exists(callback_query.from_user.id)

                await bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Пользователь:\n"
                                                                   f"ID {callback_query.from_user.id},\n"
                                                                   f"Username: @{callback_query.from_user.username},\n"
                                                                   f"Имя: {callback_query.from_user.first_name},\n"
                                                                   f"Фамилия: {callback_query.from_user.last_name},\n\n"
                                                                   f"Приобрел пароль от TelegramMaster 2.0 (криптой)")
        else:
            # Если оплата еще не прошла
            await bot.send_message(
                chat_id=callback_query.message.chat.id,
                text="❌ Платеж еще не оплачен. Пожалуйста, завершите оплату и нажмите кнопку 'Проверить оплату' еще раз."
            )

    except Exception as e:
        # Обработка ошибок
        logger.error(f"Ошибка при проверке оплаты: {e}")
        await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text="⚠️ Произошла ошибка при проверке оплаты. Пожалуйста, попробуйте позже."
        )


def register_cryptomus_password():
    """Регистрируем handlers для бота"""
    dp.message.register(buy_handler)
