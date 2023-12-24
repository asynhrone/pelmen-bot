from vkbottle.bot import BotLabeler, Message, Bot
from functions import get_user, converter, set_them, bot_get_user
from config import token
from datetime import datetime, timedelta
import time

al = BotLabeler()
al.vbml_ignore_case = True
bot = Bot(token=token)

@al.message(text="Состояние")
async def monitoring(message: Message):
    user = await bot.api.users.get(message.from_id)
    start_time = time.time()
    user_info = await get_user(user_id=user[0].id)
    if user_info['status'] in ['Владелец', 'Управляющий']:
        end_time = time.time()
        ping_time = round(end_time - start_time, 3)
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
        photo_id = "photo-222672748_456239022_acd808e85b126ec97c"
        await message.answer(f"@id{user_info['id']}({user_info['nickname']}), строка состояния:"
                             f"\n\n⌛ {current_time}"
                             f"\n🧭 Пинг: {ping_time} мс."
                             "\n🔔 Статус: Запущен.", attachment=photo_id)
    else:
        return
    

@al.message(text=["Установить", "Установить <type> <count> <userid>"])
async def set(message: Message, type=None,count=None, userid=None):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info['status'] in ['Владелец', 'Управляющий']:
        if type is not None and count is not None and userid is not None:
            if type in ['Баланс', 'баланс']:
                type = 'balance'
                userid = await bot_get_user(user_id=userid)
                count = await converter(count=count)
                await set_them(user_id=userid['id'], type=type, count=count)
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы установили @id{userid['id']}({userid['nickname']})"
                                     f" {count:,}$ ✅".replace(',', '.'))
            if type in ['EXP', 'exp', 2]:
                type = 'exp'
                userid = await bot_get_user(user_id=userid)
                count = await converter(count=count)
                await set_them(user_id=userid['id'], type=type, count=count)
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы установили @id{userid['id']}({userid['nickname']})"
                                     f" {count:,} EXP ✅".replace(',', '.'))
            if type in ['Удочка', 'удочка', 'Удочку', 'удочку']:
                type = 'fishing_rob_level'
                userid = await bot_get_user(user_id=userid)
                count = await converter(count=count)
                await set_them(user_id=userid['id'], type=type, count=count)
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы установили @id{userid['id']}({userid['nickname']})"
                                     f" удочку {count:,} LVL ✅".replace(',', '.'))
            if type in ['Биткоин', 'биткоин']:
                type = 'bitcoin'
                userid = await bot_get_user(user_id=userid)
                count = await converter(count=count)
                await set_them(user_id=userid['id'], type=type, count=count)
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы установили @id{userid['id']}({userid['nickname']})"
                                     f" {count:,}₿ ✅".replace(',', '.'))
            if type in ['Ник', 'ник']:
                type = 'nickname'
                userid = await bot_get_user(user_id=userid)
                await set_them(user_id=userid['id'], type=type, count=count)
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы установили @id{userid['id']}({userid['nickname']})"
                                     f" ник {count} ✅")
        else:
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), доступные установки:"
                                 "\n\n1. Баланс"
                                 "\n2. EXP"
                                 "\n3. Удочка"
                                 "\n4. Биткоин"
                                 "\n5. Ник"
                                 "\n\n❓ Пример: установить «баланс» «сумма» «id»")
    else:
        return