from enum import Enum


class RestaurantStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    closed = "closed"


class OrderStatus(str, Enum):
    pending = "pending"
    preparing = "preparing"
    delivered = "delivered"
    cancelled = "cancelled"


class DiscountType(str, Enum):
    percent = "percent"
    fixed = "fixed"