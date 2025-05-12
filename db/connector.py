import psycopg2
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from contextlib import asynccontextmanager

from settings import Setting


class DatabaseConnector:
    __setting = Setting()


    engine = create_async_engine(__setting.db_url,
                                 echo=True,
                                 pool_pre_ping=True,
                                 pool_timeout=1200,
                                 pool_size=10,
                                 pool_recycle=1200,
                                 )

    async_session_maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=True
    )


    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        async with self.async_session_maker() as session:
            async with session.begin():
                try:
                    yield session

                except Exception as e:
                    print(f"Не удалось создать сессию подключения к БД: {e}")
                    await session.rollback()

                finally:
                    await session.close()
