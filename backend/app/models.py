from sqlalchemy import Column, String, TIMESTAMP, func
from .database import Base
import uuid

class Case(Base):
    __tablename__ = "cases"
    
    id = Column(String, primary_key=True, index=True, default=lambda: f"case_{uuid.uuid4().hex[:16]}")
    created_at = Column(TIMESTAMP(timezone=True), index=True, default=func.now())
    status = Column(String, default="submitted")