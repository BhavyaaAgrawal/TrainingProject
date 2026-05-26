from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logger import setup_logger
from app.core.middleware.request_logger import RequestLoggingMiddleware
from app.routers import (user, menu_items, user_address,
                         restaurant, orders, cart, background_tasks,
                         cart_items)
from app.core.exceptions.exception_handlers import register_exception_handlers


def register_api_routers(app: FastAPI):
    app.include_router(user.router)
    app.include_router(menu_items.router)
    app.include_router(user_address.router)
    app.include_router(restaurant.router)
    app.include_router(orders.router)
    app.include_router(cart.router)
    app.include_router(background_tasks.router)
    app.include_router(cart_items.router)

def bootstrap(app: FastAPI):
    # initiate logging
    logger = setup_logger()
    logger.info('Bootstrapping FastAPI app')

    # to allow cross origin and to avoid cors error
    origins = [
        "http://localhost:1234",
    ]
    #initiate request middleware
    app.add_middleware(RequestLoggingMiddleware)

    app.add_middleware(CORSMiddleware,
                       allow_origins=origins,
                       allow_credentials=True,
                       allow_methods=["*"],
                       allow_headers=["*"])

    app.include_router(user.router)

    # register exception handler
    register_exception_handlers(app)

    #initiate api routes
    register_api_routers(app)