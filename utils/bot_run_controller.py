from botActions.commands import Handler
from scheduleHandlers.schedules import AdminHandler
from settings import Setting

from aiogram import Bot, Dispatcher


class Controller:
    __config = Setting()
    __bot = Bot(token=__config.bot_token)
    dp = Dispatcher(bot=__bot)

    __command_handler = Handler(__bot, dp)
    __admin_handler = AdminHandler(__bot, dp)


    async def __on_startup(self, _=None):
        await self.__admin_handler.start_scheduler()

    async def start_bot(self):
        self.dp.startup.register(self.__on_startup)
        await self.dp.start_polling(self.__bot)

