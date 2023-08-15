import sqlite3
import logging
import inspect
import gspread
import datetime
import telebot

import keyboards
import config

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

service_acc = gspread.service_account(filename='service_account.json')
sheet = service_acc.open(config.SPREAD_NAME)
work_sheet = sheet.worksheet(config.LIST_NAME)


def get_all_info(user_id):
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    info = cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,)).fetchall()[0]

    cursor.close()
    database.close()

    return info


def add_user(user_id, user_username):
    """Adds a new user to database."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute(f'''
            INSERT INTO users (user_id, username)
            VALUES ("{user_id}", "{user_username}")
            ''')

    database.commit()
    cursor.close()
    database.close()


def update_field(user_id, field, value):
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute(f'''UPDATE users
                    SET {field}=?
                    WHERE user_id=?
                    ''', (value, user_id,))

    database.commit()
    cursor.close()
    database.close()


def get_field_info(user_id, field):
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    info = cursor.execute(f'''SELECT {field}
                            FROM users 
                            WHERE user_id=?
                            ''', (user_id,)).fetchall()[0][0]
    
    cursor.close()
    database.close

    return info


def delete_user(user_id):
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute('DELETE FROM users WHERE user_id=?', (user_id,))

    database.commit()
    cursor.close()
    database.close()


def update_check(user_id, check, check_type):
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute(f'''UPDATE users
                    SET check_id=?, check_type=?
                    WHERE user_id=?
                    ''', (check, check_type, user_id,))

    database.commit()
    cursor.close()
    database.close()


def update_photo(user_id, photo):
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute(f'''UPDATE users
                    SET photo=?
                    WHERE user_id=?
                    ''', (photo, user_id,))

    database.commit()
    cursor.close()
    database.close()


def handle_payment(user_id):
    user_info = get_all_info(user_id)

    username = user_info[2]
    name = user_info[3]
    check_id = user_info[4]
    check_type = user_info[5]
    photo = user_info[6]
    request = user_info[7]

    transfer_to_google_sheets_payments(user_id, username, name, request)

    try:
        bot.send_message(chat_id=config.MANAGER_ID,
                         text=f'Пользователь @{username} оплатил услугу *тестовый расклад*.',
                         parse_mode='Markdown',
                         )
        
        check_message = bot.send_message(chat_id=config.MANAGER_ID,
                         text=f'Платежный документ пользователя @{username}:',
                         )
        
        if check_type == 'document':
            bot.send_document(chat_id=config.MANAGER_ID,
                              document=check_id,
                              reply_to_message_id=check_message.id,
                              )
        else:
            bot.send_photo(chat_id=config.MANAGER_ID,
                            photo=check_id,
                            reply_to_message_id=check_message.id,
                            )
            
        bot.send_photo(chat_id=config.MANAGER_ID,
                            photo=photo,
                            caption=f'Селфи пользователя @{username}.',
                            )
        
        request_message = bot.send_message(chat_id=config.MANAGER_ID,
                         text=f'Запрос пользователя @{username}:',
                         )
        

        bot.send_message(chat_id=config.MANAGER_ID,
                            text=request,
                            reply_to_message_id=request_message.id,
                            )

    except:
        pass


def get_row():
    """Gets the number of first empty row in table."""

    return len(work_sheet.col_values(1)) + 1


def transfer_to_google_sheets_payments(user_id, username, name, request):
    """Transfers data to google sheets."""

    row = get_row()

    fill_date = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(hours=3), "%d.%m.%Y %H:%M")

    try:
        work_sheet.update(f'A{row}:E{row}', [[user_id, username, name, request, fill_date]])
    except:
        pass