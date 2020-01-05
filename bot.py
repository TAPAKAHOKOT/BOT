import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
from random import randint as rnd
import bs4
import requests as req
import time as tt
import datetime

t = tt.perf_counter()

password = "4608"


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


global running
running = True


def n():
    global running
    running = False
    print("---BREAKING---")


def get_films(params=0):
    id = "8323152"
    pl = "Полярисе"

    if params:
        for place in params:
            if place.lower() in ["полярис", "полик"]:
                id = "8323152"
                params.pop(params.index(place))
                break

            elif place.lower() == "оцнк":
                id = "8325231"
                pl = "ОЦНК"
                params.pop(params.index(place))
                break

    if params:
        d = params[0]
    else:
        d = 0

    if str(d).lower() == "завтра":
        d = 1
    day = d

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
    if day not in arr_days.keys() and day != 0 and day != 1:
        send_mes("Расписание на {} число отсутсвтует".format(
            day), event.user_id)
    else:
        if day in arr_days:
            link = arr_days[day]
        elif day == 0 or day == 1:
            link = list(arr_days.values())[d]
            day = list(arr_days.keys())[d]

        send_mes("Рассписание кино на {}.{} в {}".format(
            day, datetime.date.today().strftime('%m'), pl), event.user_id)

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


def send_mes(mes, u_id, attachments=False):
    if attachments:
        vk.messages.send(
            user_id=u_id,
            message=mes,
            attachment=','.join(attachments),
            random_id=rnd(10**8, 10**9))
    else:
        vk.messages.send(
            user_id=u_id,
            message=mes,
            random_id=rnd(10**8, 10**9))


films = ["кино", "афиша"]
stop = ["break", "стоп"]

print("--CONNTECTED SUCCESFULL")
print(">>LIstening messages started")

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        # Слушаем longpoll, если пришло сообщение то:

        command = event.text.split(" ")[0].lower()
        params = event.text.split(" ")[1:]

        if command in stop:
            if password in params:
                send_mes("---BREAKING---", event.user_id)
                running = False
            else:
                send_mes("WRONG PASSWORD", event.user_id)

        elif command in films:
            if params:
                text, imgs = get_films(params)
            else:
                text, imgs = get_films()

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

                    send_mes(text[k], event.user_id, attachments)
        else:
            send_mes("Else", event.user_id)
