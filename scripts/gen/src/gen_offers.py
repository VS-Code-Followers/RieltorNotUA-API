from os import getcwd
from sys import path

path.insert(0, getcwd())

import random
from argparse import ArgumentParser
from asyncio import run
from typing import Optional
from uuid import uuid4

from src.config import get_engine
from src.api.models import Offer, Location, OfferType, Author
from src.db.repo.offers import OfferRepo


async def gen_offers(
    gen_num: Optional[int],
    flat_num: Optional[int],
    house_num: Optional[int],
    office_num: Optional[int],
    photo_nums: int,
):
    if gen_num is not None:
        flat_num, house_num, office_num = [gen_num] * 3
    elif not (
        isinstance(flat_num, int)
        and isinstance(house_num, int)
        and isinstance(office_num, int)
        and isinstance(photo_nums, int)
    ):
        raise ValueError('Args is not int!')
    engine = get_engine()
    async with engine.connect() as session:
        repo = OfferRepo(session)
        for j in range(house_num):
            lat = round(random.uniform(10.0, 50.0), 5)
            lon = round(random.uniform(50.0, 100.0), 5)
            await repo.add_offer(
                Offer(
                    uuid=uuid4(),
                    author=Author(
                        name=f'test_name{j}',
                        account_id=random.randint(100000000, 999999999),
                    ),
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
                    author=Author(
                        name=f'test_name{i}',
                        account_id=random.randint(100000000, 999999999),
                    ),
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
                    author=Author(
                        name=f'test_name{n}',
                        account_id=random.randint(100000000, 999999999),
                    ),
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


parser = ArgumentParser()
parser.add_argument(
    '--gen_num', help='General amount of each offer type', default=None, type=int
)
parser.add_argument(
    '--flat_num', help='Amount of flat-type offers', default=None, type=int
)
parser.add_argument(
    '--house_num', help='Amount of house-type offers', default=None, type=int
)
parser.add_argument(
    '--office_num', help='Amount of office-type offers', default=None, type=int
)
parser.add_argument('--photo_num', help='Amount of photos in each offer', type=int)
args = parser.parse_args()
run(
    gen_offers(
        args.gen_num, args.flat_num, args.house_num, args.office_num, args.photo_num
    )
)
