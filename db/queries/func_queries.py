from db.connector import DatabaseConnector
from db.models import *

from sqlalchemy import select, delete

from datetime import datetime, timedelta, time, date


class QueryService:
    __db = DatabaseConnector()


    async def create_user(self, user_id: int, username: str, first_name: str, last_name: str):
        async with self.__db.get_session() as session:

            query = await session.execute(
                select(User).where(User.telegram_id == user_id)
            )

            if not query.one_or_none():
                user = User(
                    telegram_id=user_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name
                )
                session.add(user)

                await session.commit()


    async def create_cart(self, user_id: int):
        async with self.__db.get_session() as session:

            query = await session.execute(
                select(Cart).where(Cart.telegram_id == user_id)
            )

            if not query.one_or_none():
                cart = Cart(
                    cart_id=f"CART_{user_id}",
                    telegram_id=user_id
                )
                session.add(cart)

                await session.commit()


    async def get_products_by_category_id(self, category_id: int):
        async with self.__db.get_session() as session:

            query = (
                select(
                    Product.product_id,
                    Product.name,
                    Product.description,
                    Product.price,
                    Product.sku
                )
                .join(ProductCategory, Product.product_id == ProductCategory.product_id)
                .where(ProductCategory.category_id == category_id)
            )

            result = await session.execute(query)

            return result.mappings().all()


    async def add_item_to_cart(self, user_id, product_id, quantity):
        async with self.__db.get_session() as session:

            query = await session.get(
                CartItem,
                f"ITEM_{user_id}_{product_id}"
            )

            if query is None:
                # Если записи нет - создаём новую
                cart_item = CartItem(
                    cart_item_id=f"ITEM_{user_id}_{product_id}",
                    cart_id=f"CART_{user_id}",
                    product_id=product_id,
                    quantity=quantity
                )
                session.add(cart_item)
            else:
                # Если запись есть - увеличиваем количество
                query.quantity = quantity

            await session.commit()


    async def delete_cart_item(self, user_id, product_id):
        async with self.__db.get_session() as session:

            query = await session.get(
                CartItem,
                f"ITEM_{user_id}_{product_id}"
            )

            if query is not None:
                await session.delete(query)

            else:
                print(f"Товар с id: {product_id} не найден в корзине пользователя")

            await session.commit()


    async def get_cart_items(self, user_id):
        async with self.__db.get_session() as session:

            query = (
                select(
                    CartItem.product_id,
                    Product.name.label("product_name"),
                    Product.price,
                    CartItem.quantity
                )
                .join(Product, CartItem.product_id == Product.product_id)
                .where(CartItem.cart_id == f"CART_{user_id}")
            )

            result = await session.execute(query)

            return result.mappings().all()


    async def get_product_name(self, product_id):
        async with self.__db.get_session() as session:

            query = await session.get(
                Product,
                product_id
            )

            return query.name


    #--------------------------Оформление заказа---------------------------------


    async def place_order_into_orders(self, user_id, cart_data, order_id):
        async with self.__db.get_session() as session:

            order_data = {
                "summ_price": 0,
                "summ_quantity": 0,
                "user_id": user_id,
                "completion_date": None
            }

            for i in cart_data:
                order_data["summ_price"] += i["price"] * i["quantity"]
                order_data["summ_quantity"] += i["quantity"]

            days_to_add = 3 * order_data["summ_quantity"]
            order_data["completion_date"] = datetime.utcnow() + timedelta(days=days_to_add)

            query = Order(
                order_id=order_id,
                telegram_id=order_data["user_id"],
                total_amount=order_data["summ_price"],
                order_status="PENDING",
                completion_date=order_data["completion_date"]
            )
            session.add(query)

            await session.commit()


    async def place_order_items(self, cart_data, order_id):
        async with self.__db.get_session() as session:

            for i in cart_data:

                query = OrderItem(
                    order_item_id=f"{order_id}_{i["product_id"]}",
                    order_id=order_id,
                    product_id=i["product_id"],
                    quantity=i["quantity"],
                    unit_price=i["price"]
                )

                session.add(query)

            await session.commit()


    async def clear_cart_after_payment(self, user_id):
        async with self.__db.get_session() as session:

            query = delete(CartItem).where(CartItem.cart_id == f"CART_{user_id}")

            await session.execute(query)

            await session.commit()


    async def change_order_status_after_payment(self, order_id, flag: bool):
        async with self.__db.get_session() as session:

            query = await session.get(
                Order,
                order_id
            )

            if flag:
                query.order_status = "ON_HOLD"

            else:
                query.order_status = "FAILED"

            await session.commit()


    #-------------------------------------------------------------------------------


    async def get_products_by_name(self, data):
        async with self.__db.get_session() as session:

            query = (
                select(
                    Product.product_id,
                    Product.name,
                    Product.description,
                    Product.price,
                    Product.sku
                )
                .where(Product.name.ilike(f"%{data}%"))
            )

            result = await session.execute(query)

            return result.mappings().all()


    async def get_products_by_article(self, data):
        async with self.__db.get_session() as session:

            query = (
                select(
                    Product.product_id,
                    Product.name,
                    Product.description,
                    Product.price,
                    Product.sku
                )
                .where(Product.sku == data)
            )

            result = await session.execute(query)

            return result.mappings().all()


    async def get_upcoming_order(self):
        async with self.__db.get_session() as session:
            today_start = datetime.combine(date.today(), time.min)

            query = (
                select(
                    User.username,
                    Order.order_status,
                    Order.completion_date,
                    Order.order_date
                )
                .join(User, User.telegram_id == Order.telegram_id)
                .where(Order.completion_date >= today_start)
                .where(Order.order_status == "IN_PROGRESS")
            )

            result = await session.execute(query)

            return result.mappings().all()


    #--------------------------------------------------------------------------------------

    async def complete_order_status(self, order_id: str):
        async with self.__db.get_session() as session:
            query = await session.get(
                Order,
                order_id
            )

            query.order_status = "COMPLETED"

            await session.commit()


    async def get_order_by_status(self, status):
        async with self.__db.get_session() as session:
            query = (
                select(
                    Order.order_id,
                    User.username,
                    Product.name.label("product_name"),
                    OrderItem.quantity
                )
                .join(User, User.telegram_id == Order.telegram_id)
                .join(OrderItem, OrderItem.order_id == Order.order_id)
                .join(Product, Product.product_id == OrderItem.product_id)
                .where(Order.order_status == status)
                .order_by(Order.order_id)
            )

            result = await session.execute(query)

            return result.mappings().all()


    async def get_to_work_order(self, order_id):
        async with self.__db.get_session() as session:
            query = await session.get(
                Order,
                order_id
            )

            query.order_status = "IN_PROGRESS"

            await session.commit()


    async def get_user_order_data(self, order_id):
        async with self.__db.get_session() as session:
            query = (
                select(
                    Order.telegram_id,
                    Product.name.label("product_name"),
                    OrderItem.quantity
                )
                .join(OrderItem, OrderItem.order_id == Order.order_id)
                .join(Product, Product.product_id == OrderItem.product_id)
                .where(Order.order_id == order_id)
            )

            result = await session.execute(query)

            return result.mappings().all()
