import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import csv


API_TOKEN = 'botfather TOKEN'
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    username = message.from_user.username
    btn1 = types.InlineKeyboardButton('سدان', callback_data='1111')
    btn2 = types.InlineKeyboardButton('شاسی بلند', callback_data='2222')
    btn3 = types.InlineKeyboardButton('وانت', callback_data='3333')
    btn4 = types.InlineKeyboardButton('هاچبک', callback_data='4444')
    btn5 = types.InlineKeyboardButton('ون', callback_data='5555')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    if username:
        bot.send_message(message.chat.id,
                         f'کاربر {username} به ربات ماشین یاب خوش آمدی.😊\n'
                         f'دوست داری اطلاعات مربوط به کدوم مدل ماشین رو ببینی؟\n', reply_markup=markup)
    else:
        bot.send_message(message.chat.id,
                         f'😊کاربر عزیز به ربات ماشین یاب خوش آمدی.'
                         f'دوست داری اطلاعات مربوط به کدوم مدل ماشین رو ببینی؟\n', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: ['1111', 'k1', 's1', 'back', '1', '14', 'k5', '5555', '17', '05'
                                               '15', '2222', 'backk', '10-50', 'k3', '12', '4444', 'k4', '04'
                                               '5-10', '50-100', '2', '3', 'mm', 'nn', 's5', 's3', '01',
                                               '02', '03', '033', 's4', '08', '900', '3333', '13', '022', '07'])
def callback(call):
    # sedan
    if call.data == '1111':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn0 = types.InlineKeyboardButton('کارکرده', callback_data='k1')
        btn1 = types.InlineKeyboardButton('صفر', callback_data='s1')
        btn3 = types.InlineKeyboardButton('برگشت⬅️', callback_data='back')
        markup.add(btn0, btn1, btn3)
        bot.edit_message_text('وضعیت خودرو را انتخاب کنید:',
                              call.message.chat.id, call.message.message_id, reply_markup=markup)
    if call.data == 'k1':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('پانصد میلیون-یک میلیارد', callback_data='5-10')
        btn4 = types.InlineKeyboardButton('یک میلیارد-پنج میلیارد', callback_data='10-50')
        btn5 = types.InlineKeyboardButton('پنج میلیارد-ده میلیارد', callback_data='50-100')
        btn3 = types.InlineKeyboardButton('برگشت⬅️', callback_data='backk')
        markup.add(btn1, btn4, btn5, btn3)
        bot.edit_message_text('بازه قیمتی خودرو را انتخاب کنید:',
                              call.message.chat.id, call.message.message_id, reply_markup=markup)
    if call.data == '10-50':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=2&bodytype=sedan&price=1000,5000'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)
    if call.data == '50-100':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=2&bodytype=sedan&price=5000,10000'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)
    if call.data == '5-10':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=2&bodytype=sedan&price=500,1000'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)
    if call.data == 's1':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('پانصد میلیون-یک میلیارد', callback_data='1')
        btn4 = types.InlineKeyboardButton('یک میلیارد-پنج میلیارد', callback_data='2')
        btn5 = types.InlineKeyboardButton('پنج میلیارد-ده میلیارد', callback_data='3')
        btn3 = types.InlineKeyboardButton('برگشت⬅️', callback_data='backk')
        markup.add(btn1, btn4, btn5, btn3)
        bot.edit_message_text('بازه قیمتی خودرو را انتخاب کنید:',
                              call.message.chat.id, call.message.message_id, reply_markup=markup)
    if call.data == '1':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=3&bodytype=sedan&price=500,1000&km=0'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)
    if call.data == '2':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=3&bodytype=sedan&price=1000,5000&km=0'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)
    if call.data == '3':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=3&bodytype=sedan&price=5000,10000&km=0'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)

