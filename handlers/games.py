from vkbottle.bot import BotLabeler, Message, Bot
from functions import (get_user, insert_user, get_fishing, fishing_update_cooldown, 
                       fish_rob_upgrade, converter, casino_win, casino_lose)
from config import successfull_registration, token, farm_income, farm_prices, BITCOIN_COST, multipliers
import random
from datetime import datetime, timedelta
import re

gl = BotLabeler()
gl.vbml_ignore_case = True
bot = Bot(token=token)

@gl.message(text="Рыбалка")
async def fishing_page(message: Message):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info:
        now = datetime.now()
        if user_info['last_fishing_time'] is None:
            display_fishing = "⛱ Рыбалка доступна! Для начала, используйте: «Рыбачить»."
        elif now - user_info['last_fishing_time'] < timedelta(hours=2):
            display_fishing = "⛱ Рыбалка недоступна, попробуйте позже."
        else:
            display_fishing = "⛱ Рыбалка доступна! Для начала, используйте: «Рыбачить»."

        photo_id = 'photo-222672748_456239023_d018eef133566f8d64'
        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), страница рыбалки:"
                             f"\n\n{display_fishing}"
                             f"\n🔧 {user_info['fishing_rob_level']} Уровень удочки"
                             "\n\n❓ СТОИМОСТЬ улучшения удочки 25000 EXP за УРОВЕНЬ."
                             " За КАЖДЫЙ новый УРОВЕНЬ ДОХОД, получаемый вами УВЕЛИЧИВАЕТСЯ вдвое,"
                             " количество уровней НЕОГРАНИЧЕНО.", attachment=photo_id)
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        return await message.answer(successfull_registration)
    
@gl.message(text="Рыбачить")
async def fishing(message: Message):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info:
        now = datetime.now()
        if user_info['last_fishing_time'] is None:
            fish_level = user_info['fishing_rob_level']
            win_dollars = fish_level*random.randint(10000,15000)
            win_exp = random.randint(100, 300)
            exp_count = user_info['exp']
            await get_fishing(user_id=user_info['id'], win_dollars=win_dollars, win_exp=win_exp, exp_count=exp_count)
            await fishing_update_cooldown(user_id=user_info['id'], new_fishing_time=now.isoformat())
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы отправились на рыбалку:"
                                f"\n\n💸 Вы заработали {win_dollars:,}$ и {win_exp:,} EXP".replace(',','.') +
                                f"\n\n❓ Чем больше уровень вашей удочки, тем больше вы можете заработать")
        else:
            if now - user_info['last_fishing_time'] < timedelta(hours=2):
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), рыбачить можно раз в 2 часа ❌")
            else:
                fish_level = user_info['fishing_rob_level']
                win_dollars = fish_level*random.randint(10000,15000)
                win_exp = random.randint(100, 300)
                exp_count = user_info['exp']
                await get_fishing(user_id=user_info['id'], win_dollars=win_dollars, win_exp=win_exp, exp_count=exp_count)
                await fishing_update_cooldown(user_id=user_info['id'], new_fishing_time=now.isoformat())
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы отправились на рыбалку:"
                                    f"\n\n💸 Вы заработали {win_dollars:,}$ и {win_exp:,} EXP".replace(',','.') +
                                    f"\n\n❓ Чем больше уровень вашей удочки, тем больше вы можете заработать")
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        return await message.answer(successfull_registration)
    

@gl.message(text="Удочка улучшить")
async def fishing(message: Message):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info:
        if user_info['exp'] < 25000:
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), у вас недостаточно EXP ❌")
        else:
            await fish_rob_upgrade(user_id=user_info['id'])
            new_fish_lvl_rob = user_info['fishing_rob_level']+1
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы улучшили удочку до {new_fish_lvl_rob} уровня 👍")
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        return await message.answer(successfull_registration)
    

@gl.message(text=['Казино', 'Азино', 'Казино <count>', 'Азино <count>'])
async def casino(message: Message, count=None):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info:
        if count is not None:
            multiplier = random.choice(multipliers)
            if count == "все":
                if user_info['balance'] <= 0:
                    await message.answer(f"@id{user_info['id']}({user_info['nickname']}), недостаточно средств ❌")
                else:
                    bet = user_info['balance']
                    if multiplier == 0:
                        await casino_lose(user_id=user_info['id'], bet=bet)
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы проиграли {int(bet):,}$ (x0) ❌".replace(',', '.'))
                    if multiplier in [0.25, 0.5, 0.75]:
                        res = bet * multiplier
                        await casino_lose(user_id=user_info['id'], bet=res)
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы проиграли {int(res):,}$ (x{multiplier}) ❌".replace(',', '.'))
                    elif multiplier == 1:
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), деньги остаются при вас 😯")
                    elif multiplier in [1.5, 2.5]:
                        res = bet * multiplier
                        await casino_win(user_id=user_info['id'], bet=res)
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы выиграли {int(res):,} (x{multiplier}) 🤑".replace(',', '.'))
            else:
                bet = await converter(count=count)
                if bet > user_info['balance']:
                    await message.answer(f"@id{user_info['id']}({user_info['nickname']}), недостаточно средств ❌")
                else:
                    if multiplier == 0:
                        await casino_lose(user_id=user_info['id'], bet=bet)
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы проиграли {int(bet):,}$ (x0) ❌".replace(',', '.'))
                    if multiplier in [0.25, 0.5, 0.75]:
                        res = bet * multiplier
                        await casino_lose(user_id=user_info['id'], bet=res)
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы проиграли {int(res):,}$ (x0) ❌".replace(',', '.'))
                    elif multiplier == 1:
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), деньги остаются при вас 😯")
                    elif multiplier in [1.5, 2.5, 3.0, 5.0, 10.0]:
                        res = bet * multiplier
                        await casino_win(user_id=user_info['id'], bet=res)
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы выиграли {int(res):,} (x{multiplier}) 🤑".replace(',', '.'))
        else:
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), использование: Казино «ставка»")
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        return await message.answer(successfull_registration)
    