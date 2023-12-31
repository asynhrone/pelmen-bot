from vkbottle.bot import BotLabeler, Message, Bot
from functions import (get_user, insert_user, insert_newnickname, get_top_users_by_them, 
                       format_number, get_user_place_in_top, update_user_bonus_time, 
                       bonus_get, race_update_cups, race_update_cooldown, get_users_by_them,
                       get_random_user, generate_profile_image, bot_get_user,
                       converter, transfer_money)
from config import successfull_registration, token, phrases, emoji_dict
import random, asyncio
from datetime import datetime, timedelta

ul = BotLabeler()
ul.vbml_ignore_case = True
bot = Bot(token=token)

@ul.message(text='Помощь')
async def help(message: Message):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info: 
        return await message.answer(f"@id{user_info['id']}({user_info['nickname']}), мои команды:"
                                    "\n\n📚 Основное:"
                                    "\nㅤ📙 Профиль"
                                    "\nㅤ📊 Топ"
                                    "\nㅤ✏️ Ник"
                                    "\nㅤ🔖 Продать [Предмет]"
                                    "\nㅤ🛒 Магазин"
                                    "\nㅤ💵 Перевести [ID]  [Сумма]"
                                    "\n\n💸 Заработок:"
                                    "\nㅤ🎁 Бонус"
                                    "\nㅤ⛱️ Рыбалка"
                                    "\nㅤ💽 Майнинг"
                                    "\nㅤ🚖 Таксовать"
                                    "\n\n🌈 Равзлечения:"
                                    "\nㅤ🏁 Гонка"
                                    "\nㅤ🎰 Казино [Ставка]")
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        return await message.answer(successfull_registration)
    

@ul.message(text=['Профиль', 'Проф'])
async def profile(message: Message):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info:
        farm_name = {1: "ASICminer 8 Nano Pro", 2: "Ebit E9 Plus", 3: "Miner 741", 4: "DragonMint T1"}
        farm_type = farm_name.get(user_info['farm-type']) 
        display_status = f"🔥 {user_info['status']}" if user_info['status'] != "Пользователь" else ''
        display_status = display_status.strip() 
        exp = user_info['exp'] if user_info['exp'] is not None else 0

        display_property = "\n\n🔑 Имущество:"
        if 'flat' in user_info and user_info['flat'] is not None:
            flat = {"1": "Квартира в хрущевке", "2": "Квартира в центре Челябинска", "3": "Квартира на окраине Питера",
                    "4": "Квартира в центре Москвы", "5": "Квартира в Нью-Йорке", "6": "Квартира в сердце Пекина",
                    "7": "Квартира в Odeon Tower", "8": "Сарай"}
            flat_description = flat.get(str(user_info['flat']), '')
            if flat_description:  # Проверка, что описание квартиры существует
                display_property += f"\nㅤ🏬 {flat_description}"

        if 'farm-count' in user_info and user_info['farm-count']:
            # Переменная `farm_type` должна быть определена где-то в вашем коде.
            display_property += f"\nㅤ🔋 Ферма: {farm_type} ({user_info['farm-count']:,} шт.)".replace(',', '.')

        if 'car' in user_info and user_info['car'] is not None:
            car = {"1": "Nissan Pathfinder", "2": "Mazda 6", "3": "Mercedes-Benz CLS",
                    "4": "Audi R8", "5": "Ferrari 458 Italia", "6": "Mercedes-Benz Pullman",
                    "7": "Rolls-Royce Sweptail", "8": "Bugatti Bolide", "9": "Aurus Senat Limousine", "10": "Новогодний унитаз 🌲"}
            car_description = car.get(str(user_info['car']), '')
            if car_description:  # Проверка, что описание автомобиля существует
                display_property += f"\nㅤ🚗 {car_description}"

        if 'yacht' in user_info and user_info['yacht'] is not None:
            yacht = {"1": "Seven Seas", "2": "Octopus", "3": "Lady Moura", "4": "Al Mirqab", 
                      "5": "Eclipse", "6": "Histoty SUPREMEE", "7": "Баранка"}
            yacht_description = yacht.get(str(user_info['yacht']), '')
            if yacht_description:  # Проверка, что описание автомобиля существует
                display_property += f"\nㅤ🛥️ {yacht_description}"

        if display_property == "\n🔑 Имущество:":
            display_property += '\nㅤㅤПусто'

        profile_message = (
            f"@id{user_info['id']}({user_info['nickname']}), ваш профиль:"
            f"\n\n🔎 ID: {user_info['bot_id']}" +
            (f"\n{display_status}" if display_status else "") +
            f"\n🏆 {user_info['cups']} Кубков"
            f"\n💸 Баланс: {user_info['balance']:,}$".replace(',', '.') +
            f"\n⭐ {exp:,} EXP".replace(',', '.') +
            f"\n💽 Биткоины: {user_info['bitcoin']:,}₿".replace(',', '.') +
            display_property
        )
        attachment = await generate_profile_image(flat=user_info['flat'], car=user_info['car'])
        return await message.answer(profile_message, attachment=attachment)

    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        return await message.answer(successfull_registration)
    

