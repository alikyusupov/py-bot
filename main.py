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
        parsed_data = json.loads(response.content)
        return parsed_data
    except Exception as e:
        bot.send_message(chat_id, f"Произошла ошибка при получении данных: {str(e)}")
        return None

@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = """
    Привет! Я бот для работы с заданиями по математике ЕГЭ. Выбери интересующий раздел, чтобы начать.
    """
    
    layout = types.InlineKeyboardMarkup(
        [
            [
                types.InlineKeyboardButton('Начать', callback_data='start'),
            ],
        ]
    )
    
    msg = bot.send_message(message.chat.id, welcome_text, reply_markup=layout)

@bot.callback_query_handler(func=lambda callback: True)
def callback_handler(callback):
    chat_id = callback.message.chat.id
    
    try:
        bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id - 1, text="Новый текст сообщения или что-то еще")
    except Exception as e:
        pass

    if callback.data == 'start':
        layout = types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton('Темы', callback_data='themes'),
                    types.InlineKeyboardButton('Справка', callback_data='button2'),
                ],
                [
                    types.InlineKeyboardButton('Кодификатор', callback_data='codificator'),
                ],
            ]
        )
        user_state[chat_id] = 'start'
        bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='<b>Меню</b>', reply_markup=layout, parse_mode='html')
    elif callback.data == 'themes':
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id - 1, text="Новый текст сообщения для тем или что-то еще")
        except Exception as e:
            pass

        layout = types.InlineKeyboardMarkup()

        themes_list = [
            'Тема 1', 'Тема 2', 'Тема 3', 'Тема 4', 'Тема 5',
            'Тема 6', 'Тема 7', 'Тема 8', 'Тема 9', 'Тема 10',
            'Тема 11', 'Тема 12', 'Тема 13', 'Тема 14', 'Тема 15',
            'Тема 16', 'Тема 17', 'Тема 18', 'Тема 19', 'Тема 20',
            'Тема 21', 'Тема 22', 'Тема 23', 'Тема 24', 'Тема 25',
            'Тема 26', 'Тема 27', 'Тема 28', 'Тема 29', 'Тема 30',
            'Тема 31', 'Тема 32', 'Тема 33', 'Тема 34', 'Тема 35',
            'Тема 36', 'Тема 37', 'Тема 38', 'Тема 39', 'Тема 40',
            # добавьте остальные темы
        ]

        for theme in themes_list:
            layout.add(types.InlineKeyboardButton(theme, callback_data=f'theme_{theme.lower().replace(" ", "_")}'))

        user_state[chat_id] = 'themes'
        bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='<b>Темы</b>', reply_markup=layout, parse_mode='html')
    elif callback.data == 'button2':
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id - 1, text="New text for the help message or something else")
        except Exception as e:
            pass

        instruction_text = """<b>Инструкции по использованию бота:</b>

        1. Запуск бота:
           • Нажмите кнопку "Пуск" или другую команду, предложенную ботом, чтобы активировать его.

        2. Ознакомьтесь с командами:
           • Большинство ботов поддерживают определенные команды. Например, "/help", "/info" или "/commands" для получения списка доступных команд."""
        layout = types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton('Темы', callback_data='themes'),
                    types.InlineKeyboardButton('Справка', callback_data='button2'),
                ],
                [
                    types.InlineKeyboardButton('Назад', callback_data='back')
                ],
            ]
        )
        user_state[chat_id] = 'button2'
        bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text=instruction_text, reply_markup=layout, parse_mode='html')
    elif callback.data == 'back':
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id - 1, text="New text for the back button message or something else")
        except Exception as e:
            pass

        if chat_id in user_state and user_state[chat_id] == 'themes':
            layout = types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton('Topics', callback_data='themes'),
                        types.InlineKeyboardButton('Help', callback_data='button2'),
                    ],
                ]
            )
            user_state[chat_id] = 'start'
            bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='<b>Main Menu</b>', reply_markup=layout, parse_mode='html')
        elif chat_id in user_state and user_state[chat_id] == 'button2':
            layout = types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton('Темы', callback_data='themes'),
                        types.InlineKeyboardButton('Справка', callback_data='button2'),
                    ],
                ]
            )
            user_state[chat_id] = 'start'
            bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='<b>Main Menu</b>', reply_markup=layout, parse_mode='html')
    elif callback.data == 'codificator':
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id - 1, text="New text for the codificator button message or something else")
        except Exception as e:
            pass

        layout = types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton('Назад', callback_data='back'),
                ],
            ]
        )
        user_state[chat_id] = 'codificator'
        bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='<b>Codificator</b>', reply_markup=layout, parse_mode='html')
    else:
        url = f'https://math-ege.sdamgia.ru/test?theme={callback.data}'
        bot.send_message(chat_id, f'<b>{callback.data}</b>', parse_mode='html')
        bot.send_message(chat_id, f'<a href="{url}">Link to the site</a>', parse_mode='html', disable_web_page_preview=True)

bot.polling(none_stop=True)