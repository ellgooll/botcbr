from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify

import requests
import json
import re


app = Flask(__name__)
sslify = SSLify(app)

URL = 'https://api.telegram.org/<yourapitoken>/'

def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def send_message(chat_id, text='привет!'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()

def parse_text(text):
    pattern = r'\w+'
    curency = re.search(pattern, text).group()
    return curency

def get_price(curency):
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    r = requests.get(url).json()
    price = r ['Valute'][format(curency)]['Value']
    return price

def get_prev(curency):
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    r = requests.get(url).json()
    prev = r ['Valute'][format(curency)]['Previous']
    return prev

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r ['message']['text']
        pattern = r'\w+'

        if re.search(pattern, message):
            price = get_price(parse_text(message))
            prev = get_prev(parse_text(message))
            # dif = curency_dif()
            price_diff = abs(float(price)-float(prev))

            if float(price) > float(prev):
                dif = 'Вырос на: '
            else:
                dif = 'Упал на: '
            # else:
            #     dif = 'Разница: '

            send_message(chat_id, text= '{0}{1}{2}\n{3}{4}{5}\n{6}{7}{8}'.format('Сегодняшний курс: ', round(price, 2), ' руб.', 'Вчерашний курс: ', round(prev, 2), ' руб.', dif, round(price_diff, 4), ' руб.'))

        # write_json(r)
        return jsonify(r)
    return '<center><br><br><br><h1>created by cats...</h1>'

if __name__ == '__main__':
    app.run()
