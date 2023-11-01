import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()
bot = telebot.TeleBot("6465757449:AAGdhxnPnssGiXu3wTWnJKbmAq2QRdQu3eo",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "регистрация"
text_button_1 = "веб разработка"
text_button_2 = "мобильная разработка"
text_button_3 = "ПО для ПК"


menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Ответь на вопросы ниже)',
        reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, '*Ваше* _имя_?')
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Здорово! Ваш `возраст?`')
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Спасибо за регистрацию! Можете потыкать на кнопочки', reply_markup=menu_keyboard)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "HTML. Отличный базовый язык программирования, с помощью которого разрабатываются интернет страницы. Он прост в изучении и способен дать новичку понимание того, как устроена страница в Сети, какие ее главные компоненты, какие функциональные возможности здесь реализовываются. Но стоит отметить, что самого HTML слишком мало для успешной деятельности в Интернет, так как с его помощью можно в основном только создавать внешний облик страницы, но не ее функционал. HTML – это отличный язык программирования для новичков, которые хотят начать писать сайты и разобраться в основах.", reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Java это очень серьезный язык, который позволяет писать не только мобильное ПО, но и разрабатывать программы для работы серверов, работать с графикой и многое другое. Java как первый язык может быть отличным выбором, так как дает большие знания и возможности решать реальные задачи.", reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "С. Старый язык, но очень распространенный. На нем пишутся драйвера, операционные системы, он может быть задействован для решения огромного множества задач. Большинство программ на ПК создано на базе этого языка; "
                                      "С++. Современный язык программирования, который используется для решения всех классических задач для программиста: написания ПО, разработка игр, драйверов и тому подобных вещей. Понемногу устаревает, но все еще повсеместно применяется.", reply_markup=menu_keyboard)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()

