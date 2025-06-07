from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from settings import Setting
from botActions.func_services import TelegramFuncService


class AdminHandler:
    __settings = Setting()
    func_service = TelegramFuncService()


    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.chat_id = self.__settings.admin_chat_id
        self.group_id = self.__settings.admin_group_id
        self.scheduler = AsyncIOScheduler()


    async def check_upcoming_order_for_admin(self):
        try:
            data = await self.func_service.get_upcoming_order()

            print(f"Проверка ближащих заказов: найдено {len(data) if data else 0} заказов")

            for i in data:
                await self.bot.send_message(chat_id=self.__settings.admin_group_id,
                                            text=f"У юзера с никнеймом: {i['username']} заказ должен быть выполнен сегодня.\n"
                                            f"Узнайте актуальный статус заказа у сотрудников и, в случае необходимости, "
                                            f"оповестите заказчика о возможных задержках!\n"
                                            f"Текущий статус заказа: {i['order_status']}\n"
                                            f"День заказа: {i['order_date']}")

        except Exception as e:
            print(f"Ошибка при проверке ближайших заказов check_upcoming_order: {e}")


    async def start_scheduler(self):
        # Запускаем каждый день в 00:00
        self.scheduler.add_job(
            self.check_upcoming_order_for_admin,
            trigger=CronTrigger(minute="*/10"),
            timezone="Asia/Bishkek"
        )
        self.scheduler.start()