@ul.message(text="Баланс")
async def balance(message: Message):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info:
        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), баланс:"
                             f"\n\n💸 Баланс: {user_info['balance']:,}$".replace(',', '.') +
                             f"\n💽 Биткоины: {user_info['bitcoin']:,}₿".replace(',', '.'))
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        return await message.answer(successfull_registration)
    

@ul.message(text=['Ник', 'Ник <newnickname>'])
async def changenickname(message: Message, newnickname=None):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info:
        if not newnickname:
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), "
                        "используйте: ник «новый ник»")
        else:
            if len(newnickname) > 32:
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), "
                    "никнейм не должен быть длиннее 32 символов ❌")
            elif len(newnickname) < 3:
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), "
                    "никнейм не должен быть короче 3 символов ❌")
            else:
                random_phrase = random.choice(list(phrases.values()))
                await insert_newnickname(user_id=user[0].id, newnickname=newnickname)
                return await message.answer(f"@id{user_info['id']}({newnickname}), " + random_phrase)
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        return await message.answer(successfull_registration)
    

@ul.message(text=["Топ", "Топ <type>"])
async def top(message: Message, type=None):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info:
        if type in ["баланс", "по балансу"]:
            top_users = await get_top_users_by_them(type='balance')
            user_place = await get_user_place_in_top(user_info['id'], top_users)
            top_users_str = "\n".join([f"{emoji_dict[str(i+1)]} @id{user[0]}({user[1]}) | ${format_number(user[2])}" for i, user in enumerate(top_users)])
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), топ 10 пользователей по балансу:\n\n{top_users_str}\n\n➡{emoji_dict[str(user_place)]} @id{user_info['id']}({user_info['nickname']}) | ${format_number(user_info['balance'])}")
        elif type in ["удочка", "по удочке"]:
            top_users = await get_top_users_by_them(type='fishing_rob_level')
            user_place = await get_user_place_in_top(user_info['id'], top_users)
            top_users_str = "\n".join([f"{emoji_dict[str(i+1)]} @id{user[0]}({user[1]}) | LVL {format_number(user[2])}" for i, user in enumerate(top_users)])
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), топ 10 пользователей по уровню удочки:\n\n{top_users_str}\n\n➡{emoji_dict[str(user_place)]} @id{user_info['id']}({user_info['nickname']}) | LVL {format_number(user_info['fishing_rob_level'])}")
        else:
            photo_id = "photo-222672748_456239024_acb7a0d480f3dec3fe"
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), доступные топы:"
                    "\n\n1. По балансу (баланс)"
                    "\n2. По удочке (удочка)"
                    "\n\n❓ Используйте: Топ «баланс»", attachment=photo_id)
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        return await message.answer(successfull_registration)


