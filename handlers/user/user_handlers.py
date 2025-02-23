# -*- coding: utf-8 -*-
import datetime  # Дата

from aiogram import F
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from loguru import logger

from db.settings_db import save_user_activity, add_user_to_db, is_user_in_db
from keyboards.user_keyboards import greeting_keyboards  # Клавиатуры поста приветствия
from messages.messages import greeting_post  # Пояснение для пользователя FAG
from system.dispatcher import dp, bot  # Подключение к боту и диспетчеру пользователя


class SomeState(StatesGroup):
    some_state = State()  # Пример состояния, можно добавить дополнительные состояния


@dp.message(Command("pass"))
async def send_pass(message: types.Message, state: FSMContext):
    """Обработчик команды /pass, для отправки пароля в бота"""
    await message.answer(f'Введите пароль: {message.text}')
    await state.set_state(SomeState.some_state)  # Обновляем состояние


@dp.message(SomeState.some_state)
async def greeting(message: types.Message, state: FSMContext):
    """Обработчик состояния some_state, он же пост приветствия"""
    text = message.text  # Получаем текст сообщения
    # Используем with open для открытия файла с использованием кодека utf-8
    with open("setting/password/TelegramMaster/password.txt", "w", encoding='utf-8') as file:
        file.write(text)
    await state.clear()


@dp.message(Command('start'))
async def greeting(message: types.Message, state: FSMContext):
    """Обработчик команды /start, он же пост приветствия"""
    await state.clear()
    # Получаем текущую дату и время
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Записываем данные пользователя в базу данных

    save_user_activity(message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                       message.from_user.username, current_date)

    print(f'Запустили бота: {message.from_user.id, message.from_user.username, current_date}')
    keyboards_greeting = greeting_keyboards()
    # Клавиатура для Калькулятора цен или Контактов
    await message.answer(
        text=greeting_post,
        reply_markup=keyboards_greeting,
        disable_web_page_preview=True,
        parse_mode="HTML"
    )


@dp.callback_query(F.data == 'start_menu_keyboard')
async def start_menu_no_edit(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик команды /start, он же пост приветствия"""
    await state.clear()
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Получаем текущую дату и время
    # Записываем данные пользователя в базу данных

    save_user_activity(callback_query.from_user.id, callback_query.from_user.first_name,
                       callback_query.from_user.last_name,
                       callback_query.from_user.username, current_date)

    logger.info(f'Запустили бота: {callback_query.from_user.id, callback_query.from_user.username, current_date}')
    keyboards_greeting = greeting_keyboards()
    await bot.send_message(callback_query.message.chat.id, greeting_post, reply_markup=keyboards_greeting,
                           parse_mode="HTML", )


@dp.message(Command('id'))
async def process_id_command(message: types.Message):
    """Обработчик команды /id"""
    try:
        user_id = int(message.text.split()[1])
        result = is_user_in_db(user_id)  # Запись ID в базу данных
        if result is None:
            add_user_to_db(user_id)
            await message.reply(f"ID {user_id} успешно записан в базу данных.")
        else:
            await message.reply(f"ID {user_id} уже существует в базе данных.")
    except (IndexError, ValueError):
        await message.reply("Используйте команду /id followed by ваш ID.")
    except Exception as error:
        logger.exception(error)


def greeting_handler():
    dp.message.register(greeting)
    dp.message.register(process_id_command)
