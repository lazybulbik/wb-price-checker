from telebot import TeleBot, types

bot = TeleBot('5694054533:AAGVrj58icZPu0L0_3XEVwa3pP1tLO1TGkU')

btn = types.InlineKeyboardButton(text='test', web_app=types.WebAppInfo(url='https://3385-94-25-190-56.ngrok-free.app'))
kb = types.InlineKeyboardMarkup().add(btn)

bot.send_message(chat_id=5981743985, text='test', reply_markup=kb) # 5061120370 