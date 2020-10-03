#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

import time
import json

import smtplib

import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from platform import python_version

import random

token = "9373e02c313f48a30dab7084ff6c571023fc46114cd821ec0a5e198224c7ffa49ecefa785606429a8a709"
vk = vk_api.VkApi(token=token)
vk._auth_token()

def start1(id): # Приветствие   
    vk_session = vk_api.VkApi(token=token)
    vk1 = vk_session.get_api() 

    vk1.messages.send(
        peer_id=id,
        random_id=get_random_id(),
        message='Добро пожаловать в сервис сбора заказов и доставки продуктов, Huck UI!'
    )
    
    vk1.messages.send(
        peer_id=id,
        random_id=get_random_id(),
        message='В настоящее время сервис работает только для студентов и сотрудников, проживающих на кампусе ДВФУ. В связи с этим необходимо подтверждение корпоративной почты ДВФУ.'
    )

    email1(id)

def email1(id): ## Введите email
    vk_session = vk_api.VkApi(token=token)
    vk1 = vk_session.get_api()  

    vk1.messages.send(
        peer_id=id,
        random_id=get_random_id(),
        message='Введите email, на который будет выслан проверочный код.'
    )    
    with open(pat, 'r') as f:
        json_data = json.load(f)
        json_data['com'] = "email2"
    with open(pat, 'w') as f:
        f.write(json.dumps(json_data))

def email2(id, email): ## Проверка правильности почты и отправка проверочного кода
    if email[(len(email)-7):len(email)] == 'dvfu.ru' and '@' in email:
        server = 'smtp.yandex.ru'
        user = 'dvfu@appliks.ru'
        password = 'yqtkbkimbmaatdwa'
        rand = random.randint(1000, 9999)
        pat = 'C:/Users/li/Desktop/bot/' + str(id) + '.json'

        recipients = [email]
        sender = 'dvfu@appliks.ru'
        subject = 'Код для доступа к сервису'
        text = str(rand)
        html = '<html><head></head><body><p>'+text+'</p></body></html>'
      
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = 'Huck UI <' + sender + '>'
        msg['To'] = ', '.join(recipients)
        msg['Reply-To'] = sender
        msg['Return-Path'] = sender
        msg['X-Mailer'] = 'Python/'+(python_version())
 
        part_text = MIMEText(text, 'plain')
        part_html = MIMEText(html, 'html')
 
        msg.attach(part_text)
 
        mail = smtplib.SMTP_SSL(server)
        mail.login(user, password)
        mail.sendmail(sender, recipients, msg.as_string())
        mail.quit()

        vk_session = vk_api.VkApi(token=token)
        vk1 = vk_session.get_api()

        keyboard = VkKeyboard(one_time=True)
        
        keyboard.add_button('Отправить новый код подтверждения', color=VkKeyboardColor.PRIMARY)      
        keyboard.add_line()  
        keyboard.add_button('Изменить email', color=VkKeyboardColor.SECONDARY)              
        
        vk1.messages.send(
            peer_id=id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
            message='Проверочный код выслан на корпоративную почту ДВФУ.'
        )
    else: 
        vk_session = vk_api.VkApi(token=token)
        vk1 = vk_session.get_api()
        
        vk1.messages.send(
            peer_id=id,
            random_id=get_random_id(),
            message='Пожалуйста введите корпоративную почту ДВФУ.'
        )
    with open(pat, 'r') as f:
        json_data = json.load(f)
        json_data['code'] = rand
        json_data['email'] = email
        json_data['com'] = 'email3'
    with open(pat, 'w') as f:
        f.write(json.dumps(json_data))

def email3(id, body): ## Проверка проверочного кода
    pat = 'C:/Users/li/Desktop/bot/' + str(id) + '.json'
    with open(pat, 'r') as f:
        json_data = json.load(f)
        code = str(json_data['code'])   
        email = json_data['email']
    if code == str(body):
        with open(pat, 'r') as f:
            json_data = json.load(f)
            json_data['com'] = "email4"
        with open(pat, 'w') as f:
            f.write(json.dumps(json_data))
        email4(id)
    elif body == 'Отправить новый код подтверждения':
        with open(pat, 'r') as f:
            json_data = json.load(f)
            json_data['email'] = ""
            json_data['com'] = "email2"
        with open(pat, 'w') as f:
            f.write(json.dumps(json_data))
        email2(id, email)
    elif body == 'Изменить email':
        with open(pat, 'r') as f:
            json_data = json.load(f)
            json_data['email'] = ""
            json_data['com'] = "email1"
        with open(pat, 'w') as f:
            f.write(json.dumps(json_data))
        email1(id)
    else: 
        vk_session = vk_api.VkApi(token=token)
        vk1 = vk_session.get_api()                   
        vk1.messages.send(
            peer_id=id,
            random_id=get_random_id(),
            message='Не верный код'
        )
        with open(pat, 'r') as f:
            json_data = json.load(f)
            json_data['email'] = ""
            json_data['com'] = "email2"
        with open(pat, 'w') as f:
            f.write(json.dumps(json_data))
        email2(id, email)
        
