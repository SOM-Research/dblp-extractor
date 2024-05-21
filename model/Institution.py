from model import ModelBase
from sqlalchemy import Column, String, UUID
from sqlalchemy.dialects.postgresql import ARRAY

class Institution(ModelBase):
    __tablename__ = "institutions"

    uuid = Column(UUID, primary_key=True)
    name = Column(String, unique=True)
    version_names = Column(ARRAY(String))
    country = Column(String)