@ul.message(text="Бонус")
async def bonus(message: Message):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    price = random.randint(1000, 100000)
    exp = random.randint(100, 500)
    if user_info:
        now = datetime.now()
        if user_info['last_bonus_time'] is None:
            exp_count = user_info['exp']
            await bonus_get(user_id=user_info['id'], price=price, price_exp=exp, exp_count=exp_count)
            await update_user_bonus_time(user_id=user_info['id'], last_bonus_time=now.isoformat())
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), держите бонус {price:,}$ и {exp:,} EXP 😎".replace(',', '.'))
        else:   
            if now - user_info['last_bonus_time'] < timedelta(hours=24):
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), бонус доступен лишь раз в 24 часа ❌")
            else:
                exp_count = user_info['exp']
                await bonus_get(user_id=user_info['id'], price=price, price_exp=exp, exp_count=exp_count)
                await update_user_bonus_time(user_id=user_info['id'], last_bonus_time=now.isoformat())
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), держите бонус {price:,}$ и {exp:,} EXP 😎".replace(',', '.'))
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name) 
        await message.answer(successfull_registration)


@ul.message(text="Гонка")
async def race(message: Message):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    now = datetime.now()
    if user_info:
        if user_info['car'] is None or user_info['car'] == 0:
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), у вас нет машины ❌")
        else:
            if user_info['last_race_time'] is None or now - user_info['last_race_time'] > timedelta(minutes=20):
                users_with_cars = await get_users_by_them(type='car')
                opponent = await get_random_user(users=users_with_cars, excluded_user_id=user_info['id'])
                sent_message = await message.answer(
                    f"@id{user_info['id']}({user_info['nickname']}), вы начали гонку против @id{opponent['id']}({opponent['nickname']}) 🏁\n\n⌛ Результаты через 4"
                )
                if int(user_info['car']) > int(opponent['car']):
                    for i in reversed(range(-1, 3)):
                        await asyncio.sleep(1)
                        new_text = f"@id{user_info['id']}({user_info['nickname']}), вы начали гонку против @id{opponent['id']}({opponent['nickname']}) 🏁\n\n⌛ Результаты через {i+1}"
                        await bot.api.messages.edit(
                            peer_id=sent_message.peer_id,
                            message=new_text,
                            **{
                                attr: getattr(sent_message, attr)
                                for attr in ['message_id', 'conversation_message_id']
                                if hasattr(sent_message, attr) and getattr(sent_message, attr)
                            }
                        )
                    new_text = f"@id{user_info['id']}({user_info['nickname']}), гонка против @id{opponent['id']}({opponent['nickname']}) завершена 🏁\n\n 🥇 Вы пришли к финишу первым! +100 🏆"
                    await race_update_cooldown(user_id=user_info['id'], new_race_time=now.isoformat())
                    await race_update_cups(user_id=user_info['id'],operation='+', count=100, cups=user_info['cups'])
                    await bot.api.messages.edit(
                        peer_id=sent_message.peer_id,
                        message=new_text,
                        **{
                            attr: getattr(sent_message, attr)
                            for attr in ['message_id', 'conversation_message_id']
                            if hasattr(sent_message, attr) and getattr(sent_message, attr)
                        }
                    )
                    await message.answer(sticker_id=83931)
                    return
                elif int(user_info['car']) < int(opponent['car']):
                    for i in reversed(range(-1, 3)):
                        await asyncio.sleep(1)
                        new_text = f"@id{user_info['id']}({user_info['nickname']}), вы начали гонку против @id{opponent['id']}({opponent['nickname']}) 🏁\n\n⌛ Результаты через {i+1}"
                        await bot.api.messages.edit(
                            peer_id=sent_message.peer_id,
                            message=new_text,
                            **{
                                attr: getattr(sent_message, attr)
                                for attr in ['message_id', 'conversation_message_id']
                                if hasattr(sent_message, attr) and getattr(sent_message, attr)
                            }
                        )
                    new_text = f"@id{user_info['id']}({user_info['nickname']}), гонка против @id{opponent['id']}({opponent['nickname']}) завершена 🏁\n\n 🥈 Противник пришел к финишу первым! -100 🏆"
                    await race_update_cooldown(user_id=user_info['id'], new_race_time=now.isoformat())
                    await race_update_cups(user_id=user_info['id'],operation='-', count=100, cups=user_info['cups'])
                    await bot.api.messages.edit(
                        peer_id=sent_message.peer_id,
                        message=new_text,
                        **{
                            attr: getattr(sent_message, attr)
                            for attr in ['message_id', 'conversation_message_id']
                            if hasattr(sent_message, attr) and getattr(sent_message, attr)
                        }
                    )
                    await message.answer(sticker_id=83936)
                    return
                else:
                    for i in reversed(range(-1, 3)):
                        await asyncio.sleep(1)
                        new_text = f"@id{user_info['id']}({user_info['nickname']}), вы начали гонку против @id{opponent['id']}({opponent['nickname']}) 🏁\n\n⌛ Результаты через {i+1}"
                        await bot.api.messages.edit(
                            peer_id=sent_message.peer_id,
                            message=new_text,
                            **{
                                attr: getattr(sent_message, attr)
                                for attr in ['message_id', 'conversation_message_id']
                                if hasattr(sent_message, attr) and getattr(sent_message, attr)
                            }
                        )
                    new_text = f"@id{user_info['id']}({user_info['nickname']}), гонка против @id{opponent['id']}({opponent['nickname']}) завершена 🏁\n\n 🥈 Вы свели счет в ничью! +0 🏆"
                    await race_update_cooldown(user_id=user_info['id'], new_race_time=now.isoformat())
                    await bot.api.messages.edit(
                        peer_id=sent_message.peer_id,
                        message=new_text,
                        **{
                            attr: getattr(sent_message, attr)
                            for attr in ['message_id', 'conversation_message_id']
                            if hasattr(sent_message, attr) and getattr(sent_message, attr)
                        }
                    )
                    await message.answer(sticker_id=79410)
                    return
            else:
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), участвовать в гонке можно раз в 20 минут ❌")
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name)
        await message.answer(successfull_registration)


