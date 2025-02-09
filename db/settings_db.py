from .database import connect_db
from loguru import logger


def read_amount_db():
    """Функция для получения суммы из базы данных"""
    try:
        conn = connect_db()  # Инициализация базы данных SQLite
        cursor = conn.cursor()
        cursor.execute('''SELECT amount FROM settings''')
        result = cursor.fetchone()
        conn.close()
        return result[0]
    except Exception as e:
        logger.exception(f"Ошибка при чтении базы данных: {e}")


def clear_amount():
    """Функция для очистки суммы в базе данных"""
    try:
        conn = connect_db()  # Инициализация базы данных SQLite
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM settings''')
        conn.commit()
        conn.close()
    except Exception as e:
        logger.exception(f"Ошибка при очистке базы данных: {e}")


def checking_for_presence_in_the_user_database(user_id):
    # Инициализация базы данных SQLite
    conn = connect_db()  # Инициализация базы данных SQLite
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY)')
    # Проверка наличия ID в базе данных
    cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    return result


def writing_to_the_database_about_a_new_user(chat_id, chat_title, user_id, username, first_name, last_name, date_now):
    """Запись данных о новом пользователе"""
    # Записываем данные в базу данных
    conn = connect_db()  # Инициализация базы данных SQLite
    cursor = conn.cursor()
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS group_members (chat_id, chat_title, user_id, username, first_name, last_name, "
        "date_joined)"
    )
    cursor.execute(
        f"INSERT INTO group_members (chat_id, chat_title, user_id, username, first_name, last_name, date_joined) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (chat_id, chat_title, user_id, username, first_name, last_name, date_now)
    )
    conn.commit()
    conn.close()


if __name__ == '__main__':
    read_amount_db()
    clear_amount()
