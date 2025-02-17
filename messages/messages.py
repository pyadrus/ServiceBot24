# -*- coding: utf-8 -*-
greeting_post = ("<b>👋 Добро пожаловать в мой 🤖 Telegram-бот!</b>\n\n"
                 "<i>Рад приветствовать вас в универсальном 🤖 боте, готовом помочь во всех вопросах, связанных с моими "
                 "продуктами и услугами.</i>\n\n"
                 "<i>Благодарю за использование моих услуг! Независимо от того, с каким запросом вы обратитесь, я всегда "
                 "готов оказать вам поддержку. Свяжитесь со мной по @PyAdminRU.</i>")

message_text_faq = ("📢 Вы можете связаться со мной в следующих социальных сетях:\n\n"
                    "Telegram: <a href='https://t.me/PyAdminRU'>@PyAdminRU</a>\n"
                    "VKontakte (VK): <a href='https://vk.com/zh.vitaliy'>@zh.vitaliy</a>\n\n"
                    "🚀 Мой основной проект в Telegram:\n"
                    "<a href='https://t.me/master_tg_d'>@master_tg_d</a>\n"
                    "Мой основной проект в Вконтакте (VK):\n"
                    "<a href='https://vk.com/tg_smm2'>@tg_smm2</a>\n\n"
                    "Для возврата нажмите на /start")

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


def generate_payment_message_commentator(current_date, password_TelegramMaster_Commentator):
    return ("Получить пароль от TelegramMaster_Commentator. \n\n"
            f"Цена на {current_date} — {password_TelegramMaster_Commentator} рублей.\n\n"
            "Если по какой-либо причине бот не выдал пароль или произошла ошибка платежа, писать: "
            "@PyAdminRU. 🤖🔒\n\n"
            "Для возврата в начальное меню, нажмите: /start")


def generate_payment_message(current_date, password_TelegramMaster):
    return ("Получить пароль от TelegramMaster 2.0. \n\n"
            f"Цена на {current_date} — {password_TelegramMaster} рублей.\n\n"
            "Если по какой-либо причине бот не выдал пароль или произошла ошибка платежа, писать: "
            "@PyAdminRU. 🤖🔒\n\n"
            "Для возврата в начальное меню, нажмите: /start")
