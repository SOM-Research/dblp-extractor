from model import ModelBase
from sqlalchemy import Column, Integer, ForeignKey, UUID
from sqlalchemy.orm import relationship, Mapped

class Editor(ModelBase):
    __tablename__ = "editors"
    researcher_id = Column(UUID, ForeignKey("researchers.id"), primary_key=True)
    researcher: Mapped["Researcher"] = relationship("Researcher", back_populates="publication_groups")
    publication_group_id = Column(UUID, ForeignKey("publication_groups.id"),  primary_key=True)
    publication_group: Mapped["PublicationGroup"] = relationship("PublicationGroup", back_populates="editors")
    position = Column(Integer)