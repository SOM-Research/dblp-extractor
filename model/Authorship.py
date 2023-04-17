from model import ModelBase
from sqlalchemy import Column, Integer, ForeignKey, UUID
from sqlalchemy.orm import relationship, Mapped

class Authorship(ModelBase):
    __tablename__ = "authorships"
    researcher_id = Column(UUID, ForeignKey("researchers.id"), primary_key=True)
    researcher: Mapped["Researcher"] = relationship("Researcher", back_populates="publications")
    publication_id = Column(UUID, ForeignKey("publications.id"),  primary_key=True)
    publication: Mapped["Publication"] = relationship("Publication", back_populates="authors")
    position = Column(Integer, primary_key=True)