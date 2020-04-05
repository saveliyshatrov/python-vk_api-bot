# 7c7705436a9f0705bdb09d8734b9ef4817828f2781b3bd943c45dae1fe8e54fa97954f1dc5ec81a101d33
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import random
import wikipedia
import time
import json
import datetime

print(str(datetime.datetime.now()).replace('-', '').replace(':', '').replace('.', '').replace(' ', ''))

wikipedia.set_lang("RU")

token = '7c7705436a9f0705bdb09d8734b9ef4817828f2781b3bd943c45dae1fe8e54fa97954f1dc5ec81a101d33'
vk = vk_api.VkApi(token=token)
class VK(object):
    def __init__(self):
        pass

    def TakeRandomId(self):
        random_id = str(datetime.datetime.now()).replace('-', '').replace(':', '').replace('.', '').replace(' ', '')
        return random_id

    def CreateButton(self, _type='text', label='название кнопки', color='red'):
        if color == 'red':
            color = 'negative'
        if color == 'green':
            color = 'positive'
        if color == 'gray':
            color = 'secondary'
        if color == 'blue':
            color = 'primary'
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
        vk.method('messages.send', {'user_id': user_id,
                                    'message': message, 
                                    'random_id': self.TakeRandomId(), 
                                    'keyboard': keyboard})

VK = VK()
button_fast_decision = VK.CreateButton(_type='text', label='Быстрое решение', color='green')
button_tarrifs = VK.CreateButton(_type='text', label='Тарифы', color='gray')
button_about_us = VK.CreateButton(_type='text', label='О нас', color='gray')
button_help = VK.CreateButton(_type='text', label='Help', color='gray')
button_close = VK.CreateButton(_type='text', label='Закрыть', color='red')

main_keyboard = VK.CreateKeyboard(one_time=False, buttons=[
    [button_fast_decision],
    [button_tarrifs],
    [button_about_us, button_help],
    [button_close]
])

button_tariff_1 = VK.CreateButton(_type='text', label='Тариф 1', color='gray')
button_tariff_2 = VK.CreateButton(_type='text', label='Тариф 2', color='gray')
button_tariff_3 = VK.CreateButton(_type='text', label='Тариф 3', color='gray')
button_to_main_keyboard = VK.CreateButton(_type='text', label='В главное меню', color='green')

tariff_keyboard = VK.CreateKeyboard(one_time=False, buttons=[
    [button_tariff_1],
    [button_tariff_2],
    [button_tariff_3],
    [button_to_main_keyboard]
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
            elif request == 'Тарифы':
                VK.WriteMessege(event.user_id, 'Тарифы', tariff_keyboard)

            elif request == 'В главное меню':
                VK.WriteMessege(event.user_id, '⬅ Назад', main_keyboard)

            elif request == 'время':
                VK.WriteMessege(event.user_id, str(time.ctime()), main_keyboard)
            else:
                VK.WriteMessege(event.user_id, "Ничего не понял, но очень интересно", main_keyboard)
