import asyncio
import logging
import sys

from loguru import logger  # https://github.com/Delgan/loguru

from handlers.cryptocurrency_handlers.password_handlers import cry_register_message_handler
from handlers.cryptocurrency_handlers.program_handlers import program_cry_register_message_handler
from handlers.cryptocurrency_handlers.training_handlers import training_cry_register_message_handler
from handlers.fag_handlers import fag_register_message_handler
from handlers.program_service_handlers import buy_handler_program_setup_service
from handlers.sale_of_goods_handlers import buy_handler
from handlers.sending_log_file import sending_log_file_register_handler
from handlers.user_handlers.reference_handlers import register_faq_handler
from handlers.user_handlers.user_handlers import greeting_handler
from system.dispatcher import dp, bot

logger.add("logs/log.log", retention="1 days", enqueue=True)  # Логирование бота


async def main() -> None:
    """Запуск бота https://t.me/h24service_bot"""
    await dp.start_polling(bot)
    # buy_handler_program_admin_service()  # Удаление системных сообщений
    greeting_handler()  # Пост приветствие пользователей бота
    buy_handler()  # Купить Telegram_BOT_SMM
    buy_handler_program_setup_service()  # Оплата настройки ПО
    fag_register_message_handler()  # Помощь по боту
    sending_log_file_register_handler()
    register_faq_handler()  # Регистрация FAQ

    # Оплата Криптой
    cry_register_message_handler() # Покупка пароля TelegramMaster 2.0
    program_cry_register_message_handler() # Покупка TelegramMaster 2.0
    training_cry_register_message_handler() # Покупка 'Помощь в настройке ПО (консультация)'


if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except Exception as e:
        logger.exception(e)
