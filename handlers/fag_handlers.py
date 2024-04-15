from aiogram import types, F
from aiogram.fsm.context import FSMContext

from system.dispatcher import bot, dp

fag_post = ("<i>Основные функции бота 🤖</i>\n\n"
            "<b>🔧 Обратная связь и обновления:</b><code> Если у вас есть вопросы, предложения или вы обнаружили "
            "ошибку, не стесняйтесь обращаться через этого 🤖 бота. Я ценю вашу обратную связь и стремлюсь сделать "
            "мои продукты еще лучше.</code>\n\n"
            "<b>🔑 Получение пароля для обновлений:</b><code> 🤖 Бот также предоставит вам пароль для доступа к "
            "последним обновлениям моих программ. Просто запросите пароль, и 🤖 бот обеспечит вас всей необходимой "
            "информацией.</code>\n\n"
            "<b>📁 Отправка файлов с ошибками:</b><code> Если вы столкнулись с какой-либо проблемой или ошибкой, "
            "вы можете отправить файл с описанием ситуации (log файл). 🤖 Бот примет этот файл и передаст его "
            "мне</code> @PyAdminRU <code>для анализа.</code>\n\n"
            "<b>💳 Оплата услуг и продуктов:</b><code> Через 🤖 бота вы можете легко и удобно оплатить услуги, "
            "оплатить услуги за сервер или купить программу. Просто следуйте инструкциям, предоставленным 🤖 "
            "ботом.</code>\n\n"
            "<b>🙏 Благодарность:</b><code> Я ценю каждого пользователя. Если вы хотите поделиться своей "
            "благодарностью или положительным опытом использования моих продуктов, пожалуйста, делитесь своими "
            "впечатлениями с 🤖 ботом.</code>\n\n"
            "Для возврата нажмите на /start")


# @dp.callback_query_handler(lambda c: c.data == "fag")
@dp.callback_query(F.data == "fag")
async def fag_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.message.chat.id, fag_post)


def fag_register_message_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(fag_handler)
