import telebot
from telebot import types
import requests
import json

bot = telebot.TeleBot('6803479333:AAH-q47fG_ICMIKEfmAn-mtZZ2oi6al9mr0')
user_state = {}

def get_general_data():
    try:
        response = requests.get('https://math-ege.sdamgia.ru/newapi/general')
        response.raise_for_status()
        return json.loads(response.content)
    except Exception as e:
        bot.send_message(chat_id, f"Произошла ошибка при получении данных: {str(e)}")
        return None

@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = "Привет! Я бот для работы с заданиями по математике ЕГЭ. Выбери интересующий раздел, чтобы начать."
    layout = types.InlineKeyboardMarkup([[types.InlineKeyboardButton('Начать', callback_data='start')]])
    bot.send_message(message.chat.id, welcome_text, reply_markup=layout)

@bot.callback_query_handler(func=lambda callback: True)
def callback_handler(callback):
    chat_id = callback.message.chat.id
    prev_message_id = callback.message.message_id - 1
    
    try:
        bot.edit_message_text(chat_id=chat_id, message_id=prev_message_id, text="Новый текст сообщения или что-то еще")
    except Exception as e:
        pass

    if callback.data == 'start':
        layout = types.InlineKeyboardMarkup([
            [types.InlineKeyboardButton('Темы', callback_data='themes'),
             types.InlineKeyboardButton('Справка', callback_data='button2'),
             types.InlineKeyboardButton('Справочник', callback_data='reference')],
        ])
        user_state[chat_id] = 'start'
        bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='<b>Меню</b>', reply_markup=layout, parse_mode='html')
    
    elif callback.data in ['themes', 'button2', 'reference']:
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=prev_message_id, text=f"Новый текст для {callback.data} или что-то еще")
        except Exception as e:
            pass

        if callback.data == 'button2':
            instruction_text = """<b>Инструкции по использованию бота:</b>
            1. Запуск бота: Нажмите кнопку "Пуск" или другую команду, предложенную ботом, чтобы активировать его.
            2. Ознакомьтесь с командами: Большинство ботов поддерживают определенные команды. Например, "/help", "/info" или "/commands" для получения списка доступных команд."""
            layout = types.InlineKeyboardMarkup([[types.InlineKeyboardButton('Назад', callback_data='back')]])
            user_state[chat_id] = 'button2'
            bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text=instruction_text, reply_markup=layout, parse_mode='html')
        else:
            data_dict = {'themes': '<b>Темы</b>', 'reference': '<b>Справочник:</b>'}
            text = f"{data_dict.get(callback.data, '')}\nЗдесь вы можете найти полезные материалы и ссылки для подготовки к математике ЕГЭ."
            layout = types.InlineKeyboardMarkup([[types.InlineKeyboardButton('Назад', callback_data='back')]])
            user_state[chat_id] = callback.data
            bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text=text, reply_markup=layout, parse_mode='html')
    
    elif callback.data == 'back':
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=prev_message_id, text="Новый текст для справочного сообщения или чего-то еще")
        except Exception as e:
            pass

        if user_state.get(chat_id):
            menu_dict = {'themes': 'Темы', 'button2': 'Справка', 'reference': 'Справочник'}
            layout = types.InlineKeyboardMarkup([
                [types.InlineKeyboardButton(menu_dict.get(user_state[chat_id], 'Темы'), callback_data=user_state[chat_id])],
                [types.InlineKeyboardButton('Справка', callback_data='button2'),
                 types.InlineKeyboardButton('Справочник', callback_data='reference')],
            ])
            user_state[chat_id] = 'start'
            bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='<b>Меню</b>', reply_markup=layout, parse_mode='html')

    else:
        url = f'https://math-ege.sdamgia.ru/test?theme={callback.data}'
        bot.send_message(chat_id, f'<b>{callback.data}</b>', parse_mode='html')
        bot.send_message(chat_id, f'<a href="{url}">Link to the site</a>', parse_mode='html', disable_web_page_preview=True)

bot.polling(none_stop=True)
