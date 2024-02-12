import telebot
from telebot import types
import requests
import json

bot = telebot.TeleBot('6977710887:AAGfoal03KVByfACrLxM6dcjgX6dd48OWs0')

def get_general_data():
    response = requests.get('https://math-ege.sdamgia.ru/newapi/general')
    parsedData = json.loads(response.content)
    return parsedData

@bot.message_handler(commands=['start'])
def main(message):
    layout = types.InlineKeyboardMarkup(
        [
            [
                types.InlineKeyboardButton('Темы', callback_data='themes'),
            ],
        ]
    )
    bot.send_message(message.chat.id, '<b>Меню</b>', reply_markup=layout, parse_mode='html')

def create_layout():
    data = get_general_data()
    iterableData = sorted(data['constructor'], key=lambda k: k['title'])
    filteredData = list(filter(lambda item: type(item.get("subtopics")) is list, iterableData))
    layout = types.InlineKeyboardMarkup()
    for item in filteredData:
        layout.add(types.InlineKeyboardButton(item['title']+ ' ' + '(' +str(item['amount'])+ ')', callback_data=item['issue']))
    return layout

@bot.callback_query_handler(func=lambda callback: True)
def callback_handler(callback):
    if  callback.data == 'themes':
        bot.send_message(callback.message.chat.id, '<b>Темы</b>', reply_markup=create_layout(), parse_mode='html')
    else:
        bot.send_message(callback.message.chat.id, '<b>Разделы</b>', reply_markup=create_subtopics_layout(callback.data), parse_mode='html')
        
def get_subtopics(issue):
    data = get_general_data()
    iterableData = data['constructor']
    element = list(filter(lambda item: item.get("issue") == issue, iterableData))
    return sorted(element[0]['subtopics'], key=lambda k: k['title'])

def create_subtopics_layout(issue):
    subtopics = get_subtopics(issue)
    layout = types.InlineKeyboardMarkup()
    for sub in subtopics:
        layout.add(types.InlineKeyboardButton(sub['title']+ ' ' + '(' +str(sub['amount'])+ ')', url='https://math-ege.sdamgia.ru/test?theme=' + str(sub['id'])))
    return layout


bot.polling(none_stop=True)