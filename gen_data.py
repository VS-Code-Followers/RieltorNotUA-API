import random
from asyncio import run
from uuid import uuid4
from src.config import get_engine
from src.api.models import Offer, Location, OfferType
from src.db.repo.offers import OfferRepo


async def gen_offers(
    flat_num: int = 10,
    house_num: int = 10,
    office_num: int = 10,
    photo_nums: int = 5,
):
    engine = get_engine()
    async with engine.connect() as session:
        repo = OfferRepo(session)
        for j in range(house_num):
            lat = round(random.uniform(10.0, 50.0), 5)
            lon = round(random.uniform(50.0, 100.0), 5)
            await repo.add_offer(
                Offer(
                    uuid=uuid4(),
                    author_id=random.randint(100000000, 999999999),
                    offer_type=OfferType.HOUSE.value,
                    area=round(random.uniform(10.0, 50.0), 4),
                    name=f'flat_gen_{j}',
                    description=f'This is test generate data. Test number {j}',
                    location=Location(
                        text=f'Coords of Offer is ({lat}, {lon})',
                        coordinate=(lat, lon),
                    ),
                    price=random.randint(1000000, 99999999),
                    floor=random.randint(1, 24),
                    photos=[uuid4() for _ in range(photo_nums)],
                    tags=None,
                )
            )
        for i in range(flat_num):
            lat = round(random.uniform(10.0, 50.0), 5)
            lon = round(random.uniform(50.0, 100.0), 5)
            await repo.add_offer(
                Offer(
                    uuid=uuid4(),
                    author_id=random.randint(100000000, 999999999),
                    offer_type=OfferType.FLAT.value,
                    area=round(random.uniform(10.0, 50.0), 4),
                    name=f'flat_gen_{i}',
                    description=f'This is test generate data. Test number {i}',
                    location=Location(
                        text=f'Coords of Offer is ({lat}, {lon})',
                        coordinate=(lat, lon),
                    ),
                    price=random.randint(1000000, 99999999),
                    floor=random.randint(1, 24),
                    photos=[uuid4() for _ in range(photo_nums)],
                    tags={
                        'rooms_num': random.randint(1, 5),
                        'has_balcony': bool(random.randint(0, 1)),
                    },
                )
            )

        for n in range(office_num):
            lat = round(random.uniform(10.0, 50.0), 5)
            lon = round(random.uniform(50.0, 100.0), 5)
            await repo.add_offer(
                Offer(
                    uuid=uuid4(),
                    author_id=random.randint(100000000, 999999999),
                    offer_type=OfferType.OFFICE.value,
                    area=round(random.uniform(10.0, 50.0), 4),
                    name=f'flat_gen_{n}',
                    description=f'This is test generate data. Test number {n}',
                    location=Location(
                        text=f'Coords of Offer is ({lat}, {lon})',
                        coordinate=(lat, lon),
                    ),
                    price=random.randint(1000000, 99999999),
                    floor=random.randint(1, 24),
                    photos=[uuid4() for _ in range(photo_nums)],
                    tags={'has_secure': bool(random.randint(0, 1))},
                )
            )
    await engine.dispose()

run(gen_offers())