import asyncio
import base64
import hashlib
import json
import sqlite3
import uuid

import aiohttp
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from loguru import logger

from setting import settings
from system.dispatcher import dp, form_router


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


async def check_invoice_paid(id: str, message):
    while True:
        invoice_data = await make_request(
            url="https://api.cryptomus.com/v1/payment/info",
            invoice_data={"uuid": id},
        )

        if invoice_data['result']['payment_status'] in ('paid', 'paid_over'):
            await message.answer("Счет оплачен! Спасибо!")
            return
        else:
            logger.info("Счет еще не оплачен")

        await asyncio.sleep(10)


@dp.message(CommandStart())
async def buy_handler(message: Message):

    results = read_amount_db()
    logger.info(results)

    invoice_data = await make_request(
        url="https://api.cryptomus.com/v1/payment",
        invoice_data={
            "amount": f"{results}",
            "currency": "RUB",
            "order_id": str(uuid.uuid4())
        },
    )

    asyncio.create_task(
        check_invoice_paid(invoice_data['result']['uuid'],
                           message=message))

    await message.answer(f"Счет для оплаты: {invoice_data['result']['url']}")


ADMIN_USER_IDS = [535185511]  # Список администраторов


class ServiceCreation(StatesGroup):
    enter_amount = State()


@form_router.message(Command("service_creation"))
async def service_creation_handler(message: Message, state: FSMContext):
    """Обработчик команды для создания услуги (только для админа)"""
    logger.info(message.from_user.id)

    if message.from_user.id in ADMIN_USER_IDS:
        await message.reply("Введите сумму без копеек")
        await state.set_state(ServiceCreation.enter_amount)
    else:
        await message.reply("Вы не админ!")
        return

# Функция для обновления суммы в базе данных
def update_amount_db(amount):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS settings (amount)''')
    cursor.execute('''INSERT INTO settings (amount) VALUES (?)''', (amount,))
    conn.commit()
    conn.close()


def read_amount_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT amount FROM settings''')
    result = cursor.fetchone()
    conn.close()
    return result[0]

def lcear_amount():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM settings''')
    conn.commit()
    conn.close()


@form_router.message(ServiceCreation.enter_amount)
async def update_info(message: Message, state: FSMContext):
    """Обработчик текстовых сообщений для сохранения суммы в базу данных"""
    amount = message.text
    lcear_amount() # Очистка базы данных
    update_amount_db(amount)  # Сохранение суммы в базу данных
    await message.reply("Сумма успешно обновлена в базе данных.")
    await state.clear()