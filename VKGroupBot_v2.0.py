import telebot
from telebot import types
import requests
import time
import os
import json

vk_token = 'Your vk token'
tg_token ='Your tg token'
id_channel = '@your id channel'
group_name = 'your group name'
URL = 'your group url'

with open('old_id.json') as file:
    old_id = json.load(file)

bot = telebot.TeleBot(tg_token)
print('bot is online')
while True:
    url = f'https://api.vk.com/method/wall.get?domain={group_name}&count=10&access_token={vk_token}&v=5.81'
    req = requests.get(url)
    src = req.json()
    posts = src['response']['items']
    new_post = posts[1]

    if new_post["id"] != old_id['id']:
        print('----New Post!----')
        LINK = f'{URL}{new_post["from_id"]}_{new_post["id"]}'

        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Перейти к записи 🛫", url=LINK)
        markup.add(button1)
        try:
            photo_url =new_post['attachments'][0]['photo']['sizes'][3]['url']
            img = requests.get(photo_url)
            with open(f'{new_post["id"]}.jpg', 'wb') as img_file:
                img_file.write(img.content)

            print(f'photo_{new_post["id"]} is loaded!   ||  {LINK}')
            pic = open(f'{new_post["id"]}.jpg','rb')
            text = f'{new_post["text"]}'
            bot.send_photo(id_channel, pic, f'{text[:278]}...<a href="{LINK}">Читать полностью</a>', parse_mode='html', reply_markup=markup)
            pic.close()
            os.remove(f'{new_post["id"]}.jpg')
            print('photo deleted')
        except Exception:
            print(f'No photo or any something Exceptions...   ||  {LINK}')
            bot.send_message(id_channel, f'Новый пост в нашем сообществе. Бегом смотреть!\n\n{LINK}',reply_markup=markup)

        old_id = new_post
        with open('old_id.json', 'w') as outfile:
            json.dump(old_id, outfile)

        print('-'*30)

    time.sleep(3600)

bot.infinity_polling()
