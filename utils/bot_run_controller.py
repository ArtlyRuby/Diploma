from botActions.commands import Handler
from settings import Setting

from aiogram import Bot, Dispatcher


class Controller:
    __config = Setting()
    __bot = Bot(token=__config.bot_token)
    dp = Dispatcher(bot=__bot)

    __command_handler = Handler(__bot, dp)

    async def start_bot(self):
        await self.dp.start_polling(self.__bot)

