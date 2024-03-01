from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from sqlalchemy import insert, select, delete, cast, BIGINT
from uuid import UUID
from ..models import Offers
from ...api.models import Offer, SearchValidate, ShortOffer


class OfferRepo:
    def __init__(self, session: AsyncSession | AsyncConnection):
        self.session = session
        self.offer_params = (
            'uuid',
            'author',
            'offer_type',
            'area',
            'name',
            'description',
            'location',
            'price',
            'floor',
            'photos',
            'tags',
        )
        self.short_offer_params = (
            'uuid',
            'offer_type',
            'price',
            'name',
            'location',
            'photo',
        )

    async def add_offer(self, offer: Offer) -> None:
        await self.session.execute(insert(Offers).values(**offer.model_dump()))
        await self.session.commit()

    async def delete_offers_by_uuid(self, uuid: UUID) -> None:
        await self.session.execute(delete(Offers).where(Offers.uuid == uuid))
        await self.session.commit()

    async def delete_offers_by_author_id(self, author_id: int) -> None:
        await self.session.execute(
            delete(Offers).where(
                cast(Offers.author['account_id'].as_string(), BIGINT) == author_id
            )
        )
        await self.session.commit()

    async def cleanup_offers(self) -> None:
        await self.session.execute(delete(Offers))
        await self.session.commit()

    async def get_offers_by_uuid(self, uuid) -> list[Offer]:
        result = await self.session.execute(select(Offers).where(Offers.uuid == uuid))
        return [
            Offer(**dict(zip(self.offer_params, i._tuple()))) for i in result.fetchall()
        ]

    async def get_all_offers(self) -> list[Offer]:
        result = await self.session.execute(select(Offers))
        return [
            Offer(**dict(zip(self.offer_params, i._tuple()))) for i in result.fetchall()
        ]

    async def get_all_short_offfers(self) -> list[ShortOffer]:
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

    async def get_filters_offers(
        self,
        value: SearchValidate,
    ) -> list[Offer]:
        exp = []
        if (
            (value.offer_type is None)
            and (value.uuid is None)
            and (value.author_id is None)
            and (value.author_name is None)
            and (value.price is None)
            and (value.area is None)
        ):
            return await self.get_all_offers()
        if value.uuid is not None:
            return await self.get_offers_by_uuid(value.uuid)
        if value.offer_type is not None:
            exp.append(Offers.offer_type == value.offer_type.value)
        if value.author_id is not None:
            exp.append(
                cast(Offers.author['account_id'].as_string(), BIGINT) == value.author_id
            )
        if value.author_name is not None:
            exp.append(Offers.author['name'].as_string() == value.author_name)
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
            Offer(**dict(zip(self.offer_params, i._tuple()))) for i in result.fetchall()
        ]
