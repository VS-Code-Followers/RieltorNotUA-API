from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from ..models import Offers

class OfferRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    def add_offer(
        self
    ):
        ...