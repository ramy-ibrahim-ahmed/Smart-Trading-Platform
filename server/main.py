import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .helpers.db_conf import ENGINE, ORM_BASE
from .routes import user_router, car_router, order_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with ENGINE.begin() as conn:
        await conn.run_sync(ORM_BASE.metadata.create_all)
    yield
    await ENGINE.dispose()


app = FastAPI(
    lifespan=lifespan,
    openapi_url="/openapi.json",
    root_path="/api/server",
)

app.include_router(user_router)
app.include_router(car_router)
app.include_router(order_router)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the API!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
