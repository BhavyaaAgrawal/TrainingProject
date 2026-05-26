from sqlalchemy import (
    Column, Integer, DateTime, ForeignKey, Boolean, Index, func, text)
from app.db.database import Base

class CartItem(Base):
    __tablename__ = "cart_items"

    cart_item_id = Column(Integer, primary_key=True)

    cart_id = Column(
        Integer,
        ForeignKey("cart.cart_id", deferrable=True, initially="IMMEDIATE"),
        nullable=False
    )

    item_id = Column(
        Integer,
        ForeignKey("menu_items.item_id", deferrable=True, initially="IMMEDIATE"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    created_by = Column(Integer)
    updated_by = Column(Integer)

    is_deleted = Column(Boolean, server_default="false")

    __table_args__ = (
        Index("idx_active_cart_items", "cart_item_id", postgresql_where=text("is_deleted = false")),
    )