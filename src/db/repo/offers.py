from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from sqlalchemy import insert, select, delete, BIGINT
from uuid import UUID
from ..models import Offers
from ...api.models.offers import Offer, SearchValidate, ShortOffer, OfferWithOutAuthor


class OfferRepo:
    def __init__(self, session: AsyncSession | AsyncConnection):
        self.session = session
        self.offer_params = [
            offer_param.key for offer_param in Offers.__table__.columns
        ]  # All columns in table

        self.short_params = [
            param
            for param in self.offer_params
            if param not in ('area', 'description', 'floor', 'tags', 'photos')
        ]  # Columns for brief viev of Offer
        self.offer_params_without_author = [
            param for param in self.offer_params if param != 'author'
        ]

    async def add_offer(self, offer: Offer) -> None:
        """Adding offer in DB by Offer pydantic model"""
        await self.session.execute(
            insert(Offers).values(**offer.model_dump(mode='json'))
        )
        await self.session.commit()

    async def delete_offers_by_uuid(self, uuid: UUID) -> None:
        """Deleting offer in DB by Offer UUID"""
        await self.session.execute(delete(Offers).where(Offers.uuid == uuid))
        await self.session.commit()

    async def delete_offers_by_author_id(self, author_id: int) -> None:
        """Deleting all offers in DB by Offer`s author"""
        await self.session.execute(
            delete(Offers).where(
                Offers.author['account_id'].astext.cast(BIGINT) == author_id
            )
        )
        await self.session.commit()

    async def cleanup_offers(self) -> None:
        """Deleting ALL offers in the table"""
        await self.session.execute(delete(Offers))
        await self.session.commit()

    async def get_all_offers(self) -> list[Offer]:
        """Getting ALL offers in the table"""
        result = await self.session.execute(select(Offers))
        return [
            Offer(**dict(zip(self.offer_params, i._tuple()))) for i in result.fetchall()
        ]

    async def get_all_short_offfers(self) -> list[ShortOffer]:
        """Getting ALL a brief view of the offers in the table"""
        result = await self.session.execute(
            select(
                Offers.uuid,
                Offers.offer_type,
                Offers.price,
                Offers.name,
                Offers.location,
                Offers.photos,
            )
        )
        return [
            ShortOffer(
                **dict(
                    zip(
                        self.short_offer_params,
                        [
                            n if ind != 5 else res._tuple()[5][0]
                            for ind, n in enumerate(res._tuple())
                        ],
                    )
                )
            )
            for res in result.fetchall()
        ]

    async def get_offers_by_author(self, author_id) -> list[OfferWithOutAuthor]:
        """Getting Author`s offers"""
        result = await self.session.execute(
            select(
                *[cl for cl in Offers.__table__.columns if cl.key != 'author']
            ).where(Offers.author['account_id'].astext.cast(BIGINT) == author_id)
        )
        return [
            OfferWithOutAuthor(
                **dict(zip(self.offer_params_without_author, i._tuple()))
            )
            for i in result.fetchall()
        ]

    async def get_offer_by_uuid(self, uuid: UUID) -> list[OfferWithOutAuthor]:
        """Getting Offer by Offer UUID"""
        result = await self.session.execute(
            select(
                *[cl for cl in Offers.__table__.columns if cl.key != 'author']
            ).where(Offers.uuid == uuid)
        )
        return [
            OfferWithOutAuthor(
                **dict(zip(self.offer_params_without_author, i._tuple()))
            )
            for i in result.fetchall()
        ]

    async def get_filters_offers(
        self,
        value: SearchValidate,
    ) -> list[Offer]:
        """Getting offers by multiple filters"""
        exp = []
        if value.offer_type is not None:
            exp.append(Offers.offer_type == value.offer_type.value)
        if value.author_id is not None:
            exp.append(
                Offers.author['account_id'].astext.cast(BIGINT) == value.author_id
            )
        if value.author_name is not None:
            exp.append(Offers.author['name'].astext == value.author_name)
        if value.price is not None:
            if value.price.value is None:
                if (value.price.since is not None) and (value.price.to is not None):
                    exp.extend(
                        [
                            value.price.to >= Offers.price,
                            Offers.price >= value.price.since,
                        ]
                    )
                elif value.price.since is not None:
                    exp.append(Offers.price >= value.price.since)
                elif value.price.to is not None:
                    exp.append(value.price.to >= Offers.price)
            else:
                exp.append(Offers.price == value.price.value)
        if value.area is not None:
            if value.area.value is None:
                if (value.area.since is not None) and (value.area.to is not None):
                    exp.extend(
                        [value.area.to >= Offers.area, Offers.area >= value.area.since]
                    )
                elif value.area.since is not None:
                    exp.append(Offers.area >= value.area.since)
                elif value.area.to is not None:
                    exp.append(value.area.to >= Offers.area)
            else:
                exp.append(Offers.price == value.price.value)
        result = await self.session.execute(select(Offers).where(*exp))
        return [
            Offer(**dict(zip(self.offer_params, i._tuple()))) for i in result.fetchall()
        ]
