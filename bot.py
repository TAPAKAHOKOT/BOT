import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
from random import randint as rnd
import bs4
import requests as req
import keyboard as kb


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


kb.add_hotkey('q', n)


def get_films():
    arr = []
    page = req.get("https://salekhard.kinoafisha.info/cinema/8323152/")
    soup = bs4.BeautifulSoup(page.text, "html.parser")

    arr_names = soup.select(".films_name.link.link-default")
    arr_times = soup.select(".showtimes_item.fav.fav-film")
    arr_imgs = soup.select(".films_iconFrame")

    text = []
    images = []

    for times, names, img in zip(arr_times, arr_names, arr_imgs):
        s = ""
        times = str(times).split("session_time")[1:]

        name = str(names).split('class="link_border">')[1].split('</span>')[0]

        img = str(img).split('src="')[1].split('"')[0]
        images.append(img)

        s += "\n" + name + "\n"
        for time in times:

            s += time[2:7] + " "
        text.append(s)
    return text, images


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


films = ["кино", "фильмы", "рассписание кино", "афиша", "киноафиша"]

print("--CONNTECTED SUCCESFULL")
print(">>LIstening messages started")

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
       # Слушаем longpoll, если пришло сообщение то:
        if event.text.lower() in films:

            text, imgs = get_films()

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
