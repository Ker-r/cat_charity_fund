from sqlalchemy import Column, String, Text

from .base import CharityBase


class CharityProject(CharityBase):

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
