from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    FARMER = "farmer"
    ADMIN = "admin"


class FieldStatus(str, enum.Enum):
    OPTIMAL = "optimal"
    WARNING = "warning"
    CRITICAL = "critical"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default=UserRole.FARMER.value)
    location = Column(String(100), default="Karnal, India")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    fields = relationship("Field", back_populates="owner")
    chats = relationship("ChatMessage", back_populates="user")


class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(150), nullable=True)
    area_hectares = Column(Float, default=1.0)
    status = Column(String(20), default=FieldStatus.OPTIMAL.value)
    crop_type = Column(String(50), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="fields")
    yield_records = relationship("YieldRecord", back_populates="field")
    soil_data = relationship("SoilData", back_populates="field")


class YieldRecord(Base):
    __tablename__ = "yield_records"

    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.id"))
    crop = Column(String(50), nullable=False)  # Maize, Wheat, Rice
    year = Column(Integer, nullable=False)
    predicted_yield = Column(Float, nullable=True)  # tons/hectare
    historical_yield = Column(Float, nullable=True)
    actual_yield = Column(Float, nullable=True)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())

    field = relationship("Field", back_populates="yield_records")


class SoilData(Base):
    __tablename__ = "soil_data"

    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.id"))
    moisture_percent = Column(Float, nullable=False)
    ph = Column(Float, nullable=True)
    nitrogen = Column(Float, nullable=True)  # N
    phosphorus = Column(Float, nullable=True)  # P
    potassium = Column(Float, nullable=True)  # K
    temperature = Column(Float, nullable=True)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    is_current = Column(Boolean, default=True)

    field = relationship("Field", back_populates="soil_data")


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(100), nullable=False)
    temperature = Column(Float, nullable=False)
    condition = Column(String(50), nullable=False)  # Partly Cloudy, etc.
    humidity = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    precipitation = Column(Float, nullable=True)
    forecast = Column(JSON, nullable=True)  # 5-day forecast
    alert = Column(String(255), nullable=True)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String(20), nullable=False)  # user / assistant
    content = Column(Text, nullable=False)
    image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="chats")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    crop = Column(String(50), nullable=True)
    category = Column(String(50), nullable=True)  # pest, irrigation, fertilizer
    priority = Column(String(20), default="medium")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
