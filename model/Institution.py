from model import Base
from sqlalchemy import Column, String, UUID

class Institution(Base):
    __tablename__ = "institutions"

    id = Column(UUID, primary_key=True)
    name = Column(String, unique=True)
