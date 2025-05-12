from aiogram import types, Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from utils.keyboard_presets.keyboard_presets_user import UserKeyboardPreset
from botActions.user_services import TelegramUserService


class Handler:
    user_kb = UserKeyboardPreset()
    __user_service = TelegramUserService()

    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.register_handlers()
        self.dp.fsm_storage = MemoryStorage()


    def register_handlers(self):

        @self.dp.message(F.text, Command("start"))
        async def start_interaction(message: types.Message):
            try:
                user_id = message.from_user.id
                user_name = message.from_user.username
                first_name = message.from_user.first_name
                last_name = message.from_user.last_name

                await self.__user_service.create_user(user_id, user_name, first_name, last_name)

                await self.__user_service.create_cart(user_id)

                await message.answer(
                    "Привет, пользователь, добро пожаловать в наш онлайн-магазин мебели.\n"
                    "Здесь ты можешь найти много различных товаров и приобрести их по доступной цене!\n"
                    "Для взаимодействия с онлайн-магазином представляем тебе интерфейс с кнопками ниже!",
                    reply_markup=self.user_kb.get_main_preset()
                )

            except Exception as e:
                print(f"Ошибка при обработке /start: {e}")
                await message.answer("Произошла ошибка, Попробуйте позже.")


        @self.dp.callback_query(F.data == "help")
        async def get_help_info(callback: types.CallbackQuery):
            try:
                await callback.answer("Открывается меню помощи")

                await callback.message.answer(text="Тут должен был быть текст, но мне лень писать",
                                              reply_markup=self.user_kb.get_help_preset())

            except Exception as e:
                print(f"Что-то пошло не так при попытке открыть меню помощи: {e}")


        @self.dp.message(F.text, Command("cart"))
        async def get_cart_items(message: types.Message):
            try:
                data = await self.__user_service.get_cart_items(message.from_user.id)

                await message.answer("———————————————————————————————")

                await message.answer("Ваши товары в корзине:")

                summ_price = 0
                summ_quantity = 0
                for i in data:
                    await message.answer(text=f"Имя товара: {i["product_name"]}\n"
                                              f"Цена: {i["price"] * i["quantity"]}\n"
                                              f"Кол-во: {i["quantity"]}",
                                         reply_markup=self.user_kb.get_cart_item_manage_preset(i['product_id']))
                    summ_price += i["price"] * i["quantity"]
                    summ_quantity += i["quantity"]

                await message.answer(f"Итоговая цена за все товары: {summ_price}\n"
                                     f"Общее кол-во товаров: {summ_quantity}")

            except Exception as e:
                print(f"Что-то пошло не так при отображении корзины товаров: {e}")


        @self.dp.callback_query(F.data == "go_main")
        async def handle_go_main(callback: types.CallbackQuery):
            try:
                await callback.answer("Открываем главную страницу")

                await callback.message.edit_reply_markup(
                    reply_markup=self.user_kb.get_main_preset()
                )

            except Exception as e:
                print(f"Что-то пошло не так при открытии главной страницы: {e}")


        @self.dp.callback_query(F.data == "category_list")
        async def handle_get_category_list(callback: types.CallbackQuery):
            try:
                await callback.answer("Открываем список категорий...")

                await callback.message.answer("———————————————————————————————")

                await callback.message.answer(
                    text="Список категорий товаров, выберите нужную вам категорию:",
                    reply_markup=self.user_kb.get_category_list_preset()
                )

            except Exception as e:
                print(f"Что-то пошло не так при открытии списка категорий: {e}")


        async def get_category_items(callback: types.CallbackQuery, data):
            n = 1
            for i in data:
                await callback.message.answer(text=f"Товар №{n}\n"
                                                   f"Наименование: {i['name']}\n"
                                                   f"Описание: {i['description']}\n"
                                                   f"Цена: {i['price']} сом\n"
                                                   f"Артикул: {i['sku']}",
                                              reply_markup=self.user_kb.get_add_to_cart_preset(i['product_id'])
                                              )
                n += 1


        @self.dp.callback_query(F.data.in_(["tables", 'chairs', 'beds', 'shelves']))
        async def handle_get_category_items(callback: types.CallbackQuery):
            try:
                await callback.answer("Открываем список товаров...")

                await callback.message.answer("———————————————————————————————")

                category_hash = {
                    "tables": 1,
                    "chairs": 2,
                    "beds": 3,
                    "shelves": 4
                }

                # Достаю строку из колбека и сравнию с хешем, далее передаю как номер категории сюда
                data = await self.__user_service.get_products_by_category_id(category_hash[callback.data])

                await get_category_items(callback, data)

                await callback.message.answer(text="Вернуться к списку категорий",
                                              reply_markup=self.user_kb.get_go_back_to_categories()
                                              )

            except Exception as e:
                print(f"Что-то пошло не так при отображении списка товаров: {e}")


        @self.dp.message(StateFilter("waiting_for_quantity"))
        async def handle_quantity_input(message: types.Message,
                                        state: FSMContext):
            try:
                data = await state.get_data()
                product_id = data.get("product_id")
                callback_str = data.get("callback_str")
                product_name = data.get("product_name")

                await state.clear()  # Очищаем состояние

                quantity = int(message.text)

                if quantity <= 0 or quantity >= 100 or not isinstance(quantity, int):
                    await message.answer("🚫 Значение должно быть больше 0, меньше 100 или быть целочисленным",
                                         reply_markup=self.user_kb.get_main_preset())
                    return  # Прерываем выполнение

                # Ваш метод добавления в корзину
                await self.__user_service.add_item_to_cart(
                    user_id=message.from_user.id,
                    product_id=product_id,
                    quantity=quantity
                )

                await message.answer(f"Установленное кол-во товара ({product_name}) в корзине: {quantity} шт.")

                await message.answer("———————————————————————————————")

                if "from_category" in callback_str:
                    await message.answer(f"Данные товара обновились. Откройте корзину, чтобы увидеть изменения",
                                         reply_markup=self.user_kb.get_category_list_preset())

                else:
                    await message.answer(f"Данные товара обновились. Откройте корзину, чтобы увидеть изменения",
                                         reply_markup=self.user_kb.get_after_quantity_change_preset())

            except ValueError:
                await message.answer("Введено неверное значение, принимаются только целочисленные.\n"
                                     "Перейдите снова к спискам товара, чтобы попытаться добавить его в корзину",
                                     reply_markup=self.user_kb.get_category_list_preset())


        @self.dp.callback_query(F.data.contains("add_to_cart_"))
        async def handle_add_to_cart(callback: types.CallbackQuery,
                                     state: FSMContext):
            try:
                await callback.answer("Добавляем товар в корзину...")

                product_id = int(callback.data.split("_")[-1])
                callback_str = callback.data
                product_name = await self.__user_service.get_product_name(product_id)

                await state.update_data(
                    product_id=product_id,
                    callback_str=callback_str,
                    product_name=product_name
                )

                await callback.message.answer(text="———————————————————————————————")

                await callback.message.answer(
                    f"Введите количество товара ({product_name}), которое хотите добавить в корзину числом: ",
                    reply_markup=types.ReplyKeyboardRemove()
                )

                # Устанавливаем состояние ожидания
                await state.set_state("waiting_for_quantity")

            except Exception as e:
                print(f"Что-то пошло не так при добавлении товара в корзину {e}")


        @self.dp.callback_query(F.data.contains("delete_cart_item_"))
        async def handle_delete_cart_item(callback: types.CallbackQuery):
            try:
                await callback.message.answer(text="———————————————————————————————")

                await callback.answer("Удаляем товар из корзины")

                product_id = int(callback.data.split("_")[-1])

                await self.__user_service.delete_cart_item(callback.from_user.id, product_id)

            except Exception as e:
                print(f"Что-то пошло не так при удалении товара из корзины: {e}")

            finally:
                await callback.message.answer(text="Товар успешно удалён из корзины. Чтобы увидеть изменения - "
                                                   "откройте корзину снова",
                                              reply_markup=self.user_kb.get_after_quantity_change_preset())


        @self.dp.callback_query(F.data == "cart")
        async def handle_open_cart(callback: types.CallbackQuery):
            try:
                await callback.answer("Открывает вашу корзину товаров")

                data = await self.__user_service.get_cart_items(callback.from_user.id)

                await callback.message.answer("———————————————————————————————")

                await callback.message.answer("Ваши товары в корзине:")

                summ_price = 0
                summ_quantity = 0
                for i in data:
                    await callback.message.answer(text=f"Имя товара: {i["product_name"]}\n"
                                                       f"Цена: {i["price"] * i["quantity"]}\n"
                                                       f"Кол-во: {i["quantity"]}",
                                                  reply_markup=self.user_kb.get_cart_item_manage_preset(i["product_id"]))
                    summ_price += i["price"] * i["quantity"]
                    summ_quantity += i["quantity"]

                await callback.message.answer(f"Итоговая цена за все товары: {summ_price}\n"
                                              f"Общее кол-во товаров: {summ_quantity}",
                                              reply_markup=self.user_kb.get_place_order_preset())

            except Exception as e:
                print(f"Что-то пошло не так при отображении корзины товаров: {e}")


        @self.dp.callback_query(F.data == "place_order")
        async def handle_place_order(callback: types.CallbackQuery):
            try:
                await callback.answer(text="Обработка")

                await callback.message.answer(text="Подтвердите ваше действие:",
                                              reply_markup=self.user_kb.get_confirm_payment_preset())

            except Exception as e:
                print(f"Что-то пошло не так при оформлении заказа: {e}")


        @self.dp.callback_query(F.data == "confirm_payment")
        async def handle_place_order_sequence(callback: types.CallbackQuery):
            try:
                await callback.answer(text="Ожидаем проведение оплаты")

                user_id = callback.from_user.id

                await self.__user_service.place_order_sequence(user_id)

                await callback.message.answer("———————————————————————————————")

                await callback.message.answer(text="Ваш заказ успешно оформлен, спасибо за покупку!",
                                              reply_markup=self.user_kb.get_main_preset())

            except Exception as e:
                print(f"Что-то пошло не так при Обработке заказа: {e}")


        @self.dp.callback_query(F.data == "search_by")
        async def handle_search_by(callback: types.CallbackQuery):
            try:
                await callback.answer(f"Обработка поиска")

                await callback.message.answer(text="Выберите способ поиска товара:",
                                              reply_markup=self.user_kb.get_search_preset())

            except Exception as e:
                print(f"Что-то пошло не так при попытке поиска: {e}")


        @self.dp.message(StateFilter("waiting_for_search"))
        async def handle_search_input(message: types.Message,
                                        state: FSMContext):
            try:
                data = message.text

                await state.clear()  # Очищаем состояние

                query_data = await self.__user_service.get_products_by_data(data)

                if len(query_data) == 0:
                    await message.answer(text="По вашему запросу ничего не найдено, попробуйте ввести другие данные",
                                         reply_markup=self.user_kb.get_search_preset())

                else:
                    for i in query_data:
                        await message.answer(text=f"Имя товара: {i["name"]}\n"
                                                  f"Описание: {i["description"]}\n"
                                                  f"Цена: {i["price"]}\n"
                                                  f"Артикул: {i["sku"]}",
                                             reply_markup=self.user_kb.get_add_to_cart_preset(i["product_id"])
                                             )

                    await message.answer(text="Вернуться к поиску:",
                                         reply_markup=self.user_kb.get_search_preset())

            except Exception as e:
                print(f"Что-то пошло не так при обработке поиска: {e}")


        @self.dp.callback_query(F.data.contains("search_by_"))
        async def handle_search_by(callback: types.CallbackQuery,
                                   state: FSMContext):
            try:
                await callback.answer("Обработка выбора способа поиска")

                if "name" in callback.data:
                    await callback.message.answer(
                        f"Введите название, по которому хотите найти товар",
                        reply_markup=types.ReplyKeyboardRemove()
                    )

                else:
                    await callback.message.answer(
                        f"Введите артикул (числом), по которому хотите найти товар",
                        reply_markup=types.ReplyKeyboardRemove()
                    )

                # Устанавливаем состояние ожидания
                await state.set_state("waiting_for_search")

            except Exception as e:
                print(f"Что-то пошло не так при попытке выбрать способ поиска: {e}")

