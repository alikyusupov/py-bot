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
    # Получаем имя пользователя
    user_name = message.from_user.first_name

    # Приветственный текст с именем пользователя и кнопка "Начать"
    welcome_text = f"""
    🌟 Добро пожаловать, {user_name}! 🌟

Приготовьтесь к захватывающему путешествию в мир математики ЕГЭ! Я - ваш верный спутник, бот, готовый помочь вам в решении задач и освоении самых интересных тем.

🚀 Нажмите кнопку "Начать", чтобы взлететь в атмосферу знаний и уверенности в своих математических способностях! Выберите раздел, который вас привлекает, и дайте старт своему учебному полету к успеху.

🎓 Не просто бот, а ваш личный наставник в мире математики! Приготовьтесь к захватывающему обучению и уверенному совладению с заданиями ЕГЭ. Давайте начнем этот увлекательный путь вместе!

🔥 Готовы к приключениям? Тогда вперед, нажмите "Начать" и дайте старт математическому волшебству! 🚀

    """

    # Создаем кнопку "Начать"
    layout = types.InlineKeyboardMarkup(
        [
            [
                types.InlineKeyboardButton('Начать', callback_data='start'),
            ],
        ]
    )

    # Отправляем приветствие с кнопкой "Начать"
    bot.send_message(message.chat.id, welcome_text, reply_markup=layout)

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
        # ... (код для команды "Начать")
        layout = types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton('Темы', callback_data='themes'),
                ],
                [
                    types.InlineKeyboardButton('Справка', callback_data='button2'),
                ],
                [
                    types.InlineKeyboardButton('Справочник', callback_data='reference'),
                ],
            ]
        )
        user_state[chat_id] = 'start'
        bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='<b>Меню Бота</b>', reply_markup=layout, parse_mode='html')
    elif callback.data == 'themes':
        # ... (код для команды "Темы")
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
        layout.add(types.InlineKeyboardButton('Назад', callback_data='back'))
        user_state[chat_id] = 'themes'
        bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='<b>Темы</b>', reply_markup=layout, parse_mode='html')
    elif callback.data == 'button2':
        # ... (код для команды "Справка")
        instruction_text = f"""<b>Как использовать бота:</b>
        1. <i>Запуск бота:</i> Нажмите кнопку "Пуск" или другую команду, предложенную ботом, чтобы активировать его.
        2. <i>Ознакомьтесь с командами:</i> Большинство ботов поддерживают определенные команды. Например, "/help", "/info" или "/commands" для получения списка доступных команд."""
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
        # ... (код для команды "Справочник")
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
        layout.add(types.InlineKeyboardButton('Назад', callback_data='back'))
        user_state[chat_id] = 'reference'
        bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='<b>Справочник:</b>', reply_markup=layout, parse_mode='html')
    elif callback.data == 'back':
        # ... (код для команды "Назад")
        if chat_id in user_state and user_state[chat_id] == 'themes':
            layout = types.InlineKeyboardMarkup(
                [
                [
                    types.InlineKeyboardButton('Темы', callback_data='themes'),
                ],
                [
                    types.InlineKeyboardButton('Справка', callback_data='button2'),
                ],
                [
                    types.InlineKeyboardButton('Справочник', callback_data='reference'),
                ],
            ]
            )
            user_state[chat_id] = 'start'
            bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='<b>Меню Бота</b>', reply_markup=layout, parse_mode='html')
        elif chat_id in user_state and user_state[chat_id] == 'button2':
            layout = types.InlineKeyboardMarkup(
                [
                [
                    types.InlineKeyboardButton('Темы', callback_data='themes'),
                ],
                [
                    types.InlineKeyboardButton('Справка', callback_data='button2'),
                ],
                [
                    types.InlineKeyboardButton('Справочник', callback_data='reference'),
                ],
            ]
            )
            user_state[chat_id] = 'start'
            bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='<b>Меню Бота</b>', reply_markup=layout, parse_mode='html')
        elif chat_id in user_state and user_state[chat_id] == 'reference':
            layout = types.InlineKeyboardMarkup(
                [
                [
                    types.InlineKeyboardButton('Темы', callback_data='themes'),
                ],
                [
                    types.InlineKeyboardButton('Справка', callback_data='button2'),
                ],
                [
                    types.InlineKeyboardButton('Справочник', callback_data='reference'),
                ],
            ]
            )
            user_state[chat_id] = 'start'
            bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='<b>Меню Бота</b>', reply_markup=layout, parse_mode='html')
    else:
        # ... (код для других inline-кнопок)
        url = f'https://math-ege.sdamgia.ru/test?theme={callback.data}'
        bot.send_message(chat_id, f'<b>{callback.data}</b>', parse_mode='html')
        bot.send_message(chat_id, f'<a href="{url}">Link to the site</a>', parse_mode='html', disable_web_page_preview=True)

# Запуск бота в режиме ожидания новых сообщений
bot.polling(none_stop=True)
