from model import Base
from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship, Mapped

from model.Researcher import Researcher

class XmlKey(Base):
    __tablename__ = "researcher_xml_keys"
    researcher_id = Column(UUID, ForeignKey(Researcher.id), primary_key=True)
    researcher: Mapped["Researcher"] = relationship(back_populates="xml_cross_reference")
    xml_key = Column(String, primary_key=True)

