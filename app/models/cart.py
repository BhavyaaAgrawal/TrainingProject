from sqlalchemy import (
    Column, Integer, ForeignKey, DateTime, Boolean, func, Index, text)
from app.db.database import Base

class Cart(Base):
    __tablename__ = "cart"

    cart_id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", deferrable=True, initially="IMMEDIATE"),
        unique=True,
        nullable=False
    )

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.restaurant_id", deferrable=True, initially="IMMEDIATE"),
        nullable=False
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    created_by = Column(Integer)
    updated_by = Column(Integer)

    is_deleted = Column(Boolean, server_default="false")

    __table_args__ = (
        Index("idx_active_cart", "cart_id", postgresql_where=text("is_deleted = false")),
    )