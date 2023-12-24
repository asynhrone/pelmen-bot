import aiohttp
from vkbottle.bot import Bot, Message
from vkbottle import PhotoMessageUploader
from config import token

# Токен вашего бота
bot = Bot(token=token)

@bot.on.message(text="Загрузить картинку")
async def upload_photo_handler(message: Message):
    photo_path = "1.png"  
    photo_uploader = PhotoMessageUploader(bot.api)
    photo = await photo_uploader.upload(photo_path)
    await message.answer(f"{photo}",attachment=photo)

if __name__ == "__main__":
    bot.run_forever()
