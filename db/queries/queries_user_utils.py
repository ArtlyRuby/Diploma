from db.models import *

from sqlalchemy import select


class UserUtilsQueryService:

    @staticmethod
    async def get_user_cart_id(user_id: int, session):
        async with session:
            query = await session.execute(
                select(Cart.cart_id).where(Cart.telegram_id == user_id)
            )

            print(query.scalar_one_or_none(), 123123123123123)

            return query.scalar_one_or_none()
