import os
import sys
import requests
import re
import random
import base64
from fake_useragent import UserAgent
from datetime import datetime
import time
import platform
import socket
from termcolor import colored
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import openpyxl
import glob
import subprocess
from faker import Faker
import os
import sys
import requests
import re
import random
import base64
from fake_useragent import UserAgent
from datetime import datetime
import time
import platform
import socket
from termcolor import colored
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import openpyxl
import glob
import subprocess
from faker import Faker

DB_PATH = "/storage/emulated/0/Download/Telegram/AguhaOsintFREE/

# Конфигурация
PHONE_API_KEY = "a65bda8d58814332915390c6572e1ec9"
EMAIL_API_KEY = "1897d39d83224f9a92f491d6efaa4e6f"
WATERMARK = "@aguhaed1337"
BOT_TOKEN = "7490735094:AAEbpISOsfqO7ODT3vx-JwwSzqSom5EDuqc"
fake = Faker()
yukino = 0

SMTP_ACCOUNTS = [
    {"server": "smtp.gmail.com", "port": 587, "login": "masterali43@gmail.com", "password": "erenutku2010"},
    {"server": "smtp.office365.com", "port": 587, "login": "maveranur96@hotmail.com", "password": "5278205"},


    {"server": "smtp.office365.com", "port": 587, "login": "mava_mavi@hotmail.com", "password": "262626"},{"server": "smtp.office365.com", "port": 587, "login": "mavi-sular-76@hotmail.com", "password": "seval981"},
    {"server": "smtp.office365.com", "port": 587, "login": "mavi_mhk@hotmail.com", "password": "4505096"}
]

SMTP_TO = ["abuse@telegram.org", "dcma@telegram.org"]

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_banner():
    print("\033[1;35m" + r"""
    █████╗  ██████╗ ██╗   ██╗██╗  ██╗ █████╗ 
    ██╔══██╗██╔════╝ ██║   ██║██║  ██║██╔══██╗
    ███████║██║  ███╗██║   ██║███████║███████║
    ██╔══██║██║   ██║██║   ██║██╔══██║██╔══██║
    ██║  ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║
    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
    """ + "\033[0m")
    print("\033[1;35m          AGUHA OSINT TOOL v4.0\033[0m")
    print("\033[1;35m          " + WATERMARK + "\033[0m\n")

def send_via_bot(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=params)
        return response.json().get("ok", False)
    except Exception as e:
        print(f"\033[1;31m[×] Ошибка отправки через бота: {str(e)}\033[0m")
        return False

def search_in_databases(query, search_type='phone'):
    db_path = "/storage/emulated/0/Download/Telegram/AguhaOsintFREE/"
    if not os.path.exists(db_path):
        os.makedirs(db_path)
        print(colored(f"[!] Создана папка для баз: {db_path}", "yellow"))
    
    results = []
    for file in glob.glob(f"{db_path}*.*"):
        try:
            if file.endswith('.txt'):
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    results.extend(line.strip() for line in f if query.lower() in line.lower())
            elif file.endswith('.csv'):
                df = pd.read_csv(file)
                matches = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
                results.extend(matches.to_dict('records'))
            elif file.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
                matches = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
                results.extend(matches.to_dict('records'))
        except Exception as e:
            print(colored(f"[!] Ошибка чтения {file}: {str(e)}", "red"))
    return results