@ul.message(text=["Перевести", "Перевести <id> <count>"])
async def transfer(message: Message, id=None, count=None):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info:
        if id is not None:
            if count is not None:
                opponent = await bot_get_user(user_id=id)
                if opponent:
                    count = await converter(count)
                    if count > user_info['balance']:
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), у вас недостаточно средств ❌")
                    if count > 50000000 and user_info['status'] not in ["VIP", "ELITE", "Администратор", "Управляющий", "Владелец"]:
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы не можете переводить больше 50 миллионов за одну операцию❌\n\n✨ Для увеличения лимита необходимо приобрести VIP-статус.")
                    elif count > 100000000 and user_info['status'] not in ["ELITE", "Администратор", "Управляющий", "Владелец"]:
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы не можете переводить больше 100 миллионов за одну операцию❌\n\n✨ Для увеличения лимита необходимо приобрести ELITE-статус.")
                    elif count > 200000000 and user_info['status'] not in ["Администратор", "Управляющий", "Владелец"]:
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы не можете переводить больше 200 миллионов за одну операцию❌\n\n✨ Для увеличения лимита необходимо приобрести статус Администратора.")
                    else:
                        await transfer_money(user_id=user_info['id'], operation='-', count=count)
                        await transfer_money(user_id=opponent['id'], operation='+', count=count)
                        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы перевели @id{opponent['id']}({opponent['nickname']}) {count:,}$ ✅".replace(',', '.'))
                        message = f"@id{user_info['id']}({user_info['nickname']}) перевел вам {count:,}$ 😎".replace(',', '.')
                        await bot.api.messages.send(user_id=opponent['id'], random_id=0, message=message)
                        await bot.api.messages.send(user_id=opponent['id'], random_id=0, sticker_id=21099)
                else:
                    await message.answer(f"@id{user_info['id']}({user_info['nickname']}), такого пользователя не существует❌")
            else:
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), использование: Перевести «ID» «сумма»❌")
        else:
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), использование: Перевести «ID» «сумма»❌")
    else:
        await insert_user(user_id=user[0].id, first_name=user[0].first_name)
        await message.answer(successfull_registration)