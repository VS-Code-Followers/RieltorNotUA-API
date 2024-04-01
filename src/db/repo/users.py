from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection


class UserRepo:
    def __init__(self, session: AsyncSession | AsyncConnection):
        self.session = session
