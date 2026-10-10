from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any
from datetime import datetime


# Auth
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    location: Optional[str] = "Karnal, India"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    location: Optional[str]
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# Field
class FieldCreate(BaseModel):
    name: str
    location: Optional[str] = None
    area_hectares: float = 1.0
    crop_type: Optional[str] = None


class FieldOut(BaseModel):
    id: int
    name: str
    location: Optional[str]
    area_hectares: float
    status: str
    crop_type: Optional[str]
    owner_id: int

    class Config:
        from_attributes = True


# Yield
class YieldRecordOut(BaseModel):
    id: int
    crop: str
    year: int
    predicted_yield: Optional[float]
    historical_yield: Optional[float]
    actual_yield: Optional[float]

    class Config:
        from_attributes = True


class YieldPredictionResponse(BaseModel):
    crop_yields: List[dict]
    current_year_prediction: float
    unit: str = "Tons/Hectare"
    year: int = 2024
    chart_data: dict


# Soil
class SoilDataOut(BaseModel):
    moisture_percent: float
    ph: Optional[float]
    nitrogen: Optional[float]
    phosphorus: Optional[float]
    potassium: Optional[float]
    temperature: Optional[float]
    status: str  # Optimal / Low / High
    npk_status: str

    class Config:
        from_attributes = True


# Weather
class WeatherOut(BaseModel):
    location: str
    temperature: float
    condition: str
    humidity: Optional[float]
    wind_speed: Optional[float]
    precipitation: Optional[float]
    forecast: Optional[List[dict]]
    alert: Optional[str]


# Chat
class ChatRequest(BaseModel):
    message: str
    image_url: Optional[str] = None


class ChatMessageOut(BaseModel):
    id: int
    role: str
    content: str
    image_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    reply: str
    recommendations: Optional[List[str]] = None


# Dashboard summary
class DashboardSummary(BaseModel):
    yield_prediction: YieldPredictionResponse
    soil: SoilDataOut
    field: FieldOut
    weather: WeatherOut
    recent_chats: List[ChatMessageOut]
