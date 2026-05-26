from sqlalchemy import (
    Column, Integer, DateTime, Numeric, ForeignKey, func, Boolean, Index, text)
from app.db.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True)

    order_id = Column(Integer, ForeignKey("orders.order_id", deferrable=True, initially="IMMEDIATE"), nullable=False)
    item_id = Column(Integer, ForeignKey("menu_items.item_id", deferrable=True, initially="IMMEDIATE"), nullable=False)

    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(8, 2), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    created_by = Column(Integer)
    updated_by = Column(Integer)

    is_deleted = Column(Boolean, server_default="false")

    __table_args__ = (
        Index("idx_active_order_items", "order_item_id", postgresql_where=text("is_deleted = false")),
    )