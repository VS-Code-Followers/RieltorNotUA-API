from httpx import AsyncClient
from pydantic_extra_types.coordinate import Coordinate
from src.config import get_config

API_KEY = get_config().tools.geocoding_api_key


async def get_full_adress(coords: Coordinate) -> str:
    async with AsyncClient() as client:
        resp = await client.get(
            url='https://maps.googleapis.com/maps/api/geocode/json?',
            params={'latlng': f'{coords.latitude},{coords.longitude}', 'key': API_KEY},
        )
        result = resp.json()['results'][0]
        formatted_adress = result.get('formatted_address')
        if not formatted_adress:
            raise Exception('No address was found')
        return formatted_adress
