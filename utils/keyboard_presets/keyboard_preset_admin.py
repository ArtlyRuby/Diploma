from db.queries.func_queries import QueryService

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class AdminKeyboardPreset:
    __query = QueryService()

    @staticmethod
    def get_inline_keyboard(keyboard: list, button_order: list):
        builder = InlineKeyboardBuilder()

        for i in keyboard[0]:
            builder.add(i)
        builder.adjust(*button_order)

        return builder.as_markup()


    def get_main_preset(self):
        keyboard = [
            [
                InlineKeyboardButton(text="Проверить в работе", callback_data="complete_order"),
                InlineKeyboardButton(text="Проверить заказы в ожидании", callback_data="check_active_orders"),
            ]
        ]

        return self.get_inline_keyboard(keyboard, [1, 1])


    def get_order_to_work_button_preset(self, order_id):
        keyboard = [
            [
                InlineKeyboardButton(text="Взять заказ в работу", callback_data=f"order_to_work_{order_id}"),
                InlineKeyboardButton(text="Вернуться в меню", callback_data="open_admin_menu")
            ]
        ]

        return self.get_inline_keyboard(keyboard, [1, 1])


    def get_order_completed_button_preset(self, order_id):
        keyboard = [
            [
                InlineKeyboardButton(text="Заказ завершён", callback_data=f"order_completed_{order_id}"),
                InlineKeyboardButton(text="Вернуться в меню", callback_data="open_admin_menu")
            ]
        ]

        return self.get_inline_keyboard(keyboard, [1, 1])
