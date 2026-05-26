from __future__ import annotations

from dataclasses import dataclass
from typing import AsyncIterator, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import AsyncSessionLocal
from app.repository.order_repository import OrderRepository
from app.repository.user_repository import UserRepository
from app.repository.restaurant_repository import RestaurantRepository
from app.repository.cart import CartRepository
from app.repository.address_repository import AddressRepository
from app.repository.menu_items_repository import ItemRepository
from app.repository.cart_items_repository import CartItemRepository


@dataclass
class UnitOfWork:
    session: AsyncSession

    # optional: expose repos bound to the same session
    orders: OrderRepository
    users: UserRepository
    restaurants: RestaurantRepository
    carts: CartRepository
    addresses: AddressRepository
    items: ItemRepository
    cart_items: CartItemRepository

    @classmethod
    async def create(cls) -> "UnitOfWork":
        session = AsyncSessionLocal()
        return cls(
            session=session,
            orders=OrderRepository(session),
            users=UserRepository(session),
            restaurants=RestaurantRepository(session),
            carts=CartRepository(session),
            addresses=AddressRepository(session),
            items=ItemRepository(session),
            cart_items=CartItemRepository(session),
        )

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        try:
            if exc is None:
                await self.session.commit()
            else:
                await self.session.rollback()
        finally:
            await self.session.close()


async def get_uow() -> AsyncIterator[UnitOfWork]:
    async with await UnitOfWork.create() as uow:
        yield uow
