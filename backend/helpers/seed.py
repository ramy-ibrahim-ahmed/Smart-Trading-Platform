import random
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from ..models import UserModel, CarModel, OrderModel
from .db_conf import ENGINE, ORM_BASE
from .hash import hash_password

FIRST_NAMES = [
    "John",
    "Jane",
    "Michael",
    "Emily",
    "Chris",
    "Sarah",
    "David",
    "Laura",
    "James",
    "Anna",
    "Robert",
    "Linda",
    "William",
    "Patricia",
    "Richard",
    "Barbara",
]
LAST_NAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
    "Hernandez",
    "Lopez",
    "Gonzalez",
    "Wilson",
]

BRANDS = [
    "Toyota",
    "Honda",
    "Ford",
    "Chevrolet",
    "BMW",
    "Mercedes-Benz",
    "Audi",
    "Volkswagen",
    "Nissan",
    "Hyundai",
    "Tesla",
    "Subaru",
    "Mazda",
    "Kia",
    "Lexus",
]
BODY_TYPES = [
    "Sedan",
    "Hatchback",
    "Coupe",
    "SUV",
    "Truck",
    "Convertible",
    "Minivan",
    "Wagon",
]
ENGINE_TYPES = ["Inline-4", "V6", "V8", "Electric", "Hybrid", "Inline-6"]
TRANSMISSIONS = ["Automatic", "Manual", "CVT", "Dual-Clutch"]
FUEL_TYPES = ["Gasoline", "Diesel", "Electric", "Hybrid", "Plug-in Hybrid"]
COLORS = [
    "Black",
    "White",
    "Silver",
    "Red",
    "Blue",
    "Gray",
    "Green",
    "Yellow",
    "Orange",
]
FEATURES_POOL = [
    "Bluetooth",
    "Cruise Control",
    "Backup Camera",
    "Apple CarPlay",
    "Android Auto",
    "Lane Assist",
    "Leather Seats",
    "Premium Audio",
    "Navigation",
    "Sunroof",
    "Heated Seats",
    "Adaptive Headlights",
    "Blind Spot Monitoring",
]

DESCRIPTIONS = [
    "Reliable {body_type} with great fuel efficiency.",
    "Sporty {body_type} with modern tech features.",
    "Powerful {body_type} for performance enthusiasts.",
    "Luxurious {body_type} with premium amenities.",
    "Efficient {body_type} ideal for daily commuting.",
    "Versatile {body_type} for family use.",
    "Eco-friendly {body_type} with low emissions.",
]

NUM_USERS = 100
NUM_CARS = 500
NUM_ORDERS = 200
MIN_CARS_PER_ORDER = 1
MAX_CARS_PER_ORDER = 5


async def seed_database():
    async with ENGINE.begin() as conn:
        await conn.run_sync(ORM_BASE.metadata.create_all)

    async_session = async_sessionmaker(ENGINE, expire_on_commit=False)
    async with async_session() as session:
        users_result = await session.execute(select(UserModel))
        if users_result.scalars().all():
            print("Database already seeded. Skipping.")
            return

        users = []
        for i in range(NUM_USERS):
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            username = (
                f"{first_name.lower()}_{last_name.lower()}_{random.randint(1, 999)}"
            )
            email = f"{username}@example.com"
            user = UserModel(
                username=username,
                email=email,
                hashed_password=hash_password("password123"),
                is_active=random.choice([True, False]),
                created_at=datetime.utcnow()
                - timedelta(days=random.randint(0, 365 * 2)),
            )
            users.append(user)
        session.add_all(users)
        await session.commit()
        for user in users:
            await session.refresh(user)

        cars = []
        for i in range(NUM_CARS):
            brand = random.choice(BRANDS)
            model = random.choice(
                [
                    "Camry",
                    "Civic",
                    "Mustang",
                    "Accord",
                    "F-150",
                    "Model 3",
                    "X5",
                    "A4",
                    "Passat",
                    "Altima",
                    "Elantra",
                ]
            )
            year = random.randint(2015, 2025)
            body_type = random.choice(BODY_TYPES)
            engine_type = random.choice(ENGINE_TYPES)
            engine_size_liters = round(random.uniform(1.0, 6.0), 1)
            horsepower = random.randint(100, 600)
            transmission = random.choice(TRANSMISSIONS)
            fuel_type = random.choice(FUEL_TYPES)
            mileage_km = random.randint(0, 200000)
            top_speed_kmh = random.randint(150, 300)
            color = random.choice(COLORS)
            num_features = random.randint(3, 8)
            features = ", ".join(random.sample(FEATURES_POOL, num_features))
            price_usd = round(random.uniform(10000, 100000), 2)
            discount_percent = round(random.uniform(0, 20), 1)
            num_in_stock = random.randint(0, 20)
            description_template = random.choice(DESCRIPTIONS)
            description = description_template.format(body_type=body_type.lower())

            car = CarModel(
                brand=brand,
                model=model,
                year=year,
                body_type=body_type,
                engine_type=engine_type,
                engine_size_liters=engine_size_liters,
                horsepower=horsepower,
                transmission=transmission,
                fuel_type=fuel_type,
                mileage_km=mileage_km,
                top_speed_kmh=top_speed_kmh,
                color=color,
                features=features,
                price_usd=price_usd,
                discount_percent=discount_percent,
                num_in_stock=num_in_stock,
                description=description,
            )
            cars.append(car)
        session.add_all(cars)
        await session.commit()
        for car in cars:
            await session.refresh(car)

        # Seed Orders
        orders = []
        for i in range(NUM_ORDERS):
            user = random.choice(users)
            num_cars_in_order = random.randint(MIN_CARS_PER_ORDER, MAX_CARS_PER_ORDER)
            selected_cars = random.sample(cars, num_cars_in_order)
            order = OrderModel(
                user_id=user.id,
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 365)),
                cars=selected_cars,
            )
            orders.append(order)
        session.add_all(orders)
        await session.commit()

        print(
            f"Database seeded with {NUM_USERS} users, {NUM_CARS} cars, and {NUM_ORDERS} orders."
        )
