from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from sqlalchemy import insert, select, delete
from uuid import UUID
from ..models import Offers
from ...api.models import Offer, SearchValidate


class OfferRepo:
    def __init__(self, session: AsyncSession | AsyncConnection):
        self.session = session
        self.offer_params = (
            "uuid",
            "author_id",
            "offer_type",
            "area",
            "name",
            "description",
            "location",
            "price",
            "floor",
            "photos",
            "tags",
        )

    async def add_offer(self, offer: Offer) -> str:
        await self.session.execute(insert(Offers).values(**offer.model_dump()))
        await self.session.commit()

    async def delete_offers_by_uuid(self, uuid: UUID):
        await self.session.execute(delete(Offers).where(Offers.uuid == uuid))
        await self.session.commit()

    async def delete_offers_by_author(self, author_id: int):
        await self.session.execute(delete(Offers).where(Offers.author_id == author_id))
        await self.session.commit()

    async def cleanup_offers(self):
        await self.session.execute(delete(Offers))
        await self.session.commit()

    async def get_all_offers(self) -> list[Offer]:
        result = await self.session.execute(select(Offers))
        return [
            Offer(**dict(zip(self.offer_params, i.tuple()))) for i in result.fetchall()
        ]

    async def get_offer_by_id(self, id: UUID):
        result = await self.session.execute(select(Offers).where(Offers.uuid == id))
        return [
            Offer(**dict(zip(self.offer_params, i.tuple()))) for i in result.fetchall()
        ]

    async def get_filters_offers(
        self,
        value: SearchValidate,
    ):
        exp = []
        if (
            (value.offer_type is None)
            and (value.uuid is None)
            and (value.author_id is None)
            and (value.price is None)
            and (value.area is None)
        ):
            return await self.get_all_offers()
        if value.uuid is not None:
            return await self.get_offer_by_id(value.uuid)
        if value.offer_type is not None:
            exp.append(Offers.offer_type == value.offer_type.value)
        if value.author_id is not None:
            exp.append(Offers.author_id == value.author_id)
        if value.price is not None:
            if value.price.value is None:
                if (value.price.since is not None) and (value.price.to is not None):
                    exp.append(value.price.to >= Offers.price >= value.price.since)
                elif value.price.since is not None:
                    exp.append(Offers.price >= value.price.since)
                elif value.price.to is not None:
                    exp.append(value.price.to >= Offers.price)
            else:
                exp.append(Offers.price == value.price.value)
        if value.area is not None:
            if value.area.value is None:
                if (value.area.since is not None) and (value.area.to is not None):
                    exp.append(value.area.to >= Offers.area >= value.area.since)
                elif value.area.since is not None:
                    exp.append(Offers.area >= value.area.since)
                elif value.area.to is not None:
                    exp.append(value.area.to >= Offers.area)
            else:
                exp.append(Offers.price == value.price.value)
        result = await self.session.execute(select(Offers).where(*exp))
        return [
            Offer(**dict(zip(self.offer_params, i.tuple()))) for i in result.fetchall()
        ]
