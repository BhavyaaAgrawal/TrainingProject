from sqlalchemy import (
    Column, ForeignKey, Integer, Numeric, DateTime, Enum, Boolean, Index, func, text)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
import enum


class OrderStatus(str, enum.Enum):
    pending = "pending"
    preparing = "preparing"
    delivered = "delivered"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.user_id", deferrable=True, initially="IMMEDIATE"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id", deferrable=True, initially="IMMEDIATE"), nullable=False)
    offer_id = Column(Integer, ForeignKey("offers.offer_id", deferrable=True, initially="IMMEDIATE"))

    total_amount = Column(Numeric(10, 2), nullable=False)
    discount_amount = Column(Numeric(10, 2))
    final_amount = Column(Numeric(10, 2), nullable=False)

    order_status: Mapped[OrderStatus]=mapped_column(
        Enum(OrderStatus, name="order_status_enum"),
        server_default="pending"
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    created_by = Column(Integer)
    updated_by = Column(Integer)

    is_deleted = Column(Boolean, server_default="false")

    __table_args__ = (
        Index("idx_active_orders", "order_id", postgresql_where=text("is_deleted = false")),
    )