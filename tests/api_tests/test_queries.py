import random
from uuid import uuid4
from src.api.models import OfferType
from main import app
from fastapi.testclient import TestClient


class TestQueryAPI:
    iterations = 20
    client = TestClient(app)

    def test_create_db(self):
        data = []
        for j in range(self.iterations):
            offer_type = random.choice(
                [OfferType.FLAT, OfferType.HOUSE, OfferType.OFFICE]
            )
            tags = (
                None
                if offer_type == OfferType.HOUSE
                else (
                    {
                        'rooms_num': random.randint(1, 5),
                        'has_balcony': bool(random.randint(0, 1)),
                    }
                    if offer_type == OfferType.FLAT
                    else ({'has_secure': bool(random.randint(0, 1))})
                )
            )
            lat = round(random.uniform(10.0, 90.0), 5)
            lon = round(random.uniform(10.0, 90.0), 5)
            model = dict(
                uuid=str(uuid4()),
                author=dict(
                    name=f'test_name{j}',
                    account_id=random.randint(100000000, 999999999),
                ),
                offer_type=offer_type.value,
                area=round(random.uniform(10.0, 50.0), 4),
                name=f'flat_gen_{j}',
                description=f'This is test generate data. Test number {j}',
                location=dict(
                    text=f'Coords of Offer is ({lat}, {lon})',
                    coordinate=dict(latitude=lat, longitude=lon),
                ),
                price=random.randint(1000000, 99999999),
                floor=random.randint(1, 24),
                photos=[str(uuid4()) for _ in range(self.iterations)],
                tags=tags,
            )
            data.append(model)
            result = self.client.post(url='/query/create', json=model).json()
            assert result == {'msg': 'Successfully created model', 'status_code': 200}
            all_offers = self.client.post(url='/search', json={}).json()
        for n in data:
            assert n in all_offers
