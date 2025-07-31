from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class Attachment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    deal_id: int = Field(foreign_key="deal.id")
    filename: str
    s3_key: str
    thumb_key: Optional[str] = None  # NEW
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
  Add models.py with thumb_key field.
