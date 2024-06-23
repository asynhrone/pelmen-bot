from vkbottle.bot import BotLabeler, Message, Bot
from functions import (get_user, insert_user, update_mining_shop,
                       bitcoin_mine, update_user_mining_time)
from config import *
import random
from datetime import datetime, timedelta

ml = BotLabeler()
ml.vbml_ignore_case = True
bot = Bot(token=token)

@ml.message(text='Майнинг')
async def mining_page(message: Message):
    global BITCOIN_COST
    photo_id = 'photo-222672748_456239020_d3be635b2f96c5b846'
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info:
        if user_info['farm-count'] == 0 or user_info['farm-count'] is None:
            display_redirect = "🔋 У вас нет майниговых ферм. Для приобретения, воспользуйтесь командой «Фермы»."
        else:
            farm_type = farm_name.get(user_info['farm-type']) 
            gen_income = int(farm_income[user_info['farm-type']]) * user_info['farm-count'] #general income
            display_redirect = (f"\n🔋 Ферма {farm_type} ({user_info['farm-count']:,} шт.)".replace(',', '.')+
                                f"\n💸 Общая доходность: {gen_income:,}₿".replace(',', '.')+
                                "\n\n⭐ Чтобы начать майнить, введите «Майнить».")
        
        new_cost = random.randint(1900, 3300)
        display_cost = "📈 " if new_cost > BITCOIN_COST else "📉 "
        BITCOIN_COST = new_cost
        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), майнинговая страница:"
                             f"\n\n{display_redirect}"
                             f"\n\n{display_cost} Курс: 1₿ = {new_cost:,}$".replace(',', '.'), attachment=photo_id)
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        return await message.answer(successfull_registration)
    

@ml.message(text=['Фермы', 'Фермы <number:int> <count:int>'])
async def mining_shop(message: Message, number=None, count=None):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    farm_name = {1: "ASICminer 8 Nano Pro", 2: "Ebit E9 Plus", 3: "Miner 741", 4: "DragonMint T1"}
    if user_info:
        if number is not None and count is not None:
            price = farm_prices.get(number, 0) * count
            price = int(price)

            if int(number) < 1 or int(number) > 4:
                return await message.answer(f"@id{user_info['id']}({user_info['nickname']}), неверный тип ферм ❌")
            if int(count) <= 0:
                return await message.answer(f"@id{user_info['id']}({user_info['nickname']}), неверное количество ферм ❌") 
            if user_info['farm-type'] is None or user_info['farm-type'] == 0:
                if int(count) > 3000:
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы не можете купить больше 3000 ферм❌")
                else:
                    await update_mining_shop(user_id=user_info['id'], number=number, balance=user_info['balance'], price=price, count=count)
                    return await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы купили {count} ферм {farm_name.get(number)}")
            else:
                if (user_info['balance']) < price:
                    return await message.answer(
                        f"@id{user_info['id']}({user_info['nickname']}), у вас недостаточно средств для покупки {count} {farm_name.get(number, 'ферм')} ❌"
                    )
                if user_info['farm-type'] != number: 
                    return await message.answer(
                        f"@id{user_info['id']}({user_info['nickname']}), вы уже купили ферму типа {farm_name.get(user_info['farm-type'])}, покупка ферм другого типа невозможна ❌"
                    )
                else:
                    if int(count) > 3000:
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы не можете купить больше 3000 ферм❌")
                    elif user_info['farm-count'] + count > 3000:
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы не можете иметь больше 3000 ферм❌")
                    else:
                        await update_mining_shop(user_id=user_info['id'], number=number, balance=user_info['balance'], price=price, count=int(count))
                        return await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы купили {count} ферм {farm_name.get(number)}")
        else:
            return await message.answer(f"@id{user_info['id']}({user_info['nickname']}), майнинг-магазин:"
                                "\n\n1. 🔋 ASICminer 8 Nano Pro (1₿) - 3.000.000$"
                                "\n2. 🔋 Ebit E9 Plus (50₿) - 7.000.000.000$"
                                "\n3. 🔋 Miner 741 (1000₿) - 120.000.000.000.000$"
                                "\n4. 💠 DragonMint T1 (3000₿) - 300.000.000.000.000$"
                                "\n\n🛒 Для покупки используйте: Фермы «1-4» «кол-во»")
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        return await message.answer(successfull_registration)
    

@ml.message(text='Майнить')
async def mining(message: Message):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info:
        if user_info['farm-count'] == 0:
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), у вас нет ферм для майнинга ❌")
        else:
            now = datetime.now()
            if user_info['last_mining_time'] is None:
                bitcoin_earned = int(user_info['farm-count']) * int(farm_income[user_info['farm-type']])
                await update_user_mining_time(user_id=user_info['id'], last_mining_time=now.isoformat())
                await bitcoin_mine(user_id=user_info['id'], bitcoin_earned=bitcoin_earned)
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы заработали {bitcoin_earned:,}₿".replace(',', '.'))
            else:   
                if now - user_info['last_mining_time'] < timedelta(hours=8):
                    await message.answer(f"@id{user_info['id']}({user_info['nickname']}), майнить крипту можно раз в 8 часов ❌")
                else:
                    bitcoin_earned = int(user_info['farm-count']) * int(farm_income[user_info['farm-type']])
                    await update_user_mining_time(user_id=user_info['id'], last_mining_time=now.isoformat())
                    await bitcoin_mine(user_id=user_info['id'], bitcoin_earned=bitcoin_earned)
                    await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы заработали {bitcoin_earned:,}₿".replace(',', '.'))
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        await message.answer(successfull_registration)
