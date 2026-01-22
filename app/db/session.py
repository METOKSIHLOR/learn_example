from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine

from app.config.config import config

print("DATABASE MODULE ID:", id(__name__))

engine: AsyncEngine | None = None
SessionFactory: async_sessionmaker[AsyncSession] | None = None

async def connect_db() -> None:
    global engine, SessionFactory
    engine = create_async_engine(
        url=config.postgres.url,
        pool_pre_ping=True,
    )

    SessionFactory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    print("SessionFactory:", SessionFactory)

async def close_db() -> None:
    if engine:
        await engine.dispose()