from db.queries.func_queries import QueryService

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class UserKeyboardPreset:
    __query = QueryService()

    @staticmethod
    def get_inline_keyboard(keyboard: list, button_order: list):
        builder = InlineKeyboardBuilder()

        for i in keyboard[0]:
            builder.add(i)
        builder.adjust(*button_order)

        return builder.as_markup()

    def get_help_preset(self):
        keyboard = [
            [
                InlineKeyboardButton(text="Вернуться на главную", callback_data="go_main")
            ]
        ]

        return self.get_inline_keyboard(keyboard, [1])

    def get_main_preset(self):
        keyboard = [
            [
                InlineKeyboardButton(text="Поиск товара", callback_data="search_by"),
                InlineKeyboardButton(text="Список категорий", callback_data="category_list"),
                InlineKeyboardButton(text="Корзина", callback_data="cart"),
                InlineKeyboardButton(text="Помощь", callback_data="help"),
            ]
        ]

        return self.get_inline_keyboard(keyboard, [2, 2])


    def get_main_preset_admin(self):
        keyboard = [
            [
                InlineKeyboardButton(text="Открыть админ панель", callback_data="open_admin_menu")
            ]
        ]

        return self.get_inline_keyboard(keyboard, [2, 2, 1])


    def get_category_list_preset(self):
        keyboard = [
            [
                InlineKeyboardButton(text="Шкафы", callback_data="shelves"),
                InlineKeyboardButton(text="Кровати и ложа", callback_data="beds"),
                InlineKeyboardButton(text="Стулья", callback_data="chairs"),
                InlineKeyboardButton(text="Столы", callback_data="tables"),
                InlineKeyboardButton(text="Назад", callback_data="go_main"),
            ]
        ]

        return self.get_inline_keyboard(keyboard, [2, 2, 1])

    def get_search_preset(self):
        keyboard = [
            [
                InlineKeyboardButton(text="Поиск по артикулу", callback_data="search_by_article"),
                InlineKeyboardButton(text="Поиск по названию", callback_data="search_by_name")
            ]
        ]

        return self.get_inline_keyboard(keyboard, [2])

    def get_go_back_to_categories(self):
        keyboard = [
            [
                InlineKeyboardButton(text="Вернуться назад", callback_data="category_list")
            ]
        ]

        return self.get_inline_keyboard(keyboard, [1])

    def get_cart_item_manage_preset(self, product_id):
        keyboard = [
            [
                InlineKeyboardButton(text="Выбрать кол-во", callback_data=f"add_to_cart_{product_id}"),
                InlineKeyboardButton(text="Удалить товар", callback_data=f"delete_cart_item_{product_id}")
            ]
        ]

        return self.get_inline_keyboard(keyboard, [1, 1])

    def get_add_to_cart_preset(self, product_id):
        keyboard = [
            [
                InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add_to_cart_from_category_{product_id}")
            ]
        ]

        return self.get_inline_keyboard(keyboard, [1])

    def get_after_quantity_change_preset(self):
        keyboard = [
            [
                InlineKeyboardButton(text="Открыть корзину", callback_data=f"cart"),
                InlineKeyboardButton(text="Вернуться в главное меню", callback_data=f"go_main")
            ]
        ]

        return self.get_inline_keyboard(keyboard, [1, 1])

    def get_products_after_change_preset(self):
        keyboard = [
            [
                InlineKeyboardButton(text="Продолжить просмотр товаров", callback_data=f"cart"),
                InlineKeyboardButton(text="Вернуться в главное меню", callback_data=f"go_main")
            ]
        ]

        return self.get_inline_keyboard(keyboard, [1, 1])

    def get_place_order_preset(self):
        keyboard = [
            [
                InlineKeyboardButton(text="Оформить заказ", callback_data="place_order")
            ]
        ]

        return self.get_inline_keyboard(keyboard, [1])

    def get_confirm_payment_preset(self):
        keyboard = [
            [
                InlineKeyboardButton(text="Оплатить", callback_data="confirm_payment"),
                InlineKeyboardButton(text="Вернуться в корзину", callback_data="cart")
            ]
        ]

        return self.get_inline_keyboard(keyboard, [1, 1])
