from db.queries.func_queries import QueryService


class TelegramFuncService:
    query = QueryService()

    async def create_cart(self, user_id: int):
        try:
            await self.query.create_cart(user_id)

        except Exception as e:
            print(f"Что-то пошло не так при создании корзины пользователя: {e}")


    async def create_user(self, user_id: int, username: str, first_name=None, last_name=None):
        try:
            await self.query.create_user(user_id,
                                         username,
                                         first_name,
                                         last_name
                                         )

        except Exception as e:
            print(f"Что-то пошло не так при создании пользователя: {e}")


    async def get_products_by_category_id(self, category_id: int):
        try:
            return await self.query.get_products_by_category_id(category_id)

        except Exception as e:
            print(f"Что-то пошло не так при получении списка товара {e}")
            return None


    async def add_item_to_cart(self, user_id: int, product_id: int, quantity: int):
        try:
            await self.query.add_item_to_cart(user_id, product_id, quantity)

        except Exception as e:
            print(f"Что-то пошло не так при добавлении товара в корзину: {e}")


    async def delete_cart_item(self, user_id: int, product_id: int):
        try:
            await self.query.delete_cart_item(user_id, product_id)

        except Exception as e:
            print(f"Что-то пошло не так при добавлении товара в корзину: {e}")


    async def get_cart_items(self, user_id: int):
        try:
            return await self.query.get_cart_items(user_id)

        except Exception as e:
            print(f"Что-то пошло не так при получении товаров корзины: {e}")
            return None


    async def get_product_name(self, product_id: int):
        try:
            return await self.query.get_product_name(product_id)

        except Exception as e:
            print(f"Что-то пошло не так при получении ID категории: {e}")
            return None


    async def place_order_sequence(self, user_id: int, order_id: str):
        try:
            cart_data = await self.get_cart_items(user_id)

            await self.query.place_order_into_orders(user_id, cart_data, order_id)

            await self.query.place_order_items(cart_data, order_id)

            await self.query.clear_cart_after_payment(user_id)

            await self.query.change_order_status_after_payment(order_id, True)

        except Exception as e:
            await self.query.change_order_status_after_payment(order_id, False)
            print(f"Что-то пошло не так при попытке обработать заказ: {e}")


    async def get_products_by_data(self, data: str):
        try:
            has_digits = any(char.isdigit() for char in data)

            if has_digits:
                return await self.query.get_products_by_article(data.replace(" ", ""))

            else:
                data.lower()
                data[0].upper()
                return await self.query.get_products_by_name(data.rstrip())

        except Exception as e:
            print(f"Что-то пошло не так при попытке начать поиск: {e}")

            return None


    async def get_upcoming_order(self):
        try:
            return await self.query.get_upcoming_order()

        except Exception as e:
            print(f"Что-то пошло не так при попытке обработать предстоящие готовые заказы: {e}")
            return None


    async def complete_order_status(self, order_id: str):
        try:
            await self.query.complete_order_status(order_id)

        except Exception as e:
            print(f"Что-то пошло не так при попытке смены статуса заказа: {e}")


    async def get_order_by_status(self, status):
        try:
            return await self.query.get_order_by_status(status)

        except Exception as e:
            print(f"Что-то пошло не так при попытке обработать заказы в статусе ON_HOLD: {e}")
            return None


    async def get_to_work_order(self, order_id):
        try:
            await self.query.get_to_work_order(order_id)

        except Exception as e:
            print(f"Что-то пошло не так при попытке обработать статус заказа в работу: {e}")

