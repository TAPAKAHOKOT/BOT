import telebot
from random import choice
from random import randint as rnd
import datetime
from emoji import emojize

bot = telebot.TeleBot('979524481:AAH1mxv9Bij5GjMN_zLiD-eZRqAVlO7qtB8')


keyboard_main = telebot.types.ReplyKeyboardMarkup(resize_keyboard=3, one_time_keyboard=False)

keyboard_main.row('КиноАфиша', 'КиноШутка')
keyboard_main.row('КиноФакт', 'КиноСовет')


hello_varioations = ["Привет!!!", "Дратути", "Добрый день", "Hi Hello", "Пис)"]
what_variations = ["А? Что? не пойму", "Whaaaaaat????? ", "Ой, я тебя не понимаю", "Тебя не понять", "Чтоо? "]
hello_commands = ["привет", "салам", "дратути", "hi", "hello", "хай", "здравствуйте", "здорова"]

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


file = open("stickers_what", "r", encoding='utf-8')
stickers_what = []
stick = ""
for k in range(350):
    text = file.readline().replace("\n", "")
    stick += text

    if "%" in text:
        stickers_what.append(stick.replace("%", ""))
        stick = ""
file.close()


file = open("stickers_hello", "r", encoding='utf-8')
stickers_hello = []
stick = ""
for k in range(350):
    text = file.readline().replace("\n", "")
    stick += text

    if "%" in text:
        stickers_hello.append(stick.replace("%", ""))
        stick = ""
file.close()


file = open("stickers_sorry", "r", encoding='utf-8')
stickers_sorry = []
stick = ""
for k in range(350):
    text = file.readline().replace("\n", "")
    stick += text

    if "%" in text:
        stickers_sorry.append(stick.replace("%", ""))
        stick = ""
file.close()

@bot.message_handler(commands=['start'])
def start_message(message):

    print(message.text, message.from_user.username, str(datetime.datetime.now().strftime("%H:%M:%Ss")))
    bot.send_message(message.chat.id, f'{choice(hello_varioations)}, лови клавиатуру', reply_markup=keyboard_main)

@bot.message_handler(content_types=['text'])
def send_message(message):
    command = message.text.lower()
    print(message.text, message.from_user.username, str(datetime.datetime.now().strftime("%H:%M:%Ss")))

    if command in hello_commands:
        bot.send_message(message.chat.id, f'{choice(hello_varioations)}', reply_markup=keyboard_main)
        bot.send_sticker(message.chat.id, choice(stickers_hello))

    elif command == "киношутка":
        bot.send_message(message.chat.id, f"{choice(jokes)}", reply_markup=keyboard_main)

    elif command == "кинофакт":
        bot.send_message(message.chat.id, f"{choice(films)}", reply_markup=keyboard_main)

    elif command == "киноафиша":
        bot.send_message(message.chat.id, f"В данный момент кинотеатры закрыты\n\n\nпс функция дорабатывается", reply_markup=keyboard_main)
        bot.send_sticker(message.chat.id, choice(stickers_sorry))

    elif command == "киносовет":
        ind = rnd(0, len(filmotops))
        kino = filmotops[ind]

        kino_name = kino.split("\n")[0 if kino == filmotops[0] else 1]
        kino_desk = kino[len(kino_name) + 1:].replace("\n", "", 1)

        fire = emojize(":fire:", use_aliases=True)
        cookie = emojize(":cookie:", use_aliases=True)

        bot.send_message(message.chat.id,
                         f"Название фильма:\n\t\t{fire}{fire}{fire}{kino_name}{fire}{fire}{fire}\n\nОписание{cookie}:\n\t\t{kino_desk}",
                         reply_markup=keyboard_main)

        with open(f"photos/{ind}.jpeg", "rb") as file:
            data = file.read()
        bot.send_photo(message.chat.id, photo=data)

    else:
        bot.send_message(message.chat.id, f"{choice(what_variations)}", reply_markup=keyboard_main)
        bot.send_sticker(message.chat.id, choice(stickers_what))

bot.polling()