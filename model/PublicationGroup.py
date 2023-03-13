from model import ModelBase
from typing import List
from sqlalchemy import Column, String, UUID, DATE, Text, Integer, Enum
from sqlalchemy.orm import relationship, Mapped

class PublicationGroup(ModelBase):
    __tablename__ = "publication_groups"
    id = Column(UUID, primary_key=True)
    title = Column(String)
    #publication_venue
    publisher = Column(String)
    year = Column(Integer)
    isbn = Column(String)
    booktitle = Column(String)
    serie = Column(String)
    volume = Column(Integer)
    number = Column(String)
    xml_key = Column(String)
    xml_mdate = Column(DATE)
    xml_item = Column(Text)
    #publications: Mapped[List["Publication"]]