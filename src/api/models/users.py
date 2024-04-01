from pydantic import BaseModel


class Author(BaseModel):
    account_id: int
    name: str
