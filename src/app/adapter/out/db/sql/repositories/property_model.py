from sqlalchemy import Column, Integer, String

from ..repository import SQLRepository
from .base import BaseSQLModel


class Property(BaseSQLModel):
    __tablename__ = "properties"
    street_name = Column(String(80), nullable=True)
    postal_code = Column(String(10), nullable=True)
    city = Column(String(80), nullable=True)
    county = Column(String(80), nullable=True)
    state_code = Column(String(10), nullable=True)
    country = Column(String(80), nullable=True)


class PropertyRepositorySQL(SQLRepository):
    model = Property
    model_dto = PropertyDTO

