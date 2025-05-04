from vkbottle.bot import BotLabeler, Message, Bot
from functions import (get_user, insert_user, get_fishing, fishing_update_cooldown, 
                       fish_rob_upgrade, converter, casino_win, casino_lose)
from config import (successfull_registration, token, multipliers, weights, limits)
import random
from random import choice
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
            win_dollars = fish_level*random.randint(100000, 1500000)
            win_exp = random.randint(1000, 3000)
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
                win_dollars = fish_level*random.randint(100000, 1500000)
                win_exp = random.randint(1000, 3000)
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
    user_id = message.from_id
    user_info = await get_user(user_id=user_id)

    if not user_info:
        user = (await bot.api.users.get(user_id))[0]
        await insert_user(user_id=user_id, first_name=user[0].first_name)
        return await message.answer(successfull_registration)

    if count is None:
        return await message.answer(f"@id{user_info['id']}({user_info['nickname']}), использование: Казино «ставка»")

    balance = user_info['balance']
    if count in ["все", "вобанк", "вабанк", "во банк", "ва банк"]:
        bet = balance
    else:
        bet = await converter(count=count)

    if bet <= 0 or bet > balance:
        return await message.answer(f"@id{user_info['id']}({user_info['nickname']}), недостаточно средств ❌")

    multiplier = random.choices(multipliers, weights=weights, k=1)[0]
    result_msg = ""
    res = bet * multiplier 
    balance = user_info['balance']
    
    limit = limits.get(user_info['status'], float('inf'))  
    
    if multiplier == 0:
        await casino_lose(user_id=user_info['id'], bet=bet)
        result_msg = f"вы проиграли {int(bet):,}$ (x0) ❌"
    else:
        new_balance = res + balance
        if new_balance > limit:  
            res = limit - balance  
            
        if multiplier < 1:
            await casino_lose(user_id=user_info['id'], bet=res)
            result_msg = f"вы проиграли {int(res):,}$ (x{multiplier}) ❌"
        elif multiplier == 1:
            result_msg = "деньги остаются при вас (x1) 😯 "
        else:
            await casino_win(user_id=user_info['id'], bet=res)
            result_msg += f"вы выиграли {int(res):,}$ (x{multiplier}) 🤑"

    await message.answer(f"@id{user_info['id']}({user_info['nickname']}), {result_msg}".replace(',', '.'))
