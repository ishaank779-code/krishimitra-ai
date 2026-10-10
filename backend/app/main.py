from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, SessionLocal
from app.models.models import User, Field, YieldRecord, SoilData, WeatherData, ChatMessage
from app.services.auth import get_password_hash
from app.routers import auth, dashboard
from app.config import get_settings

settings = get_settings()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KrishiMitra AI",
    description="Smart Crop Yield Predictor & AI Farming Assistant",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(dashboard.router)


def seed_data():
    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(User).filter(User.email == "rahul@krishimitra.ai").first():
            return

        # Create demo user (Farmer Rahul)
        user = User(
            name="Farmer Rahul",
            email="rahul@krishimitra.ai",
            phone="+91-9876543210",
            location="Karnal, India",
            hashed_password=get_password_hash("rahul123"),
            role="farmer",
        )
        db.add(user)
        db.flush()

        # Field
        field = Field(
            name="Alpha Farm",
            location="Karnal, Haryana",
            area_hectares=2.5,
            status="optimal",
            crop_type="Mixed (Maize, Wheat, Rice)",
            owner_id=user.id,
        )
        db.add(field)
        db.flush()

        # Yield records
        yields = [
            YieldRecord(field_id=field.id, crop="Maize", year=2024, predicted_yield=5.2, historical_yield=4.8),
            YieldRecord(field_id=field.id, crop="Wheat", year=2024, predicted_yield=4.5, historical_yield=4.1),
            YieldRecord(field_id=field.id, crop="Rice", year=2024, predicted_yield=6.8, historical_yield=6.2),
            YieldRecord(field_id=field.id, crop="Maize", year=2023, predicted_yield=4.9, historical_yield=4.6),
            YieldRecord(field_id=field.id, crop="Wheat", year=2023, predicted_yield=4.2, historical_yield=3.9),
            YieldRecord(field_id=field.id, crop="Rice", year=2023, predicted_yield=6.3, historical_yield=5.9),
        ]
        db.add_all(yields)

        # Soil data
        soil = SoilData(
            field_id=field.id,
            moisture_percent=58.5,
            ph=6.2,
            nitrogen=45.0,
            phosphorus=30.0,
            potassium=40.0,
            temperature=28.0,
            is_current=True,
        )
        db.add(soil)

        # Weather
        weather = WeatherData(
            location="Karnal, India",
            temperature=28.0,
            condition="Partly Cloudy",
            humidity=65.0,
            wind_speed=12.0,
            precipitation=20.0,
            forecast=[
                {"day": "1 Dy", "icon": "cloud-sun", "temp": 29},
                {"day": "2 Dy", "icon": "cloud", "temp": 27},
                {"day": "3 Dy", "icon": "cloud-rain", "temp": 26},
                {"day": "4 Dy", "icon": "cloud", "temp": 28},
                {"day": "5 Dy", "icon": "sun", "temp": 30},
            ],
            alert="Weather warning",
        )
        db.add(weather)

        # Sample chat
        chats = [
            ChatMessage(
                user_id=user.id,
                role="user",
                content="Pest activity on tomato leaves, what to do?",
            ),
            ChatMessage(
                user_id=user.id,
                role="assistant",
                content="Hi Rahul! Based on symptoms, it appears to be Aphids. Apply Neem oil spray and introduce beneficial insects. (Attached Image, recommendations, products).",
            ),
        ]
        db.add_all(chats)

        db.commit()
        print("✅ Database seeded successfully with demo data.")
        print("   Login: rahul@krishimitra.ai / rahul123")
    except Exception as e:
        db.rollback()
        print(f"Seed error: {e}")
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    seed_data()


@app.get("/")
def root():
    return {
        "app": "KrishiMitra AI",
        "version": "1.0.0",
        "message": "Smart Crop Yield Predictor API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
