# 7c7705436a9f0705bdb09d8734b9ef4817828f2781b3bd943c45dae1fe8e54fa97954f1dc5ec81a101d33
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import vk_api
import random
import wikipedia
import time
import json

wikipedia.set_lang("RU")

token = 'your token here'
vk = vk_api.VkApi(token=token)
class VK(object):
    def CreateButton(self, _type='text', label='название кнопки', color='secondary'):
        button = {
            'action': {
                'type': _type,
                'payload': json.dumps({'buttons': '1'}),
                'label': label,
            },
            'color': color
        }
        return button

    def CreateKeyboard(self, one_time=False, buttons = []):
        keyboard = {
            'one_time': one_time,
            'buttons': buttons
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def WriteMessege(self, user_id, message, keyboard):
        random_number = random.randrange(1, 10000000000, 1)
        print(user_id)
        vk.method('messages.send', {'user_id': user_id,
                                    'message': message, 
                                    'random_id': random_number, 
                                    'keyboard': keyboard})

VK = VK()
button_fast_decision = VK.CreateButton(_type='text', label='Быстрое решение', color='positive')
button_tarrifs = VK.CreateButton(_type='text', label='Тарифы', color='secondary')
button_about_us = VK.CreateButton(_type='text', label='О нас', color='secondary')
button_help = VK.CreateButton(_type='text', label='Help', color='secondary')
button_close = VK.CreateButton(_type='text', label='Закрыть', color='negative')

main_keyboard = VK.CreateKeyboard(one_time=False, buttons=[
    [button_fast_decision],
    [button_tarrifs],
    [button_about_us, button_help],
    [button_close]
])

longpoll = VkLongPoll(vk)

# Основной цикл
for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:

        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:

            # Сообщение от пользователя
            request = event.text

            # Каменная логика ответа
            if request == "привет":
                VK.WriteMessege(event.user_id, "Хай", main_keyboard)
            elif request == "пока":
                VK.WriteMessege(event.user_id, "Пока((", main_keyboard)
            elif 'вики' in request:
                request = request.replace('вики', '').strip()
                if request != '':
                    VK.WriteMessege(
                        event.user_id, 'Вот что мне удалось найти: ' + str(wikipedia.summary(request)), main_keyboard)
                else:
                    VK.WriteMessege(
                        event.user_id, 'Напиши например "вики слон" и тогда твой запрос будет обработан', main_keyboard)
            elif request == 'время':
                VK.WriteMessege(event.user_id, str(time.ctime()), main_keyboard)
            else:
                VK.WriteMessege(event.user_id, "Ничего не понял, но очень интересно", main_keyboard)