# shasi_bolan
    if call.data == '2222':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn0 = types.InlineKeyboardButton('کارکرده', callback_data='nn')
        btn1 = types.InlineKeyboardButton('صفر', callback_data='mm')
        btn3 = types.InlineKeyboardButton('برگشت⬅️', callback_data='back')
        markup.add(btn0, btn1, btn3)
        bot.edit_message_text('وضعیت خودرو را انتخاب کنید:',
                              call.message.chat.id, call.message.message_id, reply_markup=markup)
    if call.data == 'nn':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('پانصد میلیون-یک میلیارد', callback_data='01')
        btn4 = types.InlineKeyboardButton('یک میلیارد-پنج میلیارد', callback_data='02')
        btn5 = types.InlineKeyboardButton('پنج میلیارد-ده میلیارد', callback_data='03')
        btn3 = types.InlineKeyboardButton('برگشت⬅️', callback_data='backk')
        markup.add(btn1, btn4, btn5, btn3)
        bot.edit_message_text('بازه قیمتی خودرو را انتخاب کنید:',
                              call.message.chat.id, call.message.message_id, reply_markup=markup)
    if call.data == 'mm':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn4 = types.InlineKeyboardButton('یک میلیارد-پنج میلیارد', callback_data='022')
        btn5 = types.InlineKeyboardButton('پنج میلیارد-ده میلیارد', callback_data='033')
        btn3 = types.InlineKeyboardButton('برگشت⬅️', callback_data='backk')
        markup.add( btn4, btn5, btn3)
        bot.edit_message_text('بازه قیمتی خودرو را انتخاب کنید:',
                              call.message.chat.id, call.message.message_id, reply_markup=markup)
    if call.data == '022':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=3&bodytype=suv&price=1000,5000&km=0'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)
    if call.data == '033':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=3&bodytype=suv&price=5000,10000&km=0'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)
    if call.data == '03':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=2&bodytype=suv&price=5000,10000'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)
    if call.data == '02':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=2&bodytype=suv&price=1000,5000'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)
    if call.data == '01':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=2&bodytype=suv&price=500,1000'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)

# vanet
    if call.data == '3333':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn0 = types.InlineKeyboardButton('کارکرده', callback_data='k3')
        btn1 = types.InlineKeyboardButton('صفر', callback_data='s3')
        btn3 = types.InlineKeyboardButton('برگشت⬅️', callback_data='back')
        markup.add(btn0, btn1, btn3)
        bot.edit_message_text('وضعیت خودرو را انتخاب کنید:',
                              call.message.chat.id, call.message.message_id, reply_markup=markup)
    if call.data == 'k3':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('پانصد میلیون-یک میلیارد', callback_data='12')
        btn4 = types.InlineKeyboardButton('یک میلیارد-پنج میلیارد', callback_data='13')
        btn3 = types.InlineKeyboardButton('برگشت⬅️', callback_data='backk')
        markup.add(btn1, btn4, btn3)
        bot.edit_message_text('بازه قیمتی خودرو را انتخاب کنید:',
                              call.message.chat.id, call.message.message_id, reply_markup=markup)
    if call.data == '12':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=2&bodytype=pickup&price=500,1000'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)
    if call.data == '13':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=2&bodytype=pickup&price=1000,5000'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)
    if call.data == '15':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=3&bodytype=pickup&price=1000,5000&km=0'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)
    if call.data == '14':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=3&bodytype=pickup&price=500,1000&km=0'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)
    if call.data == 's3':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('پانصد میلیون-یک میلیارد', callback_data='14')
        btn4 = types.InlineKeyboardButton('یک میلیارد-پنج میلیارد', callback_data='15')
        btn3 = types.InlineKeyboardButton('برگشت⬅️', callback_data='backk')
        markup.add(btn1, btn4, btn3)
        bot.edit_message_text('بازه قیمتی خودرو را انتخاب کنید:',
                              call.message.chat.id, call.message.message_id, reply_markup=markup)

# van
    if call.data == '5555':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn0 = types.InlineKeyboardButton('کارکرده', callback_data='k5')
        btn1 = types.InlineKeyboardButton('صفر', callback_data='s5')
        btn3 = types.InlineKeyboardButton('برگشت⬅️', callback_data='back')
        markup.add(btn0, btn1, btn3)
        bot.edit_message_text('وضعیت خودرو را انتخاب کنید:',
                              call.message.chat.id, call.message.message_id, reply_markup=markup)
    if call.data == 'k5':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn4 = types.InlineKeyboardButton('یک میلیارد-پنج میلیارد', callback_data='17')
        btn3 = types.InlineKeyboardButton('برگشت⬅️', callback_data='backk')
        markup.add(btn4, btn3)
        bot.edit_message_text('بازه قیمتی خودرو را انتخاب کنید:',
                              call.message.chat.id, call.message.message_id, reply_markup=markup)
    if call.data == '17':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=2&bodytype=van&price=1000,5000'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)
    if call.data == 's5':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn4 = types.InlineKeyboardButton('یک میلیارد-پنج میلیارد', callback_data='900')
        btn3 = types.InlineKeyboardButton('برگشت⬅️', callback_data='backk')
        markup.add(btn4, btn3)
        bot.edit_message_text('بازه قیمتی خودرو را انتخاب کنید:',
                              call.message.chat.id, call.message.message_id, reply_markup=markup)
    if call.data == '900':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=3&bodytype=van&price=1000,5000&km=0'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)

