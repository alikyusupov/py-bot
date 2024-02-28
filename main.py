import telebot
from telebot import types
import json
import asyncio
from playwright.async_api import async_playwright
import json

USER_NAME = ''
GENERAL_DATA = {}
SBR_WS_CDP = 'wss://brd-customer-hl_7b3b4e62-zone-scraping_browser1-country-ru:wgdghplqrzf8@brd.superproxy.io:9222'
HELP_TEXT = welcome_text = f"""
    Здесь будет текст который объясняет как пользоваться ботом

    Под текстом будет кнопка 'Назад'
    """

bot = telebot.TeleBot('6977710887:AAGfoal03KVByfACrLxM6dcjgX6dd48OWs0')

def generate_intro(name):
    return f"""
    🌟 Добро пожаловать, {name}! 🌟

Приготовьтесь к захватывающему путешествию в мир математики ЕГЭ! Я - ваш верный спутник, бот, готовый помочь вам в решении задач и освоении самых интересных тем.

🚀 Нажмите кнопку "Начать", чтобы взлететь в атмосферу знаний и уверенности в своих математических способностях! Выберите раздел, который вас привлекает, и дайте старт своему учебному полету к успеху.

🎓 Не просто бот, а ваш личный наставник в мире математики! Приготовьтесь к захватывающему обучению и уверенному совладению с заданиями ЕГЭ. Давайте начнем этот увлекательный путь вместе!

🔥 Готовы к приключениям? Тогда вперед, нажмите "Начать" и дайте старт математическому волшебству! 🚀

    """


async def run(pw):
    global GENERAL_DATA
    print('Connecting to Scraping Browser...')
    browser = await pw.chromium.connect_over_cdp(SBR_WS_CDP)
    page = await browser.new_page()
    print('Connected! Navigating to https://math-ege.sdamgia.ru/newapi/general...')
    await page.goto('https://math-ege.sdamgia.ru/newapi/general')
    # CAPTCHA handling: If you're expecting a CAPTCHA on the target page, use the following code snippet to check the status of Scraping Browser's automatic CAPTCHA solver
    client = await page.context.new_cdp_session(page)
    print('Waiting captcha to solve...')
    solve_res = await client.send('Captcha.waitForSolve', {
        'detectTimeout': 1500,
    })
    print('Captcha solve status:', solve_res['status'])
    print('Navigated! Scraping page content...')
    a_handle = await page.evaluate_handle("document.body")
    result_handle = await page.evaluate_handle("body => body.innerText", a_handle)
    stringData = await result_handle.json_value()
    await result_handle.dispose()
    await browser.close()
    GENERAL_DATA = json.loads(stringData)

async def main():
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())


@bot.message_handler(commands=['start'])
def do_start(message):
    global USER_NAME
    USER_NAME = message.from_user.first_name
    # Приветственный текст с именем пользователя и кнопка "Начать"
    welcome_text = generate_intro(USER_NAME)
    layout = create_start_layout()
    bot.send_message(message.chat.id, welcome_text, reply_markup=layout, parse_mode='html')

@bot.message_handler(commands=['topics'])
def do_topics(message):
    # Приветственный текст с именем пользователя и кнопка "Начать"
    bot.send_message(message.chat.id, '<b>Темы</b>', reply_markup=create_layout(), parse_mode='html')

@bot.message_handler(commands=['help'])
def do_help(message):
    # Приветственный текст с именем пользователя и кнопка "Начать"
    bot.send_message(message.chat.id, HELP_TEXT, reply_markup=create_help_layout() , parse_mode='html')

@bot.callback_query_handler(func=lambda callback: True)
def callback_handler(callback):
    global USER_NAME
    if  callback.data == 'topics':
        bot.send_message(callback.message.chat.id, '<b>Темы</b>', reply_markup=create_layout(), parse_mode='html')
    elif  callback.data == 'help':
        bot.send_message(callback.message.chat.id, HELP_TEXT, reply_markup=create_help_layout() , parse_mode='html')
    elif  callback.data == 'back':
        bot.send_message(callback.message.chat.id, generate_intro(USER_NAME), reply_markup=create_start_layout(), parse_mode='html')
    else:
        bot.send_message(callback.message.chat.id, '<b>Разделы</b>', reply_markup=create_subtopics_layout(callback.data), parse_mode='html')
        
def get_subtopics(issue):
    global GENERAL_DATA
    iterableData = GENERAL_DATA['constructor']
    element = list(filter(lambda item: item.get("issue") == issue, iterableData))
    return sorted(element[0]['subtopics'], key=lambda k: k['title'])

def create_start_layout():
    layout = types.InlineKeyboardMarkup(
        [
            [
                types.InlineKeyboardButton('Начать', callback_data='topics'),
            ],
            [
                types.InlineKeyboardButton('Помощь', callback_data='help'),
            ],
        ]
    )
    return layout

def create_layout():
    global GENERAL_DATA
    iterableData = sorted(GENERAL_DATA['constructor'], key=lambda k: k['title'])
    filteredData = list(filter(lambda item: type(item.get("subtopics")) is list, iterableData))
    layout = types.InlineKeyboardMarkup()
    for item in filteredData:
        layout.add(types.InlineKeyboardButton(item['title']+ ' ' + '(' +str(item['amount'])+ ')', callback_data=item['issue']))
    return layout

def create_subtopics_layout(issue):
    subtopics = get_subtopics(issue)
    layout = types.InlineKeyboardMarkup()
    for sub in subtopics:
        layout.add(types.InlineKeyboardButton(sub['title']+ ' ' + '(' +str(sub['amount'])+ ')', url='https://math-ege.sdamgia.ru/test?theme=' + str(sub['id'])))
    return layout

def create_help_layout():
    layout = types.InlineKeyboardMarkup()
    layout.add(types.InlineKeyboardButton('Назад', callback_data='back'))
    return layout


bot.polling(none_stop=True)