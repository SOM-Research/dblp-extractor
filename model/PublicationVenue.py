from model import ModelBase
from typing import List
from sqlalchemy import Column, String, UUID, Enum
from sqlalchemy.orm import relationship, Mapped
from model.PublicationVenueType import PublicationVenueType

class PublicationVenue(ModelBase):
    __tablename__ = "publication_venues"
    id = Column(UUID, primary_key=True)
    name = Column(String)
    type = Column(Enum(PublicationVenueType))
    publication_groups: Mapped[List["PublicationGroup"]] = relationship(back_populates="venue")