# hachback
    if call.data == '4444':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn0 = types.InlineKeyboardButton('کارکرده', callback_data='k4')
        btn1 = types.InlineKeyboardButton('صفر', callback_data='s4')
        btn3 = types.InlineKeyboardButton('برگشت⬅️', callback_data='back')
        markup.add(btn0, btn1, btn3)
        bot.edit_message_text('وضعیت خودرو را انتخاب کنید:',
                              call.message.chat.id, call.message.message_id, reply_markup=markup)
    if call.data == 'k4':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('پانصد میلیون-یک میلیارد', callback_data='04')
        btn4 = types.InlineKeyboardButton('یک میلیارد-پنج میلیارد', callback_data='05')
        btn3 = types.InlineKeyboardButton('برگشت⬅️', callback_data='backk')
        markup.add(btn1, btn4, btn3)
        bot.edit_message_text('بازه قیمتی خودرو را انتخاب کنید:',
                              call.message.chat.id, call.message.message_id, reply_markup=markup)
    if call.data == '04':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=2&bodytype=hatchback&price=500,1000'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)
    if call.data == '05':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=2&bodytype=hatchback&price=1000,5000'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)
    if call.data == '07':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=3&bodytype=hatchback&price=500,1000&km=0'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)
    if call.data == '08':
        url = r'https://www.hamrah-mechanic.com/cars-for-sale/?kmStatus=3&bodytype=hatchback&price=1000,5000&km=0'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_prices = soup.find_all('div', class_='carCard_price-container__cost__BO_Hy')
        car_name = soup.find_all('span', class_='carCard_header__name__ib5RB')
        with open('car.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, price in zip(car_name, buy_prices):
                writer.writerow([name.get_text(),  price.get_text()])

        with open('car.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        text = ''
        for row in rows:
            text += " | ".join(row) + "\n"
        bot.send_message(call.message.chat.id, text)
    if call.data == 's4':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('پانصد میلیون-یک میلیارد', callback_data='07')
        btn4 = types.InlineKeyboardButton('یک میلیارد-پنج میلیارد', callback_data='08')
        btn3 = types.InlineKeyboardButton('برگشت⬅️', callback_data='backk')
        markup.add(btn1, btn4, btn3)
        bot.edit_message_text('بازه قیمتی خودرو را انتخاب کنید:',
                              call.message.chat.id, call.message.message_id, reply_markup=markup)

# back
    if call.data == 'backk':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn0 = types.InlineKeyboardButton('کارکرده', callback_data='kk')
        btn1 = types.InlineKeyboardButton('صفر', callback_data='ss')
        btn3 = types.InlineKeyboardButton('برگشت⬅️', callback_data='back')
        markup.add(btn0, btn1, btn3)
        bot.edit_message_text('وضعیت خودرو را انتخاب کنید:',
                              call.message.chat.id, call.message.message_id, reply_markup=markup)
    if call.data == 'back':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('سدان', callback_data='1111')
        btn2 = types.InlineKeyboardButton('شاسی بلند', callback_data='2222')
        btn3 = types.InlineKeyboardButton('وانت', callback_data='3333')
        btn4 = types.InlineKeyboardButton('هاچبک', callback_data='4444')
        btn5 = types.InlineKeyboardButton('ون', callback_data='5555')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.edit_message_text('دوست داری اطلاعات مربوط به کدوم مدل ماشین رو ببینی؟:',
                              call.message.chat.id, call.message.message_id, reply_markup=markup)


bot.infinity_polling()
