import requests
from lxml import html
import random
import time
import json
import sqlite3
from contextlib import closing

s = requests.Session()
data = {'user': 'hamik_kul@vk.com', 'password': 'baBQQvh-ra6jz@$', 'la': 'login'}
headers = {
    'authority': 'math-ege.sdamgia.ru',
    'method': 'POST',
    'path': '/',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'cache-control': 'max-age=0',
    'content-length': '62',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'atoken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MDcxMzkwMTEsImJ1aWQiOjQwMzQ0NCwidXNlcl9pZCI6MTEyOTQwNDcsImxvZ2luX2luZm8iOjkzNjY5MzY0OTE3MjQ1MjQyMzQwMjk2MDA1ODM5NDM0NTQ3NH0.-H3YeIOO5fWfG1c-79-RhzBA-MDaWo5JY8dz5q65DWk',
    'origin': 'https://math-ege.sdamgia.ru',
    'referer': 'https://math-ege.sdamgia.ru/',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36 OPR/62.0.3331.99'
}
r = s.post('https://sdamgia.ru', data=data, headers=headers)
url = 'https://math-ege.sdamgia.ru'
def get_parsed_page(url):
    response = s.get(url)
    parsed_page = html.fromstring(response.content)
    return parsed_page
parsed_page = get_parsed_page(url)
variantHrefs = parsed_page.xpath('//span[@class="our_test pinkmark"]/a/@href')
variantHref = 'https://math-ege.sdamgia.ru/test'
for variant in variantHrefs:
    headers = {'cookie': 'atoken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MDcxMzkwMTEsImJ1aWQiOjQwMzQ0NCwidXNlcl9pZCI6MTEyOTQwNDcsImxvZ2luX2luZm8iOjkzNjY5MzY0OTE3MjQ1MjQyMzQwMjk2MDA1ODM5NDM0NTQ3NH0.-H3YeIOO5fWfG1c-79-RhzBA-MDaWo5JY8dz5q65DWk'} 
    params = {'id': int(variant.split("=")[-1])}
    response = s.get(variantHref, params = params, headers = headers)
    parsed_page = html.fromstring(response.content)
    exercise_urls = parsed_page.xpath('//div[@class="prob_maindiv"]/div/span[@class="prob_nums"]/a/@href')
    for exe in exercise_urls:
        if exercise_urls.index(exe) in (0, 14):
            pass
        else:
            params = {'id': int(exe.split("=")[-1])}
            headers = {'cookie': 'atoken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MDcxMzkwMTEsImJ1aWQiOjQwMzQ0NCwidXNlcl9pZCI6MTEyOTQwNDcsImxvZ2luX2luZm8iOjkzNjY5MzY0OTE3MjQ1MjQyMzQwMjk2MDA1ODM5NDM0NTQ3NH0.-H3YeIOO5fWfG1c-79-RhzBA-MDaWo5JY8dz5q65DWk'}
            task_resp = s.get('https://math-ege.sdamgia.ru/problem', headers = headers, params = params)
            parsed_page = html.fromstring(task_resp.content)
            task = ""
            taskLines = parsed_page.xpath('//div[@class="pbody"]/p/text()')
            for i in taskLines:
                lmn = i.split("\xad")
                for u in lmn:
                    task += u
                task += "\n"
            textLines = parsed_page.xpath('//div[@class="probtext"]/div/div/p/text()')
            text = ""
            for strTextOf in textLines:
                plm = strTextOf.split("\xad")
                for l in plm:
                    text += l            
            exerciseTaskText = task + "\n" + text
            answer = parsed_page.xpath('//div[@class="answer"]/span/text()')[0].split(": ")[-1]
            with sqlite3.connect('exams.db') as conn:
                cursor = conn.cursor()
                data = [(exerciseTaskText, (exercise_urls.index(exe)+1), answer, "ОГЭ")]
                query = 'INSERT INTO tasks (exerciseText, exercise_number, answer, work_type) VALUES (?, ?, ?, ?)'
                cursor.executemany(query, data)
                conn.commit()               
            time.sleep(10)
    time.sleep(10)
