from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from ..models import Offers
from ...api.models.core import Offer

class OfferRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    def add_offer(
        self, offer: Offer
    ):
        insert(Offers)
    
    def delete_offer(
        self
    ):
        ...
        
    def get_offer(
        self
    ):
        ...
        
    def get_offers(
        
    ):
        ...