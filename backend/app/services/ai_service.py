"""
Simple rule-based AI for farming recommendations.
In production, replace with OpenAI / Gemini / local LLM.
"""

from typing import Tuple, List
import re


PEST_RESPONSES = {
    "aphid": {
        "reply": "Hi! Based on symptoms, it appears to be Aphids. Apply Neem oil spray and introduce beneficial insects like ladybugs. Monitor the underside of leaves regularly.",
        "recs": [
            "Spray Neem oil (5ml/liter) every 7 days",
            "Introduce ladybugs or lacewings",
            "Remove heavily infested leaves",
            "Avoid excessive nitrogen fertilizer"
        ]
    },
    "whitefly": {
        "reply": "Symptoms suggest Whitefly infestation. Use yellow sticky traps and apply insecticidal soap or Neem-based spray. Keep humidity under control.",
        "recs": ["Yellow sticky traps", "Insecticidal soap spray", "Neem oil application", "Remove weeds around field"]
    },
    "blight": {
        "reply": "This looks like Early or Late Blight. Remove infected leaves immediately, improve air circulation, and apply copper-based fungicide if needed.",
        "recs": ["Remove infected plant parts", "Apply copper fungicide", "Avoid overhead irrigation", "Crop rotation next season"]
    },
    "powdery mildew": {
        "reply": "Powdery mildew detected. Improve air flow, reduce humidity, and apply sulfur or potassium bicarbonate spray.",
        "recs": ["Sulfur-based spray", "Increase spacing between plants", "Morning irrigation only", "Remove affected leaves"]
    },
    "tomato": {
        "reply": "For tomato plants, common issues include aphids, blight, or nutrient deficiency. Please share a clear photo of the affected leaves for accurate diagnosis. Meanwhile, ensure proper watering and balanced NPK.",
        "recs": ["Check underside of leaves for pests", "Maintain soil moisture 50-70%", "Balanced fertilizer (NPK 10-10-10)", "Support plants with stakes"]
    },
    "leaf": {
        "reply": "Leaf issues can be caused by pests, fungi, or nutrient imbalance. Please describe the color, spots, or any insects you see. I can guide you better with more details or a photo.",
        "recs": ["Inspect for insects", "Check soil pH (ideal 6.0-6.8)", "Ensure proper drainage", "Use organic mulch"]
    },
    "irrigation": {
        "reply": "Optimal irrigation depends on crop and soil moisture. Currently your field moisture is in optimal range (around 55-65%). Avoid overwatering to prevent root rot.",
        "recs": ["Irrigate early morning", "Use drip irrigation if possible", "Monitor soil moisture sensor", "Mulch to retain moisture"]
    },
    "fertilizer": {
        "reply": "For most crops, a balanced NPK is recommended. Based on your soil data, maintain NPK levels carefully. Organic compost is always a good base.",
        "recs": ["Apply compost or vermicompost", "Split nitrogen doses", "Test soil every season", "Avoid excess urea"]
    },
    "yield": {
        "reply": "Current predicted yield is looking good at ~6.8 tons/hectare. To improve further, focus on timely irrigation, pest management, and balanced nutrition.",
        "recs": ["Follow recommended sowing calendar", "Use certified seeds", "Integrated pest management", "Harvest at right maturity"]
    },
}

DEFAULT_REPLY = (
    "Hi! I'm KrishiMitra AI, your farming assistant. "
    "You can ask me about pests, diseases, irrigation, fertilizers, soil, weather, or crop yield. "
    "For best results, describe the problem clearly or upload a photo of the affected plant."
)

DEFAULT_RECS = [
    "Keep soil moisture in optimal range (50-70%)",
    "Monitor weather forecasts regularly",
    "Practice crop rotation",
    "Use organic methods whenever possible"
]


def get_ai_response(message: str) -> Tuple[str, List[str]]:
    msg = message.lower().strip()

    # Priority matching
    for keyword, data in PEST_RESPONSES.items():
        if keyword in msg:
            return data["reply"], data["recs"]

    # Greeting
    if any(w in msg for w in ["hello", "hi", "namaste", "hey"]):
        return (
            "Namaste! I'm KrishiMitra AI. How can I help your farm today? "
            "Ask about crop health, pests, soil, weather or yield predictions.",
            DEFAULT_RECS
        )

    if any(w in msg for w in ["thank", "thanks", "shukriya"]):
        return "You're welcome! Feel free to ask anytime. Happy farming! 🌾", []

    return DEFAULT_REPLY, DEFAULT_RECS
