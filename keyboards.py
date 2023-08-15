from telebot import types

import config


def pay_keyboard():

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('💰 Оплачено', callback_data = f'paid'))

    return keyboard


def pay_back_keyboard():

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = f'back'))

    return keyboard


def paid_keyboard():

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('🙋‍♀️ Связаться со мной', url = f'https://t.me/{config.MANAGER_USERNAME}'))

    return keyboard


def enter_name_keyboard():
    return types.ForceReply(input_field_placeholder='Введите Ваши ФИО')


def enter_check_keyboard():
    return types.ForceReply(input_field_placeholder='Чек об оплате')


def enter_photo_keyboard():
    return types.ForceReply(input_field_placeholder='Ваше селфи')


def enter_request_keyboard():
    return types.ForceReply(input_field_placeholder='Ваш запрос')