from model import ModelBase
from sqlalchemy import Column, String, UUID

class Institution(ModelBase):
    __tablename__ = "institutions"

    id = Column(UUID, primary_key=True)
    name = Column(String, unique=True)
