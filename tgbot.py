import telebot
from random import choice
from random import randint as rnd
import datetime
from emoji import emojize

bot = telebot.TeleBot('979524481:AAH1mxv9Bij5GjMN_zLiD-eZRqAVlO7qtB8')

keyboard_main = telebot.types.ReplyKeyboardMarkup(resize_keyboard=3, one_time_keyboard=False)

keyboard_main.row('КиноАфиша', 'КиноШутка')
keyboard_main.row('КиноФакт', 'КиноСовет')

hello_variations = ["Привет!!!", "Дратути", "Добрый день", "Hi Hello", "Пис)", "Добро пожаловать", "You are welcome",
                     "Добрый день, добрый вечер и доброй ночи!"]
what_variations = ["А? Что? не пойму", "Whaaaaaat????? ", "Ой, я тебя не понимаю", "Тебя не понять", "Чтоо? ",
                   "Повториии", "Not understand", "Error 418 try again", "А?"]
hello_commands = ["привет", "салам", "дратути", "hi", "hello", "хай", "здравствуйте", "здорова", "пис", "peace"]


def unpack_file(filename: str, line_end: str = "") -> list:
    file = open(filename, "r", encoding='utf-8')

    output_array = []
    text_line = ""

    for _ in range(350):
        text = file.readline().replace("\n", "")
        text_line += text + line_end

        if "%" in text:
            output_array.append(text_line.replace("%", ""))
            text_line = ""
    file.close()

    return output_array


jokes = unpack_file("jokes")
films = unpack_file("films")
filmotops = unpack_file("filmotop", line_end="\n")
stickers_what = unpack_file("stickers_what")
stickers_hello = unpack_file("stickers_hello")
stickers_sorry = unpack_file("stickers_sorry")

random_hello, random_stickers_hello = {}, {}
random_what, random_stickers_what = {}, {}
random_jokes, random_films, random_filmotop = {}, {}, {}
random_stickers_sorry = {}


def add_arrays(chat_id: int):
    if chat_id not in random_hello.keys():
        random_hello[chat_id], random_stickers_hello[chat_id] = [-1] * 3, [-1] * 3
        random_what[chat_id], random_stickers_what[chat_id] = [-1] * 3, [-1] * 3
        random_jokes[chat_id], random_films[chat_id], random_filmotop[chat_id] = [-1] * 30, [-1] * 10, [-1] * 40
        random_stickers_sorry[chat_id] = [-1] * 3


def get_smth_about_random(arr_len: int, rnd_list: list) -> list:
    elements = [k for k in range(arr_len) if k not in rnd_list]

    element = choice(elements)
    rnd_list = [element] + rnd_list[:2]

    return [*rnd_list]


@bot.message_handler(commands=['start'])
def start_message(message):
    print(message.text, message.from_user.username, str(datetime.datetime.now().strftime("%H:%M:%Ss")))
    bot.send_message(message.chat.id, f'{choice(hello_variations)}, лови клавиатуру', reply_markup=keyboard_main)


@bot.message_handler(content_types=['text'])
def send_message(message):
    global random_hello, random_stickers_hello, random_what, random_stickers_what
    global random_jokes, random_films, random_filmotop, random_stickers_sorry

    ident = message.chat.id
    add_arrays(ident)

    command = message.text.lower()
    print(message.text, message.from_user.username, str(datetime.datetime.now().strftime("%H:%M:%Ss")))

    if command in hello_commands:
        random_hello[ident] = get_smth_about_random(len(hello_variations), random_hello[ident])
        random_stickers_hello[ident] = get_smth_about_random(len(stickers_hello), random_stickers_hello[ident])

        bot.send_message(message.chat.id, f'{hello_variations[random_hello[ident][0]]}', reply_markup=keyboard_main)
        bot.send_sticker(message.chat.id, stickers_hello[random_stickers_hello[ident][0]])

    elif command == "киношутка":
        random_jokes[ident] = get_smth_about_random(len(jokes), random_jokes[ident])
        bot.send_message(message.chat.id, f"{jokes[random_jokes[ident][0]]}", reply_markup=keyboard_main)

    elif command == "кинофакт":
        random_films[ident] = get_smth_about_random(len(films), random_films[ident])
        bot.send_message(message.chat.id, f"{films[random_films[ident][0]]}", reply_markup=keyboard_main)

    elif command == "киноафиша":
        random_stickers_sorry[ident] = get_smth_about_random(len(stickers_sorry), random_stickers_sorry[ident])
        bot.send_message(message.chat.id, f"В данный момент кинотеатры закрыты\n\n\nпс функция дорабатывается",
                         reply_markup=keyboard_main)

        bot.send_sticker(message.chat.id, stickers_sorry[random_stickers_sorry[ident][0]])

    elif command == "киносовет":
        random_filmotop[ident] = get_smth_about_random(len(filmotops), random_filmotop[ident])

        ind = random_filmotop[ident][0]
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
        random_what[ident] = get_smth_about_random(len(what_variations), random_what[ident])
        random_stickers_what[ident] = get_smth_about_random(len(stickers_what), random_stickers_what[ident])

        bot.send_message(message.chat.id, f"{what_variations[random_what[ident][0]]}", reply_markup=keyboard_main)
        bot.send_sticker(message.chat.id, stickers_what[random_stickers_what[ident][0]])


bot.polling()