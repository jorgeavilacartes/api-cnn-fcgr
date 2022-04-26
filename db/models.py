
from sqlalchemy import Column, Integer, String, Float, inspect
from .database import Base

class Inference(Base):
    __tablename__ = "inferences"

    id = Column(Integer, primary_key=True, index=True)
    fasta_id = Column(String)
    filename = Column(String)
    prediction = Column(String)
    confidence = Column(Float)

    def to_dict(self):
        "Return element as a dictionary"
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }