from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, CheckConstraint
from sqlalchemy import Index, text
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(15))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    created_by = Column(Integer)
    updated_by = Column(Integer)

    is_deleted = Column(Boolean, server_default="false")
    __table_args__ = (
        Index(
            "idx_active_users",
            "user_id",
            postgresql_where=text("is_deleted = false")
        ),
        CheckConstraint("length(password) > 0", name="password_not_empty")
    )