def email4(id1): ## Email подтвержден    
        pat = 'C:/Users/li/Desktop/bot/' + str(id) + '.json'
        vk_session = vk_api.VkApi(token=token)
        vk1 = vk_session.get_api()            

        keyboard = VkKeyboard(one_time=True)

        keyboard.add_button('Продолжить регистрацию', color=VkKeyboardColor.POSITIVE)      
        keyboard.add_line()  
        keyboard.add_button('Главное меню', color=VkKeyboardColor.PRIMARY)    

        vk1.messages.send(
            peer_id=id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
            message='Email подверждён. Рекомендуем продолжить регистрацию, чтобы экономить время при оформлении заказов.'
        )

        with open(pat, 'r') as f:
            json_data = json.load(f)
            json_data['com'] = "start2"
        with open(pat, 'w') as f:
            f.write(json.dumps(json_data))

def start2(id, body): ## Продолжить регистрацию или Меню
    pat = 'C:/Users/li/Desktop/bot/' + str(id) + '.json'
    if body == 'Продолжить регистрацию':
        with open(pat, 'r') as f:
            json_data = json.load(f)
            json_data['com'] = "start3"
        with open(pat, 'w') as f:
            f.write(json.dumps(json_data))
        start3(id)
    elif body == 'Главное меню':
        with open(pat, 'r') as f:
            json_data = json.load(f)
            json_data['com'] = "menu"
        with open(pat, 'w') as f:
            f.write(json.dumps(json_data))
        menu(id)

def start3(id): ## Введите ФИО
        pat = 'C:/Users/li/Desktop/bot/' + str(id) + '.json'
        vk_session = vk_api.VkApi(token=token)
        vk1 = vk_session.get_api()            

        keyboard = VkKeyboard(one_time=True)
 
        keyboard.add_button('Продолжить без ФИО', color=VkKeyboardColor.SECONDARY)      
        keyboard.add_line()  
        keyboard.add_button('Главное меню', color=VkKeyboardColor.PRIMARY)    

        vk1.messages.send(
            peer_id=id,
            random_id=get_random_id(),
            message='Чтобы ваш заказ не достался чужому человеку, нам необходимо знать ваши личные данные.'
        )
        vk1.messages.send(
            peer_id=id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
            message='Введите ФИО (Заказы можно получить только, указав настоящие данные)'
        )
        with open(pat, 'r') as f:
            json_data = json.load(f)
            json_data['com'] = "start4"
        with open(pat, 'w') as f:
            f.write(json.dumps(json_data))

def start4(id, body): ## Ввод ФИО или Меню
    pat = 'C:/Users/li/Desktop/bot/' + str(id) + '.json'
    if body == "Продолжить без ФИО":
        with open(pat, 'r') as f:
            json_data = json.load(f)
            json_data['com'] = "start5"
        with open(pat, 'w') as f:
            f.write(json.dumps(json_data))
        start5(id)
    elif body == 'Главное меню':
        with open(pat, 'r') as f:
            json_data = json.load(f)
            json_data['com'] = "menu"
        with open(pat, 'w') as f:
            f.write(json.dumps(json_data))
        menu(id)
    else: 
        with open(pat, 'r') as f:
            json_data = json.load(f)
            json_data['com'] = "start5"
            json_data['name'] = body
        with open(pat, 'w') as f:
            f.write(json.dumps(json_data))
        start5(id)

def start5(id): ## Введите номер общежития или Меню
        pat = 'C:/Users/li/Desktop/bot/' + str(id) + '.json'   
        vk_session = vk_api.VkApi(token=token)
        vk1 = vk_session.get_api()            

        keyboard = VkKeyboard(one_time=True)
 
        keyboard.add_button('Продолжить без ввода адреса', color=VkKeyboardColor.SECONDARY)      
        keyboard.add_line()  
        keyboard.add_button('Главное меню', color=VkKeyboardColor.PRIMARY)    

        vk1.messages.send(
            peer_id=id,
            random_id=get_random_id(),
            message='Регистрация почти завершена. Осталось ввести номера общежития и комнаты.'
        )

        vk1.messages.send(
            peer_id=id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
            message='Введите номер общежития. (1-5, 6.1-8.2, 9-11, 1.1-1.10, 2.1-2.10)'        
        )
        with open(pat, 'r') as f:
            json_data = json.load(f)
            json_data['com'] = "start6"
        with open(pat, 'w') as f:
            f.write(json.dumps(json_data))

