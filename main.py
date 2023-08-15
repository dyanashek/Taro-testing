import telebot
import threading

import config
import text
import functions
import keyboards


bot = telebot.TeleBot(config.TELEGRAM_TOKEN, disable_notification=True)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(chat_id=message.chat.id,
                    text=text.MAIN_TEXT,
                    reply_markup=keyboards.pay_keyboard(),
                    parse_mode='Markdown',
                    )
            

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(chat_id=message.chat.id,
                     text=text.HELP,
                     parse_mode='Markdown',
                     )


@bot.message_handler(commands=['cancel'])
def start_message(message):
    user_id = message.from_user.id
    functions.delete_user(user_id)

    bot.send_message(chat_id=message.chat.id,
                    text=text.MAIN_TEXT,
                    reply_markup=keyboards.pay_keyboard(),
                    parse_mode='Markdown',
                    )
    

@bot.callback_query_handler(func = lambda call: True)
def callback_query(call):
    """Handles queries from inline keyboards."""

    # getting message's and user's ids
    message_id = call.message.id
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    user_username = call.from_user.username

    call_data = call.data.split('_')
    query = call_data[0]

    if query == 'paid':
        if user_username:
            functions.delete_user(user_id)
            functions.add_user(user_id, user_username)
            
            functions.update_field(user_id, 'input_data', 'name')

            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass

            bot.send_message(chat_id=chat_id,
                             text=text.REQUEST_NAME + text.CANCEL_MESSAGE,
                             reply_markup=keyboards.enter_name_keyboard(),
                             parse_mode='Markdown',
                             )

        else:
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.NO_USERNAME,
                                  )

            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.pay_back_keyboard(),
                                          )

        
@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    input = functions.get_field_info(user_id, 'input')
    input_data = functions.get_field_info(user_id, 'input_data')

    if input and input_data == 'name':
        functions.update_field(user_id, 'name', message.text)
        functions.update_field(user_id, 'input_data', 'check')

        bot.send_message(chat_id=chat_id,
                            text=text.REQUEST_CHECK + text.CANCEL_MESSAGE,
                            reply_markup=keyboards.enter_check_keyboard(),
                            parse_mode='Markdown',
                            )

    elif input and input_data == 'request':
        functions.update_field(user_id, 'request', message.text)
        functions.update_field(user_id, 'input', False)

        threading.Thread(daemon=True, 
                         target=functions.handle_payment,
                         args=(user_id,),
                         ).start()

        bot.send_message(chat_id=chat_id,
                         text=text.PAID,
                         reply_markup=keyboards.paid_keyboard(),
                         )

    else:
        bot.send_message(chat_id=chat_id,
                         text=text.NO_INPUT,
                         reply_markup=keyboards.paid_keyboard(),
                         parse_mode='Markdown',
                         )


@bot.message_handler(content_types=['document'])
def handle_voice(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    input = functions.get_field_info(user_id, 'input')
    input_data = functions.get_field_info(user_id, 'input_data')

    if input and input_data == 'check':

        functions.update_check(user_id, message.document.file_id, 'document')
        functions.update_field(user_id, 'input_data', 'photo')

        bot.send_message(chat_id=chat_id,
                             text=text.REQUEST_PHOTO + text.CANCEL_MESSAGE,
                             reply_markup=keyboards.enter_photo_keyboard(),
                             parse_mode='Markdown',
                             )
    
    elif input and input_data == 'photo':
        bot.send_message(chat_id=chat_id,
                             text=text.WRONG_FORMAT,
                             parse_mode='Markdown',
                             )

    else:
        bot.send_message(chat_id=chat_id,
                         text=text.NO_INPUT,
                         reply_markup=keyboards.paid_keyboard(),
                         parse_mode='Markdown',
                         )


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    input = functions.get_field_info(user_id, 'input')
    input_data = functions.get_field_info(user_id, 'input_data')

    if input and input_data == 'check':

        functions.update_check(user_id, message.photo[-1].file_id, 'photo')
        functions.update_field(user_id, 'input_data', 'photo')

        bot.send_message(chat_id=chat_id,
                            text=text.REQUEST_PHOTO + text.CANCEL_MESSAGE,
                            reply_markup=keyboards.enter_photo_keyboard(),
                            parse_mode='Markdown',
                            )
        
    elif input and input_data == 'photo':
        functions.update_photo(user_id, message.photo[-1].file_id)
        functions.update_field(user_id, 'input_data', 'request')

        bot.send_message(chat_id=chat_id,
                            text=text.REQUEST_REQUEST + text.CANCEL_MESSAGE,
                            reply_markup=keyboards.enter_request_keyboard(),
                            parse_mode='Markdown',
                            )
    
    else:
        bot.send_message(chat_id=chat_id,
                         text=text.NO_INPUT,
                         reply_markup=keyboards.paid_keyboard(),
                         parse_mode='Markdown',
                         )


if __name__ == '__main__':
    bot.polling(timeout=80)
    # while True:
    #     try:
    #         bot.polling()
    #     except:
    #         pass
