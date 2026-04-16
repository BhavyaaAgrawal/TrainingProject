from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship, mapped_column, Mapped
import enum
from sqlalchemy import func
from sqlalchemy import Index, text

from app.db.database import Base


#  Enum for restaurant status
class RestaurantStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    closed = "closed"


class Restaurant(Base):
    __tablename__ = "restaurants"

    restaurant_id = Column(Integer, primary_key=True)

    name = Column(String(150), nullable=False)
    address = Column(Text, nullable=True)
    phone_number = Column(String(15), nullable=True)

    status: Mapped[RestaurantStatus] = mapped_column(
        Enum(RestaurantStatus, name="restaurant_status_enum"),
        server_default="active",
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)

    is_deleted = Column(Boolean, server_default="false")

    # Relationship
    menu_items = relationship("MenuItem", back_populates="restaurant")

    __table_args__ = (
        Index(
            "idx_active_restaurants",
            "restaurant_id",
            postgresql_where=text("is_deleted = false")
        ),
    )