from vkbottle.bot import BotLabeler, Message, Bot
from functions import (get_user, insert_user, get_taxi, taxi_update_cooldown)
from config import successfull_registration, token, farm_income, farm_prices, BITCOIN_COST, multipliers
import random
from datetime import datetime, timedelta

wl = BotLabeler()
wl.vbml_ignore_case = True
bot = Bot(token=token)

@wl.message(text="Таксовать")
async def taxi(message: Message):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    now = datetime.now()
    if user_info:
        if user_info['last_taxi_time'] is None or now - user_info['last_taxi_time'] > timedelta(minutes=40):
            win_dollars = random.randint(50000, 1000000)
            win_exp = random.randint(500, 10000)
            attachment = "photo-222672748_456239067_c47cece7082a887111"
            await get_taxi(user_id=user_info['id'], win_dollars=win_dollars, win_exp=win_exp)
            await taxi_update_cooldown(user_id=user_info['id'], new_taxi_time=now.isoformat())
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы поработали в такси:\n\n💸 Заработано {win_dollars:,}$ и {win_exp:,} EXP".replace(',', '.'),
                                 attachment=attachment)
            return
        else:
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), таксовать можно раз в 40 минут ❌")
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name)
        await message.answer(successfull_registration)