def start6(id, body): ## Проверка номера общаги
    pat = 'C:/Users/li/Desktop/bot/' + str(id) + '.json'
    if body == "Продолжить без ввода адреса":
        with open(pat, 'r') as f:
            json_data = json.load(f)
            json_data['com'] = "start7"
        with open(pat, 'w') as f:
            f.write(json.dumps(json_data))
        start7(id)
    elif body == 'Главное меню':
        with open(pat, 'r') as f:
            json_data = json.load(f)
            json_data['com'] = "menu"
        with open(pat, 'w') as f:
            f.write(json.dumps(json_data))
        menu(id)
    elif body in '1, 2, 3, 4, 5, 6.1, 6.2, 7.1, 7.2, 8.1, 8.2, 9, 10, 11, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 1.10, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 2.10': 
        with open(pat, 'r') as f:
            json_data = json.load(f)
            json_data['com'] = "start7"
            json_data['kk'] = body
        with open(pat, 'w') as f:
            f.write(json.dumps(json_data))
        start7(id)
    else:
        with open(pat, 'r') as f:
            json_data = json.load(f)
            json_data['com'] = "start5"
        with open(pat, 'w') as f:
            f.write(json.dumps(json_data))
        start5(id)

def start7(id): ## Введите комнату
    pat = 'C:/Users/li/Desktop/bot/' + str(id) + '.json'
    vk_session = vk_api.VkApi(token=token)
    vk1 = vk_session.get_api()            

    keyboard = VkKeyboard(one_time=True)
  
    keyboard.add_button('Главное меню', color=VkKeyboardColor.PRIMARY)    

    vk1.messages.send(
        peer_id=id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message='Введите номер комнаты.'        
    )
    with open(pat, 'r') as f:
        json_data = json.load(f)
        json_data['com'] = "start8"
    with open(pat, 'w') as f:
        f.write(json.dumps(json_data))

def start8(id, body): ## Проверка номера комнаты
    pat = 'C:/Users/li/Desktop/bot/' + str(id) + '.json'
    nn = ""
    if body == 'Главное меню':
        with open(pat, 'r') as f:
            json_data = json.load(f)
            json_data['com'] = "menu"
        with open(pat, 'w') as f:
            f.write(json.dumps(json_data))
        menu(id)
    elif int(body) < 2000:
        with open(pat, 'r') as f:
            json_data = json.load(f)
            json_data['com'] = "menu"
            json_data['nn'] = nn
        with open(pat, 'w') as f:
            f.write(json.dumps(json_data))
        menu(id)
    else:
        with open(pat, 'r') as f:
            json_data = json.load(f)
            json_data['com'] = "menu"
            json_data['nn'] = nn
        with open(pat, 'w') as f:
            f.write(json.dumps(json_data)) 
        start7(id)

def menu(id): ## Главное меню
        vk_session = vk_api.VkApi(token=token)
        vk1 = vk_session.get_api()            

        keyboard = VkKeyboard(one_time=True)
 
        keyboard.add_button('Выбрать товар', color=VkKeyboardColor.POSITIVE)      
        keyboard.add_line()  
        keyboard.add_button('Корзина', color=VkKeyboardColor.PRIMARY)    
        keyboard.add_line() 
        keyboard.add_button('Профиль', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Заказы', color=VkKeyboardColor.SECONDARY)

        vk1.messages.send(
            peer_id=id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
            message='Главное меню.'        
        )    

def profile(id): ## Главное меню
        vk_session = vk_api.VkApi(token=token)
        vk1 = vk_session.get_api()            

        keyboard = VkKeyboard(one_time=True)
 
        keyboard.add_button('Выбрать товар', color=VkKeyboardColor.POSITIVE)      
        keyboard.add_line()  
        keyboard.add_button('Корзина', color=VkKeyboardColor.PRIMARY)    
        keyboard.add_line() 
        keyboard.add_button('Профиль', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Заказы', color=VkKeyboardColor.SECONDARY)

        vk1.messages.send(
            peer_id=id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
            message='Главное меню.'        
        )    

while True:
    try:
        messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            body = messages["items"][0]["last_message"]["text"]
            pat = 'C:/Users/li/Desktop/bot/' + str(id) + '.json'

            if os.path.exists(pat) == False:
                data = {
                    "name": "",
                    "email": "",
                    "kk": "",
                    "nn": "",
                    "com": "start1",
                    "code":"",
                    "tt":""
                    }
                with open(pat, "w") as write_file:
                    json.dump(data, write_file)

            with open(pat, 'r') as f:
                json_data = json.load(f)
                com = json_data['com']

            if com == 'start1':
                start1(id)
            elif com == 'email1':
                email1(id)
            elif com == 'email2':
                email2(id, body)
            elif com == 'email3':
                email3(id, body)
            elif com == 'email4':
                email4(id)
            elif com == 'start2':
                start2(id, body)
            elif com == 'start3':
                start3(id)
            elif com == 'start4':
                start4(id, body)
            elif com == 'start5':
                start5(id)
            elif com == 'start6':
                start6(id, body)
            elif com == 'start7':
                start7(id)
            elif com == 'start8':
                start8(id, body)
            elif com == 'menu':
                menu(id)
                     
    except Exception as E:
        time.sleep(1)