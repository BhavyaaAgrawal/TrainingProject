from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, ForeignKey,
    func, Text, Index, text, UniqueConstraint)
from app.db.database import Base


class UserAddress(Base):
    __tablename__ = "user_addresses"

    address_id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", deferrable=True, initially="IMMEDIATE"),
        nullable=False
    )

    address_line = Column(Text, nullable=False)
    city = Column(String(50))
    state = Column(String(50))
    pincode = Column(String(10))

    is_default = Column(Boolean, server_default="false")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    created_by = Column(Integer)
    updated_by = Column(Integer)

    is_deleted = Column(Boolean, server_default="false")

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "is_default",
            name="unique_default_address_per_user"
        ),
        Index(
            "idx_active_addresses",
            "address_id",
            postgresql_where=text("is_deleted = false")
        ),
    )