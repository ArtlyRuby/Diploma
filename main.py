from utils.bot_run_controller import Controller
import asyncio
"""-----------------------------------------------------------------------------------------------------------------"""

controller = Controller()

if __name__ == '__main__':

    asyncio.run(controller.start_bot())
