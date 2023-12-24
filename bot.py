from vkbottle import Bot, API
from vkbottle.bot import BotLabeler
from handlers import ul, ml, sl, gl, al, shl
from config import token
import sys
from loguru import logger

api = API(token=token)
labeler = BotLabeler()

labeler.load(ul)
labeler.load(ml)
labeler.load(sl)
labeler.load(gl)
labeler.load(al)
labeler.load(shl)

bot = Bot(api=api, labeler=labeler)

logger.remove()
logger.add(sys.stderr, level="INFO")

bot.run_forever()