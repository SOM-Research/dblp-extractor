from model import Base
from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship, Mapped

from model.Researcher import Researcher

class ResearcherName(Base):
    __tablename__ = "researcher_names"
    researcher_id = Column(UUID, ForeignKey(Researcher.id), primary_key=True)
    researcher: Mapped["Researcher"] = relationship(back_populates="names")
    name = Column(String, primary_key=True)