from vkbottle.bot import BotLabeler, Message, Bot
from functions import (get_user, converter, set_them, bot_get_user, get_reports, close_report,
                       get_user_by_report_id, get_admins)
from config import token, emoji_dict
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
    

@al.message(text=["Установить", "Установить <type> <userid> <count>"])
async def set(message: Message, type=None, userid=None,count=None):
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
                text_to_send = f"🆘 Администратор @id{user_info['id']}({user_info['nickname']}) установил @id{userid['id']}({userid['nickname']}) баланс в {count}$"
                await bot.api.messages.send(user_id="507577425", random_id=0, message=text_to_send)
            if type in ['EXP', 'exp', 2]:
                type = 'exp'
                userid = await bot_get_user(user_id=userid)
                count = await converter(count=count)
                await set_them(user_id=userid['id'], type=type, count=count)
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы установили @id{userid['id']}({userid['nickname']})"
                                     f" {count:,} EXP ✅".replace(',', '.'))
                text_to_send = f"🆘 Администратор @id{user_info['id']}({user_info['nickname']}) установил @id{userid['id']}({userid['nickname']}) {count} EXP"
                await bot.api.messages.send(user_id="507577425", random_id=0, message=text_to_send)
            if type in ['Удочка', 'удочка', 'Удочку', 'удочку']:
                type = 'fishing_rob_level'
                userid = await bot_get_user(user_id=userid)
                count = await converter(count=count)
                await set_them(user_id=userid['id'], type=type, count=count)
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы установили @id{userid['id']}({userid['nickname']})"
                                     f" удочку {count:,} LVL ✅".replace(',', '.'))
                text_to_send = f"🆘 Администратор @id{user_info['id']}({user_info['nickname']}) установил @id{userid['id']}({userid['nickname']}) {count} LVL удочки"
                await bot.api.messages.send(user_id="507577425", random_id=0, message=text_to_send)
            if type in ['Биткоин', 'биткоин']:
                type = 'bitcoin'
                userid = await bot_get_user(user_id=userid)
                count = await converter(count=count)
                await set_them(user_id=userid['id'], type=type, count=count)
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы установили @id{userid['id']}({userid['nickname']})"
                                     f" {count:,}₿ ✅".replace(',', '.'))
                text_to_send = f"🆘 Администратор @id{user_info['id']}({user_info['nickname']}) установил @id{userid['id']}({userid['nickname']}) биткоин баланс {count}₿"
                await bot.api.messages.send(user_id="507577425", random_id=0, message=text_to_send)
            if type in ['Ник', 'ник']:
                type = 'nickname'
                userid = await bot_get_user(user_id=userid)
                await set_them(user_id=userid['id'], type=type, count=count)
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы установили @id{userid['id']}({userid['nickname']})"
                                     f" ник {count} ✅")
                text_to_send = f"🆘 Администратор @id{user_info['id']}({user_info['nickname']}) установил @id{userid['id']}({userid['nickname']}) ник {count}"
                await bot.api.messages.send(user_id="507577425", random_id=0, message=text_to_send)
            if type in ['Статус', 'статус']:
                type = 'status'
                userid = await bot_get_user(user_id=userid)
                await set_them(user_id=userid['id'], type=type, count=count)
                await message.answer(f"@id{user_info['id']}({user_info['nickname']}), вы установили @id{userid['id']}({userid['nickname']})"
                                     f" ник {count} ✅")
                text_to_send = f"🆘 Администратор @id{user_info['id']}({user_info['nickname']}) установил @id{userid['id']}({userid['nickname']}) статус {count}"
                await bot.api.messages.send(user_id="507577425", random_id=0, message=text_to_send)
        else:
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), доступные установки:"
                                 "\n\n1. Баланс"
                                 "\n2. EXP"
                                 "\n3. Удочка"
                                 "\n4. Биткоин"
                                 "\n5. Ник"
                                 "\n6. Статус"
                                 "\n\n❓ Пример: установить «баланс» «id» «сумма»")
    else:
        return
    

@al.message(text="Репорты")
async def reports(message: Message):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info['status'] in ['Администратор', 'Владелец', 'Управляющий']:
        reports = await get_reports()
        if reports:
            reports_str_list = []
            for report in reports:
                report_user = await get_user(user_id=report['author'])
                reports_str = f"Репорт #️{report['id']} | От @id{report['author']}({report_user['nickname']}) | Создан {report['created']}\n💬 {report['text']}\n---"
                reports_str_list.append(reports_str)
                reports_str_joined = "\n".join(reports_str_list)
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), список репортов:\n\n" + reports_str_joined + f"\n\n❓ Для ответа на репорт, используйте: Ответить «ID» «текст»")
        else:
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), нет активных репортов.")
    else:
        return
    

@al.message(text=["Ответить", "Ответить <id> <text>"])
async def reports(message: Message, id=None, text=None):
    user = await bot.api.users.get(message.from_id)
    user_info = await get_user(user_id=user[0].id)
    if user_info['status'] in ['Администратор', 'Владелец', 'Управляющий']:
        if id and text is not None:
            try:
                vuser = await get_user_by_report_id(report_id=id)
            except:
                 await message.answer("Такого репорта не существует.")
            finally:
                if vuser is None:
                    await message.answer("Ошибка получения данных о пользователе репорта.")
                    return

            user_nickname = user_info.get('nickname', f"id{user_info['id']}")
            vuser_nickname = vuser.get('nickname', f"id{vuser['id']}")

            answer_message = f"@id{user_info['id']}({user_nickname}), вы ответили на репорт @id{vuser['id']}({vuser_nickname}) ✅"
            await message.answer(answer_message)

            text_to_send = f"@id{vuser['id']}({vuser_nickname}), администратор @id{user_info['id']}({user_nickname}) ответил вам:\n\n💬 {text}"
            await bot.api.messages.send(user_id=vuser['id'], random_id=0, message=text_to_send)
            admins = await get_admins()
            admin_message = f"Администратор @id{user_info['id']}({user_nickname}) ответил на репорт @id{vuser['id']}({vuser_nickname}) ✅"
            for admin in admins:
                await bot.api.messages.send(admin['id'], random_id=0, message=admin_message)
            await close_report(id=id)
        else:
            await message.answer(f"@id{user_info['id']}({user_info['nickname']}), используйте: Ответить «ID» «текст» ❌")
    else:
        return