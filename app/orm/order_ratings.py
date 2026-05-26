from sqlalchemy import (
    CheckConstraint, Column, Integer, DateTime, ForeignKey, String,
    Index, Boolean, text, func, Text)
from app.db.database import Base


class OrderRating(Base):
    __tablename__ = "order_ratings"

    rating_id = Column(Integer, primary_key=True)

    order_id = Column(Integer, ForeignKey("orders.order_id", deferrable=True, initially="IMMEDIATE"), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", deferrable=True, initially="IMMEDIATE"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id", deferrable=True, initially="IMMEDIATE"), nullable=False)

    rating = Column(Integer)
    review = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    created_by = Column(Integer)
    updated_by = Column(Integer)

    is_deleted = Column(Boolean, server_default="false")

    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5"),
        Index("idx_active_order_ratings", "rating_id", postgresql_where=text("is_deleted = false")),
    )