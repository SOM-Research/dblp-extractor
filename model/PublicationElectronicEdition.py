from model import ModelBase
from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship, Mapped

class PublicationElectronicEdition(ModelBase):
    __tablename__ = "publication_electronic_editions"
    publication_id = Column(UUID, ForeignKey("publications.id"), primary_key=True)
    publication: Mapped["Publication"] = relationship(back_populates="electronic_editions")
    electronic_edition = Column(String, primary_key=True)