import telebot
import os
from map import plot_map_to_file, get_coordinates, two_opt, text_of_route

# Get the token from the environment variable
token = os.environ['TELEGRAM_BOT_TOKEN']

bot = telebot.TeleBot(token)

# Create a list to store addresses with types and numbers
addresses = []

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = telebot.types.KeyboardButton("Добавить адрес")
    markup.add(button)
    bot.send_message(message.chat.id, "Привет ✌️ ", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Добавить адрес")
def add_address_type(message):
    markup = telebot.types.InlineKeyboardMarkup()
    postamat_button = telebot.types.InlineKeyboardButton("Добавить почтомат", callback_data="add_postamat")
    branch_button = telebot.types.InlineKeyboardButton("Добавить отделение", callback_data="add_branch")
    markup.add(postamat_button, branch_button)
    bot.send_message(message.chat.id, "Выберите тип адреса:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["add_postamat", "add_branch"])
def add_address_number(call):
    if call.data == "add_postamat":
        address_type = "Почтомат"
    elif call.data == "add_branch":
        address_type = "Отделение"
    bot.send_message(call.message.chat.id, f"Введите номер {address_type.lower()}а:", reply_markup=add_more_addresses_markup())
    bot.register_next_step_handler(call.message, save_address(address_type))

def save_address(address_type):
    def inner_save_address(message):
        number = message.text
        address = f"{address_type} {number}"
        addresses.append(address)
        bot.send_message(message.chat.id, f"{address_type} с номером {number} успешно добавлен.", reply_markup=add_more_addresses_markup())
    return inner_save_address

def add_more_addresses_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    add_button = telebot.types.InlineKeyboardButton("Добавить адрес", callback_data="add_address")
    done_button = telebot.types.InlineKeyboardButton("Закончить", callback_data="done")
    markup.add(add_button, done_button)
    return markup

@bot.callback_query_handler(func=lambda call: call.data == "add_address")
def add_address_handler(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите тип адреса:", reply_markup=add_address_type_markup())

def add_address_type_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    postamat_button = telebot.types.InlineKeyboardButton("Добавить почтомат", callback_data="add_postamat")
    branch_button = telebot.types.InlineKeyboardButton("Добавить отделение", callback_data="add_branch")
    markup.add(postamat_button, branch_button)
    return markup

@bot.callback_query_handler(func=lambda call: call.data == "done")
def show_addresses(call):
    if not addresses:
        bot.send_message(call.message.chat.id, "Нет добавленных адресов.")
    else:
        address_list = "\n".join(addresses)
        bot.send_message(call.message.chat.id, "Ваши адреса:\n" + address_list, reply_markup=calculate_markup())

        # Generate the map image and save it to a file
        plot_map_to_file(addresses, 'map.png')

        # Send the generated map image to the Telegram chat
        with open('map.png', 'rb') as f:
            bot.send_photo(call.message.chat.id, f)

        # Get the route text
        points = [{'number': coordinate['number'], 'coordinate': (coordinate['latitude'], coordinate['longitude'])} for coordinate in get_coordinates(addresses)]
        route = two_opt(points)
        route_text = text_of_route(route)

        # Send the route as a message in the Telegram chat
        bot.send_message(call.message.chat.id, route_text, reply_markup=restart_markup())

def calculate_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    calculate_button = telebot.types.InlineKeyboardButton("Рассчитать", callback_data="calculate")
    markup.add(calculate_button)
    return markup

def restart_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    restart_button = telebot.types.InlineKeyboardButton("Заново", callback_data="restart")
    markup.add(restart_button)
    return markup

@bot.callback_query_handler(func=lambda call: call.data == "restart")
def restart(call):
    global addresses
    addresses = []
    bot.send_message(call.message.chat.id, "Вы можете ввести новую комбинацию точек.", reply_markup=start_markup())

def start_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = telebot.types.KeyboardButton("Добавить адрес")
    markup.add(button)
    return markup

bot.infinity_polling()
