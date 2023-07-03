from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationMyDB(DonationCreate):
    id: int
    create_date: datetime = datetime.now

    class Config:
        orm_mode = True


class DonationDB(DonationMyDB):
    user_id: Optional[int]
    invested_amount: int = 0
    fully_invested: bool = False
    close_date: datetime = None
