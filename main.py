import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
from random import randint as rnd
import bs4
import requests as req
import time as tt
import datetime
from random import choice
import json


t = tt.perf_counter()

password = "4608"
running = True

class lgpoll(VkLongPoll):
    def listen(self):
        global running

        while running:
            for event in self.check():
                yield event


tok = "a893759fcdfd06fbdd7b207285342cfcf15c527b1baffda8ce3a07b9c2854565161eef71e31baee7d14a0"
vk_session = vk_api.VkApi(token=tok)

session = requests.Session()
longpoll = lgpoll(vk_session)
vk = vk_session.get_api()

def n():
    running = False
    print("---BREAKING---")



def get_days(cinema:str):
    if cinema == "полярис":
        id = "8323152"
    else:
        id = "8325231"

    arr = []
    link = "https://salekhard.kinoafisha.info/cinema/{}/".format(id)
    page = req.get(link)
    soup = bs4.BeautifulSoup(page.text, "html.parser")

    arr1 = soup.select(".week_num")
    arr2 = soup.select(".week_day")

    arr_days = {}

    for k, i in zip(arr1, arr2):

        k = str(k).split(">")[1]

        if 48 <= ord(k[1]) <= 58:
            k = k[:2]
        else:
            k = k[0]

        i = str(i).split("href=")[1].split(">")[0]

        arr_days[k] = i

    print(arr_days)

def get_films(cinema: str):
    day = 0

    if cinema == "полярис":
        id = "8323152"
    else:
        id = "8325231"

    arr = []
    link = "https://salekhard.kinoafisha.info/cinema/{}/".format(id)
    page = req.get(link)
    soup = bs4.BeautifulSoup(page.text, "html.parser")

    arr1 = soup.select(".week_num")
    arr2 = soup.select(".week_day")

    arr_days = {}

    for k, i in zip(arr1, arr2):

        k = str(k).split(">")[1]

        if 48 <= ord(k[1]) <= 58:
            k = k[:2]
        else:
            k = k[0]

        i = str(i).split("href=")[1].split(">")[0]

        arr_days[k] = i

    if arr1 == [] and arr2 == []:
        send_mes("В кинотеатре в данный момент нет фильмов", event.user_id, keyboard=keyboard_main)

    elif day not in arr_days.keys() and day != 0 and day != 1:
        send_mes("Расписание на {} число отсутсвтует".format(
            day), event.user_id)
    else:
        if day in arr_days:
            link = arr_days[day]
        elif day == 0 or day == 1:
            link = list(arr_days.values())[day]
            day = list(arr_days.keys())[day]

        send_mes("Рассписание кино на {}.{} в {}".format(
            day, datetime.date.today().strftime('%m'), cinema), event.user_id)

        link = link.split("?")
        m_l = "https:" + link[0][1:]

        p = link[1].split("&")
        par = {}

        for k in p:
            par[k.split("=")[0]] = k.split("=")[1]

        page = req.get(m_l, params=par)
        soup = bs4.BeautifulSoup(page.text, "html.parser")

        arr_names = soup.select(".films_name.link.link-default")
        arr_times = soup.select(".showtimes_item.fav.fav-film")
        arr_imgs = soup.select(".films_iconFrame")

        text = []
        images = []

        for times, names, img in zip(arr_times, arr_names, arr_imgs):
            s = ""
            times = str(times).split("session_time")[1:]

            name = str(names).split('class="link_border">')[
                1].split('</span>')[0]

            img = str(img).split('src="')[1].split('"')[0]
            images.append(img)

            s += "\n" + name + "\n"
            for time in times:

                s += time[2:7] + " "
            text.append(s)

        return text, images
    return 0, 0


def get_name(id):
    link = "https://vk.com/id" + str(id)
    page = req.get(link)
    soup = bs4.BeautifulSoup(page.text, "html.parser")

    try:
        name = soup.select(".page_name")[0]
        name = str(name).split(">")[1].split("<")[0]
    except:
        name = ""

    return name


def send_mes(mes, u_id, attachment=None, keyboard=None):
    if attachment:
        vk.messages.send(
            user_id=u_id,
            message=mes,
            attachment=attachment,
            random_id=rnd(10**8, 10**9),
            keyboard=keyboard)
    else:
        vk.messages.send(
            user_id=u_id,
            message=mes,
            random_id=rnd(10**8, 10**9),
            keyboard=keyboard)


def get_button(label, color):
    return {
        "action": {
            "type": "text",
            "label": label,
            "payload": ""
        },
        "color": color
    }

stop = ["break", "стоп"]
hello_answer = ["Добрый день))", "Привет!!!!", "Здравствуй", "Hello there"]
place = ["полярис", "оцнк"]

