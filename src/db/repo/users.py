from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from ...api.models.users import AuthorInDB, Author
from ..models import Users
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from sqlalchemy import insert, select, delete, cast, BIGINT
from pydantic import EmailStr


class UserRepo:
    def __init__(self, session: AsyncSession | AsyncConnection):
        self.session = session
        self.user_params = ['email', 'full_name', 'account_id', 'location', 'offers']

    async def create_user(self, data: AuthorInDB) -> None:
        await self.session.execute(insert(Users).values(**data.model_dump()))
        await self.session.commit()

    async def get_all_users(self) -> list[Author]:
        # !
        result = await self.session.execute(
            select(*[cl for cl in Users.__table__.columns if cl.key != 'password'])
        )
        return [
            Users(**dict(zip(self.user_params, i._tuple()))) for i in result.fetchall()
        ]

    async def get_password_by_email(self, email: EmailStr) -> str:
        result = await self.session.execute(
            select(Users.password).where(Users.email == email)
        )
        return result.scalars().first()

    async def get_user_by_email(self, email: EmailStr) -> Author:
        result = await self.session.execute(
            select(
                *[cl for cl in Users.__table__.columns if cl.key != 'password']
            ).where(Users.email == email)
        )

        return Author(**dict(zip(self.user_params, result.fetchone()._tuple())))
