from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from ...api.models.users import AuthorInDB, Author
from ..models import Users
from sqlalchemy import insert, select
from pydantic import EmailStr
from typing import Optional


class UserRepo:
    def __init__(self, session: AsyncSession | AsyncConnection):
        self.session = session
        self.user_params = ['email', 'full_name', 'account_id', 'location', 'offers']

    async def create_user(self, data: AuthorInDB) -> None:
        """Creating user by AuthorInDB pydantic model"""
        await self.session.execute(
            insert(Users).values(**data.model_dump(exclude_none=True))
        )
        await self.session.commit()

    async def get_all_users(self) -> list[Author]:
        """Getting all users from the table"""
        result = await self.session.execute(
            select(*[cl for cl in Users.__table__.columns if cl.key != 'password'])
        )
        return [
            Author(**dict(zip(self.user_params, i._tuple()))) for i in result.fetchall()
        ]

    async def get_password_by_email(self, email: EmailStr) -> Optional[str]:
        """Getting password by user`s email"""
        result = await self.session.execute(
            select(Users.password).where(Users.email == email)
        )
        return result.scalars().first()

    async def get_user_by_email(self, email: EmailStr) -> Optional[Author]:
        """Getting user by user`s email"""
        result = await self.session.execute(
            select(
                *[cl for cl in Users.__table__.columns if cl.key != 'password']
            ).where(Users.email == email)
        )
        rows = result.fetchone()
        if rows is None:
            return None
        return Author(**dict(zip(self.user_params, rows._tuple())))

    async def user_exists(self, email: EmailStr) -> bool:
        """Checking if user exists"""
        result = await self.session.execute(select(1).where(Users.email == email))
        if result.first():
            return True
        return False
