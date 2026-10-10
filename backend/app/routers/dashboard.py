from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import User, Field, YieldRecord, SoilData, WeatherData, ChatMessage
from app.schemas.schemas import (
    DashboardSummary, YieldPredictionResponse, SoilDataOut,
    FieldOut, WeatherOut, ChatMessageOut, ChatRequest, ChatResponse
)
from app.services.auth import get_current_user
from app.services.ai_service import get_ai_response

router = APIRouter(prefix="/api", tags=["Dashboard"])


@router.get("/dashboard", response_model=DashboardSummary)
def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get first field of user (or create default)
    field = db.query(Field).filter(Field.owner_id == current_user.id).first()
    if not field:
        field = Field(
            name="Alpha Farm",
            location=current_user.location or "Karnal, India",
            area_hectares=2.5,
            status="optimal",
            crop_type="Mixed",
            owner_id=current_user.id,
        )
        db.add(field)
        db.commit()
        db.refresh(field)

    # Yield data
    yields = db.query(YieldRecord).filter(YieldRecord.field_id == field.id).all()
    crop_yields = []
    for y in yields:
        crop_yields.append({
            "crop": y.crop,
            "predicted": y.predicted_yield,
            "historical": y.historical_yield,
        })

    # Default if empty
    if not crop_yields:
        crop_yields = [
            {"crop": "Maize", "predicted": 5.2, "historical": 4.8},
            {"crop": "Wheat", "predicted": 4.5, "historical": 4.1},
            {"crop": "Rice", "predicted": 6.8, "historical": 6.2},
        ]

    yield_pred = YieldPredictionResponse(
        crop_yields=crop_yields,
        current_year_prediction=6.8,
        unit="Tons/Hectare",
        year=2024,
        chart_data={
            "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"],
            "predicted": [3.2, 3.8, 4.5, 5.1, 5.6, 6.0, 6.3, 6.5, 6.7, 6.8],
            "historical": [2.9, 3.4, 4.1, 4.6, 5.0, 5.4, 5.7, 5.9, 6.1, 6.2],
        }
    )

    # Soil
    soil = db.query(SoilData).filter(
        SoilData.field_id == field.id, SoilData.is_current == True
    ).first()
    if not soil:
        soil_out = SoilDataOut(
            moisture_percent=58.5,
            ph=6.2,
            nitrogen=45.0,
            phosphorus=30.0,
            potassium=40.0,
            temperature=28.0,
            status="Optimal Range",
            npk_status="Balanced"
        )
    else:
        status = "Optimal Range" if 45 <= soil.moisture_percent <= 70 else (
            "Low" if soil.moisture_percent < 45 else "High"
        )
        soil_out = SoilDataOut(
            moisture_percent=soil.moisture_percent,
            ph=soil.ph,
            nitrogen=soil.nitrogen,
            phosphorus=soil.phosphorus,
            potassium=soil.potassium,
            temperature=soil.temperature,
            status=status,
            npk_status="Balanced"
        )

    # Weather
    weather = db.query(WeatherData).filter(
        WeatherData.location.ilike(f"%{current_user.location.split(',')[0] if current_user.location else 'Karnal'}%")
    ).order_by(WeatherData.recorded_at.desc()).first()

    if not weather:
        weather_out = WeatherOut(
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
            alert="Weather warning"
        )
    else:
        weather_out = WeatherOut(
            location=weather.location,
            temperature=weather.temperature,
            condition=weather.condition,
            humidity=weather.humidity,
            wind_speed=weather.wind_speed,
            precipitation=weather.precipitation,
            forecast=weather.forecast or [],
            alert=weather.alert
        )

    # Recent chats
    chats = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == current_user.id)
        .order_by(ChatMessage.created_at.desc())
        .limit(10)
        .all()
    )
    chats = list(reversed(chats))

    return DashboardSummary(
        yield_prediction=yield_pred,
        soil=soil_out,
        field=FieldOut.model_validate(field),
        weather=weather_out,
        recent_chats=[ChatMessageOut.model_validate(c) for c in chats]
    )


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Save user message
    user_msg = ChatMessage(
        user_id=current_user.id,
        role="user",
        content=request.message,
        image_url=request.image_url,
    )
    db.add(user_msg)

    # Get AI reply
    reply, recs = get_ai_response(request.message)

    # Save assistant message
    asst_msg = ChatMessage(
        user_id=current_user.id,
        role="assistant",
        content=reply,
    )
    db.add(asst_msg)
    db.commit()

    return ChatResponse(reply=reply, recommendations=recs)


@router.get("/chat/history", response_model=List[ChatMessageOut])
def chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chats = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == current_user.id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )
    return chats


@router.get("/fields", response_model=List[FieldOut])
def list_fields(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    fields = db.query(Field).filter(Field.owner_id == current_user.id).all()
    return fields


@router.get("/yield/{field_id}")
def get_yield_data(
    field_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    field = db.query(Field).filter(Field.id == field_id, Field.owner_id == current_user.id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    records = db.query(YieldRecord).filter(YieldRecord.field_id == field_id).all()
    return records


@router.get("/soil/{field_id}", response_model=SoilDataOut)
def get_soil(
    field_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    field = db.query(Field).filter(Field.id == field_id, Field.owner_id == current_user.id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    soil = db.query(SoilData).filter(SoilData.field_id == field_id, SoilData.is_current == True).first()
    if not soil:
        return SoilDataOut(
            moisture_percent=58.5, ph=6.2, nitrogen=45, phosphorus=30,
            potassium=40, temperature=28, status="Optimal Range", npk_status="Balanced"
        )
    status = "Optimal Range" if 45 <= soil.moisture_percent <= 70 else (
        "Low" if soil.moisture_percent < 45 else "High"
    )
    return SoilDataOut(
        moisture_percent=soil.moisture_percent,
        ph=soil.ph,
        nitrogen=soil.nitrogen,
        phosphorus=soil.phosphorus,
        potassium=soil.potassium,
        temperature=soil.temperature,
        status=status,
        npk_status="Balanced"
    )


@router.get("/weather")
def get_weather(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    loc = current_user.location or "Karnal, India"
    weather = db.query(WeatherData).filter(
        WeatherData.location.ilike(f"%{loc.split(',')[0]}%")
    ).order_by(WeatherData.recorded_at.desc()).first()
    if not weather:
        return WeatherOut(
            location=loc,
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
            alert="Weather warning"
        )
    return weather
