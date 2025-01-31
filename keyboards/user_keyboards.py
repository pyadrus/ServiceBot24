from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from handlers.payments.products_goods_services import password_TelegramMaster, TelegramMaster


def payment_keyboard_password(url, id_pay) -> InlineKeyboardMarkup:
    """Клавиатура оплаты пароля"""
    rows = [
        [InlineKeyboardButton(text=f"💳 Оплатить {password_TelegramMaster} руб. (Юкасса)", url=url)],
        [InlineKeyboardButton(text='Проверить оплату (Юкасса)', callback_data=f"payment_pass_{id_pay}")],

        [InlineKeyboardButton(text=f"💳 Оплатить {password_TelegramMaster} руб. (Крипта)", callback_data=f"payment_crypta_pas")],
    ]

    payment_keyboard_password_key = InlineKeyboardMarkup(inline_keyboard=rows)

    return payment_keyboard_password_key


def payment_keyboard(url, id_pay) -> InlineKeyboardMarkup:
    """Клавиатура оплаты TelegramMaster"""
    rows = [
        [InlineKeyboardButton(text=f"💳 Оплатить {TelegramMaster} руб. (Юкасса)", url=url)],
        [InlineKeyboardButton(text='Проверить оплату (Юкасса)', callback_data=f"check_payment_{id_pay}")],

        [InlineKeyboardButton(text=f"💳 Оплатить {TelegramMaster} руб. (Крипта)", callback_data=f"payment_crypta_pas_program")],
    ]

    payment_keyboard_key = InlineKeyboardMarkup(inline_keyboard=rows)

    return payment_keyboard_key


def greeting_keyboards() -> InlineKeyboardMarkup:
    """Клавиатуры поста приветствия 👋(Получения пароля от проектов, обратная связь, отправка логов)"""

    rows = [
        [InlineKeyboardButton(text='📥 Пароль от TelegramMaster 2.0', callback_data='get_password')],
        [InlineKeyboardButton(text='📤 Пароль от Telegram_Commentator_GPT', callback_data='get_password_tg_com')],
        [InlineKeyboardButton(text='Купить TelegramMaster 2.0', callback_data='delivery')],
        [InlineKeyboardButton(text='Оплатить настройку ПО', callback_data='purchasing_a_program_setup_service')],
        [
            InlineKeyboardButton(text='📨 Отправить log файл', callback_data='sending_file'),
            InlineKeyboardButton(text='📱 Мои контакты', callback_data='reference')
        ],
        [InlineKeyboardButton(text='⁉️ FAG', callback_data='fag')],
    ]
    inline_keyboard_markup = InlineKeyboardMarkup(inline_keyboard=rows)

    return inline_keyboard_markup


def start_menu() -> InlineKeyboardMarkup:
    """Клавиатура начального меню"""
    rows = [
        [InlineKeyboardButton(text='В начальное меню', callback_data='start_menu')],
    ]
    inline_keyboard_markup = InlineKeyboardMarkup(inline_keyboard=rows)

    return inline_keyboard_markup


def start_menu_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура начального меню, не обновляемое сообщение"""
    rows = [
        [InlineKeyboardButton(text='В начальное меню', callback_data='start_menu_keyboard')],
    ]
    inline_keyboard_markup = InlineKeyboardMarkup(inline_keyboard=rows)

    return inline_keyboard_markup


if __name__ == '__main__':
    greeting_keyboards()
