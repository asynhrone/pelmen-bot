from vkbottle.bot import BotLabeler, Message, Bot
from functions import (get_user, insert_user, sell_bitcoin, sell_farm, 
                       sell_farm_all, sell_them, converter, sell_cups)
from config import successfull_registration, token, farm_prices, car_cost
import random

sl = BotLabeler()
sl.vbml_ignore_case = True
bot = Bot(token=token)

BITCOIN_COST = random.randint(1900, 3300)

@sl.message(text=["Продать биткоин", "Продать биткоин <count>"])
async def bitcoin_selling(message: Message, count=None):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info:
        if count is not None:
            if count == "все":
                if user_info['bitcoin'] == 0 or user_info['bitcoin'] is None:
                    await message.answer(f"@id{user_info['id']}({user_info['nickname']}), у вас нет биткоинов для продажи ❌")
                else:
                    count = user_info['bitcoin']
                    res = count * BITCOIN_COST
                    await sell_bitcoin(user_id=user_info['id'], count=user_info['bitcoin'], cost=BITCOIN_COST)
                    await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы продали {count:,}₿".replace(',', '.')+
                                 f" за {res:,}$".replace(',', '.')+
                                 f"\n📊 Текущий курс: {BITCOIN_COST:,}$ за 1₿".replace(',', '.'))
            else:
                count = await converter(count)
                try:
                    count_int = int(count)
                except ValueError:
                    return await message.answer(f"@id{user_info['id']}({user_info['nickname']}), неверное количество биткоинов ❌")
                if user_info['bitcoin'] != 0 and user_info['bitcoin'] is not None:
                    if int(count) > user_info['bitcoin']:
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы не можете продать больше, чем у вас есть ❌")
                    else:
                        count = user_info['bitcoin']
                        res = count * BITCOIN_COST
                        await sell_bitcoin(user_id=user_info['id'], count=user_info['bitcoin'], cost=BITCOIN_COST)
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы продали {count:,}₿".replace(',', '.')+
                                            f" за {res:,}$".replace(',', '.')+
                                            f"\n📊 Текущий курс: {BITCOIN_COST:,}$ за 1₿".replace(',', '.'))
                else:
                    await message.answer(f"@id{user_info['id']}({user_info['nickname']}), у вас нет биткоинов для продажи ❌")
        else:
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), используйте: Продать биткоин «кол-во»")
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        await message.answer(successfull_registration)


@sl.message(text=["Продать фермы", "Продать фермы <count>"])
async def farm_selling(message: Message, count=None):
    ifall = False
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info:
        farm_name = {1: "ASICminer 8 Nano Pro", 2: "Ebit E9 Plus", 3: "Miner 741", 4: "DragonMint T1"}
        farm_type = farm_name.get(user_info['farm-type']) 
        if count is not None:
            if count == "все":
                if user_info['farm-count'] == 0 or user_info['farm-count'] is None:
                    await message.answer(f"@id{user_info['id']}({user_info['nickname']}), у вас нет ферм для продажи ❌")
                else:
                    farm_type_price = farm_prices[int(user_info['farm-type'])]
                    cost = int(user_info['farm-count']) * farm_type_price / 2
                    await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы продали {int(user_info['farm-count']):,} {farm_type} за {int(cost):,}$".replace(',', '.'))
                    await sell_farm_all(user_id=user_info['id'], count=user_info['farm-count'], cost=cost)
            else:
                try:
                    count_int = int(count)
                except ValueError:
                    return await message.answer(f"@id{user_info['id']}({user_info['nickname']}), неверное количество ферм ❌")
                if user_info['farm-count'] and user_info['farm-count'] > 0:
                    if int(count) == user_info['farm-count']:
                        ifall = True
                    elif int(count) > user_info['farm-count']:
                        return await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы не можете продать больше, чем у вас есть ❌")
                    farm_type_price = farm_prices[int(user_info['farm-type'])]
                    cost = int(count) * farm_type_price / 2
                    await sell_farm(user_id=user_info['id'], count=count, cost=cost, ifall=ifall)
                    await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы продали {int(count):,} {farm_type} за {int(cost):,}$".replace(',', '.'))
                else:
                    await message.answer(f"@id{user_info['id']}({user_info['nickname']}), у вас нет ферм для продажи ❌")
        else:
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), используйте: Продать фермы «кол-во»")
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        await message.answer(successfull_registration)


@sl.message(text="Продать машину")
async def car_selling(message: Message):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info:
        if user_info['car'] is None or user_info['car'] == 0:
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), у вас нет машины ❌")
        else:
            if user_info['car'] in [9, 10]:
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы не можете продать эту машину ❌")
            else:
                product_key = str(user_info['car'])
                cost = int(car_cost.get(product_key, 0)) / 2
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы продали машину"
                                    f" за {int(cost):,}$".replace(',', '.'))
                await sell_them(user_id=user_info['id'], type='car', product=user_info['car'])
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        await message.answer(successfull_registration)


@sl.message(text=["Продать кубки", "Продать кубки <count>"])
async def selling_cups(message: Message, count=None):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info:
        if count is not None:
            if count == "все":
                if user_info['cups'] == 0 or user_info['cups'] is None:
                    await message.answer(f"@id{user_info['id']}({user_info['nickname']}), у вас нет кубков для продажи ❌")
                else:
                    count = user_info['cups']
                    if int(count) < 0:
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы не можете продать кубки, если у вас минусовое количество ❌")
                    else:
                        res = 15000 * int(count)
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы продали {int(user_info['cups']):,} кубков за {int(res):,}$".replace(',', '.'))
                        await sell_cups(user_id=user_info['id'], count=user_info['cups'])
            else:
                count = await converter(count)
                try:
                    count_int = int(count)
                except ValueError:
                    return await message.answer(f"@id{user_info['id']}({user_info['nickname']}), неверное количество кубков ❌")
                if user_info['cups'] != 0:
                    if int(user_info['cups']) < 0:
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы не можете продать кубки, если у вас минусовое количество ❌")
                    elif int(count) > user_info['cups']:
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы не можете продать больше, чем у вас есть ❌")
                    else:
                        res = 15000 * int(count)
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы продали {int(count):,} кубков за {int(res):,}$".replace(',', '.'))
                        await sell_cups(user_id=user_info['id'], count=count)
                else:
                    await message.answer(f"@id{user_info['id']}({user_info['nickname']}), у вас нет кубков для продажи ❌")
        else:
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), используйте: Продать кубки «кол-во»")
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        await message.answer(successfull_registration)