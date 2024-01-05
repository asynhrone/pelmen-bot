from vkbottle.bot import BotLabeler, Message, Bot
from functions import get_user, insert_user, buy_them
from config import successfull_registration, token, flat_cost, car_cost, yacht_cost

shl = BotLabeler()
shl.vbml_ignore_case = True
bot = Bot(token=token)

@shl.message(text=["Магазин"])
async def shop(message: Message, type=None, number=None):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info: 
        return await message.answer(f"@id{user_info['id']}({user_info['nickname']}), магазин:"
                "\n\n🏬 Квартиры"
                "\n🚗 Машины"
                "\n🛥️ Яхты"
                "\n\n🛒 Для просмотра категории используйте: Квартиры")  
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        return await message.answer(successfull_registration)
    

@shl.message(text=["Квартиры", "Квартиры <number:int>"])
async def flats(message: Message, number=None):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info: 
        if number is not None:
            suffix = {"1": "квартиру в хрущевке", "2": "квартиру в центре Челябинска", "3": "квартиру на окраине Питера", "4": "квартиру в центре Москвы", "5": "квартиру в Нью-Йорке", "6": "квартиру в сердце Пекина", "7": "квартиру в Odeon Tower"}
            if number <= 0 or number > 7:
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), неверный номер квартиры ❌")
            elif int(flat_cost.get(str(number), 0)) > user_info["balance"]:
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), недостаточно средств❌")
            elif user_info["flat"] is not None and user_info["flat"] != 0:
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), у вас уже есть квартира❌")
            else:
                price = flat_cost.get(str(number))
                await buy_them(user_id=user_info['id'], type='flat', product=number)
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы купили {suffix.get(str(number))} за {int(price):,}$ 🥳".replace(',', '.'))
        else:
            return await message.answer(f"@id{user_info['id']}({user_info['nickname']}), квартиры:"
                "\n\n1. Квартира в хрущевке - 25.000$"
                "\n2. Квартира в центре Челябинска - 1.000.000$"
                "\n3. Квартира на окраине Питера - 50.000.000.000"
                "\n4. Квартира в центре Москвы - 300.000.000.000.000$"
                "\n5. Квартира в Нью-Йорке - 500.000.000.000.000$"
                "\n6. Квартира в сердце Пекина - 750.000.000.000.000"
                "\n7. Квартира в Odeon Tower - 3.000.000.000.000.000$"
                "\n\n🛒 Для покупки используйте: Квартиры «номер»")  
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        return await message.answer(successfull_registration)
    

@shl.message(text=["Машины", "Машины <number:int>"])
async def cars(message: Message, number=None):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info: 
        if number is not None:
            suffix = {"1": "Nissan Pathfinder", "2": "Mazda 6", "3": "Mercedes-Benz CLS", "4": "Audi R8", 
                      "5": "Ferrari 458 Italia", "6": "Mercedes-Benz Pullman", "7": "Rolls-Royce Sweptail", "8": "Bugatti Bolide"}
            if number <= 0 or number > 8:
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), неверный номер машины ❌")
            elif int(car_cost.get(str(number), 0)) > user_info["balance"]:
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), недостаточно средств❌")
            elif user_info["car"] is not None and user_info["car"] != 0:
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), у вас уже есть машина❌")
            else:
                price = car_cost.get(str(number))
                await buy_them(user_id=user_info['id'], type='car', product=number)
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы купили {suffix.get(str(number))} за {int(price):,}$ 🥳".replace(',', '.'))
        else:
            return await message.answer(f"@id{user_info['id']}({user_info['nickname']}), машины:"
                "\n\n1. Nissan Pathfinder - 10.000.000.000$"
                "\n2. Mazda 6 - 1.000.000.000.000$"
                "\n3. Mercedes-Benz CLS - 10.000.000.000.000$"
                "\n4. Audi R8 - 25.000.000.000.000$"
                "\n5. Ferrari 458 Italia - 250.000.000.000.000$"
                "\n6. Mercedes-Benz Pullman - 900.000.000.000.000$"
                "\n7. Rolls-Royce Sweptail - 1.200.000.000.000.000$"
                "\n8. Bugatti Bolide - 3.000.000.000.000.000$"
                "\n\n🛒 Для покупки используйте: Машины «номер»")  
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        return await message.answer(successfull_registration)
    

@shl.message(text=["Яхты", "Яхты <number:int>"])
async def yachts(message: Message, number=None):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info: 
        if number is not None:
            suffix = {"1": "Seven Seas", "2": "Octopus", "3": "Lady Moura", "4": "Al Mirqab", 
                      "5": "Eclipse", "6": "Histoty SUPREMEE"}
            if number <= 0 or number > 6:
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), неверный номер машины ❌")
            elif int(yacht_cost.get(str(number), 0)) > user_info["balance"]:
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), недостаточно средств❌")
            elif user_info["yacht"] is not None and user_info["yacht"] != 0:
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), у вас уже есть машина❌")
            else:
                price = yacht_cost.get(str(number))
                await buy_them(user_id=user_info['id'], type='yacht', product=number)
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы купили {suffix.get(str(number))} за {int(price):,}$ 🥳".replace(',', '.'))
        else:
            return await message.answer(f"@id{user_info['id']}({user_info['nickname']}), яхты:"
                "\n\n1. Seven Seas - 1.000.000$"
                "\n2. Octopus - 10.000.000$"
                "\n3. Lady Moura - 70.000.000$"
                "\n4. Al Mirqab - 250.000.000$"
                "\n5. Eclipse - 2.500.000.000$"
                "\n6. Histoty SUPREMEE - 30.000.000.000$"
                "\n\n🛒 Для покупки используйте: Яхты «номер»")  
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        return await message.answer(successfull_registration)