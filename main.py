# Импорт необходимых библиотек
import telebot
from telebot import types
import requests
import json

# Инициализация токена для бота
bot = telebot.TeleBot('6803479333:AAH-q47fG_ICMIKEfmAn-mtZZ2oi6al9mr0')

# Словарь для отслеживания состояния пользователя
user_state = {}

# Функция для получения общих данных
def get_general_data():
    try:
        response = requests.get('https://math-ege.sdamgia.ru/newapi/general')
        response.raise_for_status()
        parsed_data = json.loads(response.content)
        return parsed_data
    except Exception as e:
        # Обработка ошибок при получении данных
        bot.send_message(chat_id, f"Произошла ошибка при получении данных: {str(e)}")
        return None

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def welcome(message):
    # Приветственный текст и кнопка "Начать"
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

# Обработчик для inline-кнопок
@bot.callback_query_handler(func=lambda callback: True)
def callback_handler(callback):
    chat_id = callback.message.chat.id
    
    try:
        # Попытка изменить текст предыдущего сообщения
        bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id - 1, text="Новый текст сообщения или что-то еще")
    except Exception as e:
        pass

    if callback.data == 'start':
        # Обработка команды "Начать"
        layout = types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton('Темы', callback_data='themes'),
                    types.InlineKeyboardButton('Справка', callback_data='button2'),
                    types.InlineKeyboardButton('Справочник', callback_data='reference'),  # Новая кнопка
                ],
            ]
        )
        user_state[chat_id] = 'start'
        bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='<b>Меню</b>', reply_markup=layout, parse_mode='html')
    # ... (продолжение комментариев)

    elif callback.data == 'themes':
        # Обработка команды "Темы"
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id - 1, text="Новый текст сообщения для тем или что-то еще")
        except Exception as e:
            pass

        # Создание inline-кнопок для списка тем
        layout = types.InlineKeyboardMarkup()
        themes_list = [
            '1.Планиметрия', '2.Векторы', '3.Стереометрия', '4.Начала теории вероятностей', '5.Вероятности сложных событий', 
            '6.Простейшие уравнения', '7.Вычисления и преобразования', '8.Производная и первообразная', '9.Прикладные задачи', 
            '10.Текстовые задачи', '11.Графики функций', '12.Макс и Мин значение функций', '13.Уравнения', '14.Стереометрическая задача', 
            '15.Неравенства', '16.Финансовая математика', '17.Планиметрическая задача', '18.Задача с параметром', '19.Числа и их свойства'
            # ... (добавьте остальные темы)
        ]
        for theme in themes_list:
            layout.add(types.InlineKeyboardButton(theme, callback_data=f'theme_{theme.lower().replace(" ", "_")}'))

        user_state[chat_id] = 'themes'
        bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='<b>Темы</b>', reply_markup=layout, parse_mode='html')
    elif callback.data == 'button2':
        # Обработка команды "Справка"
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id - 1, text="Новый текст для справочного сообщения или чего-то еще")
        except Exception as e:
            pass

        # Текст инструкции и кнопки
        instruction_text = """<b>Инструкции по использованию бота:</b>
        1. Запуск бота: Нажмите кнопку "Пуск" или другую команду, предложенную ботом, чтобы активировать его.
        2. Ознакомьтесь с командами: Большинство ботов поддерживают определенные команды. Например, "/help", "/info" или "/commands" для получения списка доступных команд."""
        layout = types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton('Назад', callback_data='back')
                ],
            ]
        )
        user_state[chat_id] = 'button2'
        bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text=instruction_text, reply_markup=layout, parse_mode='html')
    elif callback.data == 'reference':
        # Обработка команды "Справочник"
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id - 1, text="Выберите тему из справочника:")
        except Exception as e:
            pass

        # Создание inline-кнопок для справочника
        layout = types.InlineKeyboardMarkup()
        reference_themes = [
            '1.Планиметрия', '2.Векторы', '3.Стереометрия', '4.Начала теории вероятностей', '5.Вероятности сложных событий', 
            '6.Простейшие уравнения', '7.Вычисления и преобразования', '8.Производная и первообразная', '9.Прикладные задачи', 
            '10.Текстовые задачи', '11.Графики функций', '12.Макс и Мин значение функций', '13.Уравнения', '14.Стереометрическая задача', 
            '15.Неравенства', '16.Финансовая математика', '17.Планиметрическая задача', '18.Задача с параметром', '19.Числа и их свойства'
            # ... (добавьте остальные темы)
        ]
        for theme in reference_themes:
            layout.add(types.InlineKeyboardButton(theme, callback_data=f'reference_{theme.lower().replace(" ", "_")}'))

        user_state[chat_id] = 'reference'
        bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='<b>Справочник:</b>', reply_markup=layout, parse_mode='html')
    elif callback.data == 'back':
        # Обработка команды "Назад"
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id - 1, text="Новый текст для справочного сообщения или чего-то еще")
        except Exception as e:
            pass

        # Возврат в предыдущее меню
        if chat_id in user_state and user_state[chat_id] == 'themes':
            layout = types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton('Темы', callback_data='themes'),
                        types.InlineKeyboardButton('Справка', callback_data='button2'),
                        types.InlineKeyboardButton('Справочник', callback_data='reference'),  # Новая кнопка
                    ],
                ]
            )
            user_state[chat_id] = 'start'
            bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='<b>Меню</b>', reply_markup=layout, parse_mode='html')
        elif chat_id in user_state and user_state[chat_id] == 'button2':
            layout = types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton('Темы', callback_data='themes'),
                        types.InlineKeyboardButton('Справка', callback_data='button2'),
                        types.InlineKeyboardButton('Справочник', callback_data='reference'),  # Новая кнопка
                    ],
                ]
            )
            user_state[chat_id] = 'start'
            bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='<b>Меню</b>', reply_markup=layout, parse_mode='html')
        elif chat_id in user_state and user_state[chat_id] == 'reference':
            layout = types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton('Темы', callback_data='themes'),
                        types.InlineKeyboardButton('Справка', callback_data='button2'),
                        types.InlineKeyboardButton('Справочник', callback_data='reference'),  # Новая кнопка
                    ],
                ]
            )
            user_state[chat_id] = 'start'
            bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='<b>Меню</b>', reply_markup=layout, parse_mode='html')
    else:
        # Обработка других вариантов inline-кнопок
        url = f'https://math-ege.sdamgia.ru/test?theme={callback.data}'
        bot.send_message(chat_id, f'<b>{callback.data}</b>', parse_mode='html')
        bot.send_message(chat_id, f'<a href="{url}">Link to the site</a>', parse_mode='html', disable_web_page_preview=True)

# Запуск бота в режиме ожидания новых сообщений
bot.polling(none_stop=True)
