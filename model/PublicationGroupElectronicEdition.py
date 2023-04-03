from model import ModelBase
from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship, Mapped

class PublicationGroupElectronicEdition(ModelBase):
    __tablename__ = "publication_group_electronic_editions"
    publication_group_id = Column(UUID, ForeignKey("publication_groups.id"), primary_key=True)
    publication_group: Mapped["PublicationGroup"] = relationship(back_populates="electronic_editions")
    electronic_edition = Column(String, primary_key=True)