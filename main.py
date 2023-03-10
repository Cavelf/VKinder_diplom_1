from random import randrange
from orm import *
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import TOKEN_GROUP
from vk_requests import get_user_info, get_user_search, get_photos, get_region, get_city
from keyboard import vk_keyboard

db = ORM()

vk = vk_api.VkApi(token=TOKEN_GROUP)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})


def write_msg_attachment(user_id, message, attachment):

    vk.method('messages.send',
              {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), 'attachment': attachment})


def send_button(user_id):
    vk.method('messages.send',
              {'user_id': user_id, 'random_id': randrange(10 ** 7), 'keyboard': vk_keyboard.get_keyboard(),
               'message': '<-->'})


def greeting(user_id):

    user_fullname = vk.method("users.get", {"user_ids": user_id})
    fullname = user_fullname[0]["first_name"]
    return fullname


def get_bdate():

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                user_bdate = event.text
                return user_bdate


def get_sex():

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                user_sex = event.text
                return user_sex


def get_region_for_search_city_in_chat():

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                user_answer = event.text
                user_region = get_region(user_answer, event.user_id)
                return user_region


def get_city_for_search_in_chat(user_region_id):

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                user_answer = event.text
                user_city = get_city(user_region_id, user_answer, event.user_id)
                return user_city


count = 1
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            if request == "start":
                db.drop_all_tables()

                user_info = get_user_info(event.user_id)
                if 'city_id' not in user_info.keys():  # ????????????????, ?????????????????? ???? ???????? ?????????? ?? ?????????????? ????????????????????????
                    write_msg(event.user_id, f"?? ?????????????? ???? ???????????? ??????????!\n"
                                             " ?????????????? ???????????????? ?????????????? ?? ?????????????? ???????????? ????????.")
                    user_region_id = get_region_for_search_city_in_chat()
                    while user_region_id == "?????????????? ???????????? ????????????" or len(str(user_region_id)) > 7:
                        if user_region_id == "?????????????? ???????????? ????????????":
                            write_msg(event.user_id,
                                      f"?????????????? ???????????? "
                            user_region_id = get_region_for_search_city_in_chat()
                        else:
                            write_msg(event.user_id,
                                      f"?? ?????????? ?????????????????? ???????????????? ?? ?????????????? ??????????????????, ?????? ??????:{user_region_id}")
                            user_region_id = get_region_for_search_city_in_chat()
                    write_msg(event.user_id, f"?????????? ???????????????? ???????????? ?? ?????????????? ?????????? ????????????!")
                    user_city = get_city_for_search_in_chat(user_region_id)
                    while user_city == '?? ???? ?????????? ?????????? ??????????, ?????????? ????????????!':
                        write_msg(event.user_id,
                                  f"?? ???? ?????????? ?????????? ??????????, ?????????????? ????????????")
                        user_city = get_city_for_search_in_chat(user_region_id)
                    user_info['city_id'] = user_city
                    write_msg(event.user_id, f"?????? ????! ?? ?????????? ?????????? ??????????\n"
                                             "?????????? ???? ???????????? ?????????? ?????? ???????????? ????????????, ?????????????? ???????? ??????????????!")

                if 'bdate' not in user_info.keys():  # ????????????????, ?????????????????? ???? ???????? ???????? ???????????????? ?? ?????????????? ????????????????????????
                    write_msg(event.user_id,
                              "?? ?????? ?? ?????????????? ???? ?????????????? ???????? ????????????????! ?????????? ?????? ???????? ????????????????")
                    user_bdate = get_bdate()
                    while not user_bdate.isdigit() or 2004 < int(user_bdate):
                        if user_bdate.isdigit():
                            write_msg(event.user_id, "???????? ?????? ?????? 18!")
                            user_bdate = get_bdate()
                        else:
                            write_msg(event.user_id, "???????????? ??????????! ?????????????? ???? ?????????????? ???? ??????????! ????????????: 1990")
                            user_bdate = get_bdate()
                    user_info['bdate'] = user_bdate

                if 'sex' not in user_info.keys():  # ????????????????, ?????????????????? ???? ???????? ?????? ?? ?????????????? ????????????????????????
                    write_msg(event.user_id,
                              "?? ?????? ?? ?????????????? ???? ???????????? ??????! ?????????? '1' ???????? ???? ??????????????!\n"
                              "?????????? '2' ???????? ???? ????????????!)")
                    user_sex = get_sex()
                    user_info['sex'] = user_sex

                user = get_user_search(user_info, event.user_id)
                for i in user:
                    user_id_to_db = i[0]
                    db.create_tables()
                    if not db.search_id(user_id_to_db, event.user_id):  # ????????????????, ???????????????????????? ???? ??????????????????
                        # ????????????????  ?????????????? ????????????????????????
                        db.add_user(user_id_to_db, event.user_id)  # ???????????????????? ?????????????????? ???????????????? ?? ????
                count_id_in_db = db.count_id()
                id_for_search = db.search_id_in_db(count)
                print(id_for_search)
                photo = get_photos(id_for_search, event.user_id)
                write_msg_attachment(event.user_id, f'https://vk.com/id{id_for_search}', photo)
                send_button(event.user_id)

            if request == "??????????":
                count += 1
                id_for_search = db.search_id_in_db(count)
                if id_for_search is None:
                    write_msg(event.user_id, '??????, ???? ???????? ??????????????????! ???????????? ??????????!')
                    send_button(event.user_id)
                else:
                    photo = get_photos(id_for_search, event.user_id)
                    write_msg_attachment(event.user_id, f'https://vk.com/id{id_for_search}', photo)
                    send_button(event.user_id)

            if request == "??????????":
                count -= 1
                id_for_search = db.search_id_in_db(count)
                if id_for_search is None:
                    write_msg(event.user_id, '?????? ???????????? ??????! ?????????? ??????????!')
                    send_button(event.user_id)
                else:
                    photo = get_photos(id_for_search, event.user_id)
                    write_msg_attachment(event.user_id, f'https://vk.com/id{id_for_search}', photo)
                    send_button(event.user_id)
