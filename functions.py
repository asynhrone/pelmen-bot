import aiomysql
import asyncio, random
import re
from config import flat_cost, car_cost, yacht_cost, token
from vkbottle import PhotoMessageUploader, Bot
from PIL import Image
import io

bot = Bot(token)

def format_number(n):
    if n < 1e6:
        return f"{n}"
    elif n < 1e9:
        return f"{n/1e6:.1f} млн."
    elif n < 1e12:
        return f"{n/1e9:.1f} млрд."
    elif n < 1e15:
        return f"{n/1e12:.1f} трлн."
    else:
        return f"{n/1e15:.1f} трлд."


async def connect():
    conn = await aiomysql.connect(host='127.0.0.1', port=3306, db='bot',
                                  user='root', password='', autocommit=True)
    return conn

async def insert_user(user_id, first_name):
    conn = await connect() 
    try:
        async with conn.cursor() as cursor: 
            await cursor.execute("""
                INSERT INTO `users`
                (`id`, `bot_id`, `nickname`, `balance`, `status`, `farm-count`, `farm-type`, `bitcoin`, `last_mining_time`, `exp`, `fishing_rob_level`, `last_bonus_time`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, 0, first_name, 3500, 'Пользователь', 0, 0, 0, None, 0, 1, None))

    finally:
        conn.close()

async def bot_get_user(user_id):
    conn = await connect()
    try:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM `users` WHERE `bot_id` = %s", (user_id,))
            result = await cursor.fetchone()
            return result
    finally:
        conn.close()

async def get_user(user_id):
    conn = await connect()
    try:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM `users` WHERE `id` = %s", (user_id,))
            result = await cursor.fetchone()
            return result
    finally:
        conn.close()

async def insert_newnickname(user_id, newnickname):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE `users` SET `nickname`=%s WHERE `id`=%s", 
                                 (newnickname, user_id,))
    finally:
        conn.close()

async def update_mining_shop(user_id, number, balance, price, count):
    number_to_type = {1: '1', 2: '2', 3: '3', 4: '4'}
    farm_type = number_to_type.get(number) 

    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            res = int(balance) - int(price)
            await cursor.execute(
                "UPDATE `users` SET `balance` = %s, `farm-count` = IFNULL(`farm-count`, 0) + %s, `farm-type` = %s WHERE `id` = %s",
                (res, count, farm_type, user_id,)
            )
    finally:
        conn.close()

async def bitcoin_mine(user_id, bitcoin_earned):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE `users` SET `bitcoin` = `bitcoin` + %s WHERE `id` = %s",
                (bitcoin_earned, user_id,)
            )
    finally:
        conn.close()

async def update_user_mining_time(user_id, last_mining_time):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE `users` SET `last_mining_time`= %s WHERE `id`=%s",
                (last_mining_time, user_id,)
            )
    finally:
        conn.close()

async def sell_bitcoin(user_id, count, cost):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            res = count * cost
            await cursor.execute(
                "UPDATE `users` SET `bitcoin`= `bitcoin` - %s, `balance` = `balance` + %s WHERE `id`=%s",
                (count, res, user_id)
            )
            return res
    finally:
        conn.close()

async def sell_farm(user_id, count, cost, ifall):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            if ifall == True:
                await cursor.execute(
                    "UPDATE `users` SET `farm-count`=`farm-count` - %s, `balance`=`balance` + %s, `farm-type`=%s WHERE `id`=%s",
                    (count, cost, 0, user_id)
                )
            else:
                await cursor.execute(
                    "UPDATE `users` SET `farm-count`=`farm-count` - %s, `balance`=`balance` + %s WHERE `id`=%s",
                    (count, cost, user_id)
                )
    finally:
        conn.close()

async def sell_farm_all(user_id, count, cost):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE `users` SET `farm-count`=`farm-count` - %s, `balance`=`balance` + %s, `farm-type`=%s WHERE `id`=%s",
                (count, cost, 0, user_id)
            )
    finally:
        conn.close()

async def get_top_users_by_them(type):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(f"SELECT `id`, `nickname`, `{type}` FROM `users` ORDER BY `{type}` DESC LIMIT 10")
            result = await cursor.fetchall()
            return result
    finally:
        conn.close()

async def get_user_place_in_top(user_id, top_users):
    for i, user in enumerate(top_users):
        if user[0] == user_id:
            return i + 1
    return None

async def update_user_bonus_time(user_id, last_bonus_time):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE `users` SET `last_bonus_time`= %s WHERE `id`=%s",
                (last_bonus_time, user_id,)
            )
    finally:
        conn.close()

async def bonus_get(user_id, price, price_exp, exp_count):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            if exp_count is not None:
                await cursor.execute(
                    "UPDATE `users` SET `balance` = `balance` + %s, `exp` = `exp` + %s WHERE `id` = %s",
                    (price, int(price_exp), user_id,)
                )
            else:
                await cursor.execute(
                    "UPDATE `users` SET `balance` = `balance` + %s, `exp` = %s WHERE `id` = %s",
                    (price, price_exp, user_id,)
                )
    finally:
        conn.close()

async def get_fishing(user_id, win_dollars, win_exp, exp_count):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            if exp_count is not None:
                await cursor.execute(
                    "UPDATE `users` SET `balance` = `balance` + %s, `exp` = `exp` + %s WHERE `id` = %s",
                    (win_dollars, int(win_exp), user_id,)
                )
            else:
                await cursor.execute(
                    "UPDATE `users` SET `balance` = `balance` + %s, `exp` = %s WHERE `id` = %s",
                    (win_dollars, win_exp, user_id,)
                )
    finally:
        conn.close()

async def fishing_update_cooldown(user_id, new_fishing_time):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE `users` SET `last_fishing_time`= %s WHERE `id`=%s",
                (new_fishing_time, user_id,)
            )
    finally:
        conn.close()

async def fish_rob_upgrade(user_id):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE `users` SET `fishing_rob_level`= `fishing_rob_level` + %s, `exp` = `exp` - %s WHERE `id`=%s",
                (1, 25000, user_id,)
            )
    finally:
        conn.close()

async def converter(count):
    if 'к' in count:
        bet = int(count.replace('к', '000'))
    else:
        bet = int(count)
    
    return bet

async def casino_win(user_id, bet):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE `users` SET `balance`= `balance` + %s WHERE `id`=%s",
                (bet, user_id,)
            )
    finally:
        conn.close()

async def casino_lose(user_id, bet):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE `users` SET `balance`= `balance` - %s WHERE `id`=%s",
                (bet, user_id,)
            )
    finally:
        conn.close()

async def set_them(user_id, type, count):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                f"UPDATE `users` SET `{type}`= %s WHERE `id`=%s",
                (count, user_id,)
            )
    finally:
        conn.close()

async def buy_them(user_id, type, product):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            if type == 'flat':
                price = flat_cost.get(str(product))
            if type == 'car':
                price = car_cost.get(str(product))
            if type == 'yacht':
                price = yacht_cost.get(str(product))

            await cursor.execute(
                f"UPDATE `users` SET `{type}`= %s, `balance`=`balance`- %s  WHERE `id`=%s",
                (product, price, user_id,)
            )
    finally:
        conn.close()

async def sell_them(user_id, type, product):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            if type == 'flat':
                price = flat_cost.get(str(product)) / 2
            if type == 'car':
               price = int(car_cost.get(str(product))) / 2
            if type == 'yacht':
                price = yacht_cost.get(str(product)) / 2

            await cursor.execute(
                f"UPDATE `users` SET `{type}`= %s, `balance`=`balance`+ %s WHERE `id`=%s",
                (0, price, user_id,)
            )
    finally:
        conn.close()

async def race_update_cups(user_id, cups, operation, count):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            if cups is None:
                await cursor.execute(
                    f"UPDATE `users` SET `cups`= %s WHERE `id`=%s",
                    (cups, user_id,)
                )
            else:
                await cursor.execute(
                    f"UPDATE `users` SET `cups`=`cups`{operation}%s WHERE `id`=%s",
                    (count, user_id,)
                )
    finally:
        conn.close()

async def race_update_cooldown(user_id, new_race_time):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE `users` SET `last_race_time`= %s WHERE `id`=%s",
                (new_race_time, user_id,)
            )
    finally:
        conn.close()

async def get_users_by_them(type):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(f"SELECT `id`, `nickname`, `{type}` FROM `users` WHERE `{type}` IS NOT NULL ORDER BY `{type}` DESC")
            result = await cursor.fetchall()
            return result
    finally:
        conn.close()

async def get_random_user(users, excluded_user_id):
    filtered_users = [user for user in users if user[0] != excluded_user_id]
    selected_user = random.choice(filtered_users)
    res = await get_user(user_id=selected_user[0])
    return res

async def generate_profile_image(flat, car):
    flats = {"0": "street.png", "1": "chrushevka.png", "2": "chelybinsk.png",
    "3": "piter.png", "4": "moscow.png", "5": "new-york.png",
    "6": "in-heart-pekin.png", "7": "odeon-tower.png", "8": "sarai.png"}

    cars = {"0": "", "1": "nissan-pathfinder.png", "2": "mazda6.png", "3": "mercedes-cls.png",
            "4": "audi-r8.png", "5": "ferarri-458-italia.png", 
            "6": "mercedes-pullman.png", "7": "rolls-royce-sweeptail.png", "8": "bugatti-bolide.png",
            "9": "aurus-senat.png", "10": "new-year-unitaz.png"}

    flat_filename = flats[str(flat)] if flat and flat != "0" else flats["0"]

    flat = Image.open(f"images/flats/{flat_filename}")
    car_filename = cars.get(str(car), "")

    if car_filename:  # Проверяем, не пустая ли строка
            car = Image.open(f"images/cars/{car_filename}")

            # Если режим изображения 'P', конвертируем его в 'RGBA'
            if car.mode == 'P':
                car = car.convert('RGBA')

            # Получаем размеры изображений
            flat_width, flat_height = flat.size
            car_width, car_height = car.size

            # Вычисляем координаты для размещения изображения автомобиля
            x = (flat_width - car_width) // 2 + 300
            y = (flat_height - car_height) + 250

            # Вставляем изображение автомобиля на изображение фона
            flat.paste(car, (x, y), car)

    # Prepare the image to be saved in memory
    img_byte_arr = io.BytesIO()
    flat.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    # Your existing code to upload the image
    photo_uploader = PhotoMessageUploader(bot.api)
    photo = await photo_uploader.upload(img_byte_arr)

    return photo

async def transfer_money(user_id, operation, count):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                f"UPDATE `users` SET `balance`=`balance` {operation} %s WHERE `id`=%s",
                (count, user_id,)
            )
    finally:
        conn.close()

async def get_taxi(user_id, win_dollars, win_exp):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                f"UPDATE `users` SET `balance`=`balance`+%s, `exp`=`exp`+%s  WHERE `id`=%s",
                (win_dollars, win_exp, user_id,)
            )
    finally:
        conn.close()


async def taxi_update_cooldown(user_id, new_taxi_time):
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE `users` SET `last_taxi_time`= %s WHERE `id`=%s",
                (new_taxi_time, user_id,)
            )
    finally:
        conn.close()