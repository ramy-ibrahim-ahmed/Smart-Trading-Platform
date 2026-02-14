import json
import uvicorn
import aio_pika
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from .helpers.db_conf import ENGINE, ORM_BASE
from .helpers.seed import seed_database
from .models import UserModel, CarModel, OrderModel, order_items
from .routes import user_router, car_router, order_router

RABBITMQ_URL = "amqp://guest:guest@rabbitmq:5672/"
QUEUE_NAME = "db_export_queue"


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with ENGINE.begin() as conn:
        await conn.run_sync(ORM_BASE.metadata.create_all)

    app.state.rabbit_conn = await aio_pika.connect_robust(RABBITMQ_URL)

    scheduler = AsyncIOScheduler()
    scheduler.start()

    async def export_db_data():
        async_session = async_sessionmaker(ENGINE, expire_on_commit=False)
        async with async_session() as session:
            users = await session.execute(select(UserModel))
            cars = await session.execute(select(CarModel))
            orders = await session.execute(select(OrderModel))
            order_items_data = await session.execute(select(order_items))

            data = {
                "users": [u.__dict__ for u in users.scalars().all()],
                "cars": [c.__dict__ for c in cars.scalars().all()],
                "orders": [o.__dict__ for o in orders.scalars().all()],
                "order_items": [row._asdict() for row in order_items_data.all()],
            }

        channel = await app.state.rabbit_conn.channel()
        message = aio_pika.Message(
            body=json.dumps(data, default=str).encode(), delivery_mode=2
        )
        await channel.default_exchange.publish(message, routing_key=QUEUE_NAME)
        print("DB data sent to queue")

    scheduler.add_job(export_db_data, IntervalTrigger(minutes=1), misfire_grace_time=30)
    await seed_database()

    yield

    scheduler.shutdown()
    await app.state.rabbit_conn.close()
    await ENGINE.dispose()


app = FastAPI(
    lifespan=lifespan,
    openapi_url="/openapi.json",
    root_path="/api/backend",
)

app.include_router(user_router)
app.include_router(car_router)
app.include_router(order_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the API!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
