from aiogram import *
import pytz
import datetime
from handlaers.functions import *
# from buttons.inlineuttons import *
from databas import *
from key import *


@dp.message_handler(commands='start')
async def welcome(message: types.Message):
	user_id = message.chat.id
	sql.execute("""CREATE TABLE IF NOT EXISTS users ("user_id"  INTEGER,"date"  INTEGER, "lang" INTEGER);""")
	check = sql.execute(f"""SELECT user_id FROM users WHERE user_id = {user_id}""").fetchone()
	if check == None:
		sana = datetime.datetime.now(pytz.timezone('Asia/Tashkent')).strftime('%d-%m-%Y %H:%M')
		sql.execute(f"""INSERT INTO users (user_id, date, lang) VALUES ('{user_id}', '{sana}', '{message.from_user.language_code}')""")
		db.commit()

	sql.execute("SELECT id FROM channels")
	rows = sql.fetchall()
	join_inline = types.InlineKeyboardMarkup(row_width=1)

	for row in rows:
		all_details = await dp.bot.get_chat(chat_id=row[0])
		title = 1
		url = all_details['invite_link']
		join_inline.insert(InlineKeyboardButton(f"{title} - kanal", url=url))
		title+=1
	join_inline.add(InlineKeyboardButton("🔁 Tekshirish", callback_data='check'))

	if await functions.check_on_start(message.chat.id):
		await message.answer(f'Assalomu alaykum <b>{message.from_user.first_name}</b>')
	else:
		await message.answer("Botimizdan foydalanish uchun kanalimizga azo bo'ling", reply_markup=join_inline)

@dp.callback_query_handler(text = "check")
async def check(call: CallbackQuery):
	user_id = call.from_user.id
	print(user_id)
	if await functions.check_on_start(user_id):
		await call.answer()
		await call.message.answer(f'Assalomu alaykum <b>{call.from_user.first_name}</b>')
	else:
		await call.answer(show_alert=True, text="Botimizdan foydalanish uchun kanalimizga azo bo'ling")


# await call.message.edit_text("Avval kanalimizga a'zo bo'ling", reply_markup=join_inline)