fats_photo = False
if fats_photo:
    photos = []
    upload = VkUpload(vk_session)
    for k in range(55):
        print(k)
        photos.append(upload.photo_messages(f"photos/{k}.jpeg")[0])

file = open("jokes", "r", encoding='utf-8')

jokes = []
joke = ""
for k in range(100):
    text = file.readline().replace("\n", "")
    joke += text + "\n"

    if "%" in text:
        jokes.append(joke.replace("%", ""))
        joke = ""
file.close()

file = open("koals", "r", encoding='utf-8')
koals = []
koal_fact = ""
for k in range(100):
    text = file.readline().replace("\n", "")
    koal_fact += text + "\n"

    if "%" in text:
        koals.append(koal_fact.replace("%", ""))
        koal_fact = ""
file.close()

file = open("films", "r", encoding='utf-8')
films = []
filmo_fact = ""
for k in range(100):
    text = file.readline().replace("\n", "")
    filmo_fact += text + "\n"

    if "%" in text:
        films.append(filmo_fact.replace("%", ""))
        filmo_fact = ""
file.close()

file = open("filmotop", "r", encoding='utf-8')
filmotops = []
filmotop = ""
for k in range(350):
    text = file.readline().replace("\n", "")
    filmotop += text + "\n"

    if "%" in text:
        filmotops.append(filmotop.replace("%", ""))
        filmotop = ""
file.close()


"""
>>> KEYBOARDS >>>
"""

keyboard_main= {
    "one_time": True,
    "buttons": [
        [get_button(label="КиноАфиша",  color="primary"),
        get_button(label="КиноШутка",  color="primary")],

        [get_button(label="КиноФакт",  color="primary"),
        get_button(label="КиноСовет",  color="primary")]
    ]
}

keyboard_main = json.dumps(keyboard_main, ensure_ascii=False).encode('utf-8')
keyboard_main = str(keyboard_main.decode('utf-8'))

keyboard_afisha= {
    "one_time": True,
    "buttons": [
        [get_button(label="Полярис",  color="primary")],
        [get_button(label="ОЦНК",  color="primary")]
    ]
}

keyboard_afisha = json.dumps(keyboard_afisha, ensure_ascii=False).encode('utf-8')
keyboard_afisha = str(keyboard_afisha.decode('utf-8'))


print("--CONNTECTED SUCCESFULL")
print(">>LIstening messages started\n")

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        # Слушаем longpoll, если пришло сообщение то:

        now = datetime.datetime.now()
        mes_time = str(now.strftime("%H:%M:%Ss"))
        name = get_name(event.user_id)

        try:
            file = open("text.txt", "a")
        except:
            file = open("text.txt", "w")

        mes = name + "\n" + str(event.user_id) + "\n" +\
            mes_time + "\n" + str(event.text) + "\n\n"

        print(mes)

        file.write(mes)
        file.close()

        command = event.text.replace(" ", "").lower()

        if command in stop:
            if event.user_id == 184891897:
                send_mes("---BREAKING---", event.user_id)
                running = False

        elif command == "киноафиша":
            send_mes("Выберете место", event.user_id, keyboard=keyboard_afisha)

        elif command == "киношутка":
            send_mes(f"{choice(jokes)}", event.user_id, keyboard=keyboard_main)

        elif command == "кинофакт":
            send_mes(f"{choice(films)}", event.user_id, keyboard=keyboard_main)

        elif command == "киносовет":
            kino = choice(filmotops)

            ind = filmotops.index(kino)

            upload = VkUpload(vk_session)

            if fats_photo:
                photo = photos[ind]
            else:
                photo = upload.photo_messages(f"photos/{ind}.jpeg")[0]

            attachment = 'photo{}_{}'.format(photo['owner_id'], photo['id'])

            kino_name = kino.split("\n")[0 if kino == filmotops[0] else 1]
            kino_desk = kino[len(kino_name) + 1:].replace("\n", "", 1)

            send_mes(f"Название фильма:\n\t\t\t{kino_name}\n\nОписание:\n\t\t\t\t{kino_desk}", event.user_id, keyboard=keyboard_main, attachment=attachment)

        elif command in place:

            text, imgs = get_films(command)

            if text:
                for k in range(len(text)):
                    if imgs[k]:
                        upload = VkUpload(vk_session)
                        attachments = []
                        image = session.get(imgs[k], stream=True)
                        photo = upload.photo_messages(photos=image.raw)[0]
                        attachments.append(
                            'photo{}_{}'.format(photo['owner_id'], photo['id'])
                        )

        else:
            send_mes(f"{choice(hello_answer)}, {get_name(event.user_id).split(' ')[0]}", event.user_id, keyboard=keyboard_main)
