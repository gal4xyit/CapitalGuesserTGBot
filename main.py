import telebot
import config
import json
import random

bot = telebot.TeleBot(config.token)
with open('countries.JSON', 'r', encoding="utf-8") as file:
    countries = json.load(file)

current_country = None
correct_answer = None
is_game_active = False
start_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
start_keyboard.add(telebot.types.KeyboardButton("Почати гру"))


@bot.message_handler(commands=['start'])
def start_game(message):
    bot.send_message(message.chat.id, "Вітаю, у грі - «Вгадай столицю»!\nНатисніть на кнопку щоб почати.", reply_markup=start_keyboard)


@bot.message_handler(func=lambda message: not is_game_active)
def messages_handler(message):
    if message.text == "Почати гру":
        global is_game_active
        is_game_active = True
        bot.send_message(message.chat.id, "Гра почалася!", reply_markup=telebot.types.ReplyKeyboardRemove())
        new_question(message)


@bot.message_handler(commands=['stop'])
def end_game(message):
    global is_game_active
    is_game_active = False
    bot.send_message(message.chat.id, "Гру зупинено. Введіть /start, щоб почати.", reply_markup=telebot.types.ReplyKeyboardRemove())


def new_question(message):
    global current_country, correct_answer

    current_country, correct_answer = random.choice(list(countries.items()))
    capitals = list(countries.values())
    options = random.sample(capitals, 4)
    if correct_answer not in options:
        options.pop()
        options.append(correct_answer)
    random.shuffle(options)

    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
    buttons = [telebot.types.KeyboardButton(option) for option in options]
    buttons.append(telebot.types.KeyboardButton("Завершити гру"))
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, f"{current_country}", reply_markup=keyboard)


@bot.message_handler(func=lambda message: is_game_active)
def handle_answer(message):
    global correct_answer, is_game_active

    if message.text == "Завершити гру":
        bot.send_message(message.chat.id, "Гру завершено! До зустрічі!", reply_markup=start_keyboard)
        is_game_active = False
        return

    if message.text == correct_answer:
        bot.send_message(message.chat.id, "Правильно! 🎉")
        new_question(message)
    else:
        bot.send_message(message.chat.id, f"Неправильно. Правильна відповідь: {correct_answer}.")
        new_question(message)


if __name__ == '__main__':
    bot.infinity_polling()
