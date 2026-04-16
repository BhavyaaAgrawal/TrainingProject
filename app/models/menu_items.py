from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base
from sqlalchemy import Index, text

class MenuItem(Base):
    __tablename__ = "menu_items"

    item_id = Column(Integer, primary_key=True)

    restaurant_id = Column(
        Integer,
        ForeignKey(
            "restaurants.restaurant_id",
            deferrable=True,
            initially="IMMEDIATE"
        ),
        nullable=False
    )

    name = Column(String(150), nullable=False)
    description = Column(Text)
    price = Column(Numeric(8, 2), nullable=False)

    is_veg = Column(Boolean)
    is_available = Column(Boolean)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    created_by = Column(Integer)
    updated_by = Column(Integer)

    is_deleted = Column(Boolean, server_default="false")

    restaurant = relationship("Restaurant", back_populates="menu_items")

    # INDEX DEFINED HERE
    __table_args__ = (
        Index(
            "idx_active_menu_items",
            "item_id",  # use string, not MenuItem.item_id
            postgresql_where=text("is_deleted = false")
        ),
    )