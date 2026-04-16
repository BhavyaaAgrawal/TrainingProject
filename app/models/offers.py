import enum
from sqlalchemy import (
    Enum, Numeric, Date, Column, Integer, String, Boolean,
    func, DateTime, Index, Text, text)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class DiscountType(str, enum.Enum):
    percent = "percent"
    fixed = "fixed"


class Offer(Base):
    __tablename__ = "offers"

    offer_id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(Text)

    discount_type: Mapped[DiscountType] = mapped_column(
        Enum(DiscountType, name="discount_type_enum")
    )

    discount_value = Column(Numeric(8, 2))
    min_order_amount = Column(Numeric(10, 2))
    max_discount_amount = Column(Numeric(10, 2))

    valid_from = Column(Date)
    valid_to = Column(Date)

    is_active = Column(Boolean)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    created_by = Column(Integer)
    updated_by = Column(Integer)

    is_deleted = Column(Boolean, server_default="false")

    __table_args__ = (
        Index("idx_active_offers", "offer_id", postgresql_where=text("is_deleted = false")),
    )