def check_phone(phone):
    clear_screen()
    print(colored(f"\n[🔍] Анализ номера: {phone}", "cyan"))
    
    try:
        resp = requests.get("https://phonevalidation.abstractapi.com/v1/",
                          params={'api_key': PHONE_API_KEY, 'phone': phone},
                          timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            print(colored("\n[✓] Основная информация:", "green"))
            print(f"• Формат: {data.get('format', {}).get('international', 'N/A')}")
            print(f"• Страна: {data.get('country', {}).get('name', 'N/A')}")
            print(f"• Оператор: {data.get('carrier', 'N/A')}")
    except Exception as e:
        print(colored(f"[!] Ошибка API: {str(e)}", "red"))
    
   ш print(colored("\n[✓] Локальные базы:", "green"))
    db_results = search_in_databases(phone)
    if db_results:
        for i, result in enumerate(db_results[:5], 1):
            if isinstance(result, dict):
                print(f"\n• Результат #{i}:")
                for k, v in result.items():
                    if str(v).strip() and str(v) != 'nan':
                        print(f"  {k}: {v}")
            else:
                print(f"• Найдено: {result}")
    else:
        print("• Совпадений не найдено")
    
    print(colored("\n[✓] Соцсети:", "green"))
    print(f"• Telegram: https://t.me/+{phone}")
    print(f"• WhatsApp: https://wa.me/{phone}")
    input("\nНажмите Enter чтобы вернуться...")

def check_email(email):
    clear_screen()
    print(colored(f"\n[🔍] Анализ email: {email}", "cyan"))
    
    try:
        resp = requests.get("https://emailvalidation.abstractapi.com/v1/",
                          params={'api_key': EMAIL_API_KEY, 'email': email},
                          timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            print(colored("\n[✓] Основная информация:", "green"))
            print(f"• Домен: {data.get('domain', 'N/A')}")
            print(f"• Валидность: {'Да' if data.get('is_valid_format', {}).get('value') else 'Нет'}")
    except Exception as e:
        print(colored(f"[!] Ошибка API: {str(e)}", "red"))
    
    print(colored("\n[✓] Локальные базы:", "green"))
    db_results = search_in_databases(email, 'email')
    if db_results:
        for i, result in enumerate(db_results[:3], 1):
            if isinstance(result, dict):
                print(f"\n• Результат #{i}:")
                for k, v in result.items():
                    if str(v).strip() and str(v) != 'nan':
                        print(f"  {k}: {v}")
            else:
                print(f"• Найдено: {result}")
    else:
        print("• Совпадений не найдено")
    input("\nНажмите Enter чтобы вернуться...")

def generate_person():
    clear_screen()
    print(colored("\n[🆔] Генерация личности", "cyan"))
    gender = random.choice(['М', 'Ж'])
    first_name = fake.first_name_male() if gender == 'М' else fake.first_name_female()
    last_name = fake.last_name_male() if gender == 'М' else fake.last_name_female()
    
    print(colored("\n[✓] Основная информация:", "green"))
    print(f"• ФИО: {last_name} {first_name}")
    print(f"• Пол: {gender}")
    print(f"• Дата рождения: {fake.date_of_birth().strftime('%d.%m.%Y')}")
    
    print(colored("\n[✓] Контакты:", "green"))
    print(f"• Телефон: +7{random.randint(900, 999)}{random.randint(1000000, 9999999)}")
    print(f"• Email: {fake.email()}")
    
    print(colored("\n[✓] Документы:", "green"))
    print(f"• Паспорт: {random.randint(10, 99)}{random.choice(['АБ', 'ВГ', 'ДЕ'])} {random.randint(100000, 999999)}")
    input("\nНажмите Enter чтобы вернуться...")

def spam_osk():
    clear_screen()
    print(colored("[⚠] Включи VPN перед использованием!", "red"))
    
    target_username = input("Введите username жертвы (@username): ").strip().replace('@', '')
    chat_id = target_username
    
    spam_messages = [
        "АХАХАХАХА ДА ТЫ ЛОХ",
        "СОСИ ХУЙ НАСОСАТЬ",
        "ТВОЯ МАМКА ВЧЕРА НА БЛЯДЯХ ЗАРАБАТЫВАЛА",
        "ИДИ НАХУЙ СО СВОИМ МНЕНИЕМ",
        "ЧЕ ТАК ТИХО, ТЫ РОТ ХУЕМ ЗАБИТ?",
        "ПИЗДИШЬ КАК ДЫРЯВЫЙ ТАГОН",
        "ТЫ В ЖИЗНИ НИЧЕГО НЕ ДОБЬЁШЬСЯ",
        "ТВОЙ ПАПАША МЕНЯ МОЛИЛ ЧТОБЫ Я ЕГО НЕ ЕБАЛ",
        "ЗАКРОЙ РОТ ПРЕЖДЕ ЧЕМ Я ЕГО ЗАКРОЮ",
        "ТЫ ДАЖЕ СВОЮ СОБАКУ НЕБАШИШЬ НОРМАЛЬНО",
        "ЧЕ ТЫ КАК ДНО УНИТАЗА ВОНЯЕШЬ",
        "ИДИИИ НАААХУУУЙ",
        "ТЫ ДАЖЕ В ПАБЛИК ЧМОШНИКОВ НЕ ПРОЙДЁШЬ",
        "ТВОЯ РЕПУТАЦИЯ КАК ТВОЙ ЧЛЕН — НИЖЕ ПЛИНТУСА"
    ]

    print(colored("\n[⚡] Начинаю спам... (Ctrl+C для остановки)", "yellow"))
    
    try:
        while True:
            for message in spam_messages:
                if send_via_bot(chat_id, message):
                    print(colored(f"Отправлено: {message}", "yellow"))
                else:
                    print(colored("[×] Ошибка отправки!", "red"))
                time.sleep(1)
    except KeyboardInterrupt:
        print(colored("\n[!] Спам остановлен", "yellow"))
    input("\nНажмите Enter чтобы вернуться...")

def send_web_complaint(text, proxy, target_username, target_id, phone):
    global yukino
    headers = {
        'User-Agent': UserAgent().random,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://telegram.org',
        'Referer': 'https://telegram.org/support'
    }
    
    form_data = {
        'message': text,
        'email': f"no-reply{random.randint(100,999)}@example.com",
        'phone': phone,
        'user_id': target_id,
        'setln': 'en'
    }
    
    try:
        response = requests.post(
            'https://telegram.org/support',
            data=form_data,
            headers=headers,
            proxies={'http': proxy, 'https': proxy},
            timeout=15
        )
        
        yukino += 1
        if "Thank you" in response.text:
            print(colored(f"[✓] Жалоба отправлена (Всего: {yukino})", "green"))
        else:
            print(colored("[!] Возможно капча", "yellow"))
    except Exception as e:
        print(colored(f"[!] Ошибка: {str(e)}", "reear_screen()
    print(colored("[⚠] Включи VPN перед использованием!", "red"))
    
    target_username = input("Введите @username (без @): ").strip()
    target_id = input("Введите ID пользователя: ").strip()
    phone = input("Введите номер (+7...): ").strip()
    chat_link = input("Введите ссылку на чат: ").strip() or "N/A"
   
