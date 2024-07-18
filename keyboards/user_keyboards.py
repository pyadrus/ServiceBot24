from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def payment_keyboard_password(url, id_pay) -> InlineKeyboardMarkup:
    """Клавиатура оплаты"""
    rows = [
        [InlineKeyboardButton(text="💳 Оплатить 150 руб.", url=url)],
        [InlineKeyboardButton(text='Проверить оплату', callback_data=f"payment_pass_{id_pay}")],
    ]

    payment_keyboard_password_key = InlineKeyboardMarkup(inline_keyboard=rows)

    return payment_keyboard_password_key


def payment_keyboard(url, id_pay) -> InlineKeyboardMarkup:
    """Клавиатура оплаты"""
    rows = [
        [InlineKeyboardButton(text="💳 Оплатить 1000 руб.", url=url)],
        [InlineKeyboardButton(text='Проверить оплату', callback_data=f"check_payment_{id_pay}")],
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
