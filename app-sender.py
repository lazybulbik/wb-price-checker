from telebot import TeleBot, types

bot = TeleBot('5694054533:AAGVrj58icZPu0L0_3XEVwa3pP1tLO1TGkU')

btn = types.InlineKeyboardButton(text='test', web_app=types.WebAppInfo(url='https://7709-87-117-189-163.ngrok-free.app'))
kb = types.InlineKeyboardMarkup().add(btn)

bot.send_message(chat_id=5061120370, text='test', reply_markup=kb) # 5061120370 