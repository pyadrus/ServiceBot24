from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def purchasing_a_program_setup_service(url, id_pay) -> InlineKeyboardMarkup:
    """Клавиатура оплаты за настройку программного обеспечения"""
    rows = [
        [
            InlineKeyboardButton(text="💳 Оплатить 500 руб.", url=url),
            InlineKeyboardButton(text='Проверить оплату', callback_data=f"check_service_{id_pay}"),
        ],

        [InlineKeyboardButton(text="💳 Оплатить 500 руб. (Крипта)", callback_data=f"payment_crypta_pas_training_handler")],

        [InlineKeyboardButton(text='В начальное меню', callback_data='start_menu')],
    ]

    payment_keyboard_key = InlineKeyboardMarkup(inline_keyboard=rows)

    return payment_keyboard_key
