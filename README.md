# KrishiMitra AI – Smart Crop Yield Predictor

A full-stack AI-powered agricultural dashboard for crop yield prediction, soil moisture analysis, weather integration, and intelligent farming recommendations.

![KrishiMitra AI Dashboard](docs/screenshot.png)

## Features

- **Crop Yield Predictions** – Interactive Predicted vs Historical charts for Maize, Wheat, Rice
- **Soil Moisture Analysis** – Real-time moisture %, pH, NPK status with visual map hotspots
- **Field Management** – Field status (Optimal / Warning / Critical) and yield trends
- **AI Farming Recommendations** – Chat-based assistant (rule-based, easily replaceable with LLM)
- **Weather Integration** – Current conditions + 5-day forecast + alerts (Karnal, India demo)
- **Authentication** – JWT-based login/register
- **MySQL Database** – Persistent storage for users, fields, yields, soil, weather, chat history

## Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Frontend  | HTML5 + Tailwind CSS + Chart.js     |
| Backend   | Python 3.12 + FastAPI + SQLAlchemy  |
| Database  | MySQL 8                             |
| Auth      | JWT (python-jose) + bcrypt          |

## Project Structure

```
krishimitra-ai/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry + seed data
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/models.py
│   │   ├── schemas/schemas.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   └── dashboard.py
│   │   └── services/
│   │       ├── auth.py
│   │       └── ai_service.py    # Rule-based AI (swap with OpenAI/Gemini)
│   └── requirements.txt
├── web/
│   └── index.html               # Complete dashboard UI (matches design)
├── docs/
└── README.md
```

## Quick Start

### 1. Prerequisites

- Python 3.10+
- MySQL 8 running locally
- Modern browser

### 2. Database Setup

```bash
mysql -u root -p
```

```sql
CREATE DATABASE krishimitra;
CREATE USER 'krishi'@'localhost' IDENTIFIED BY 'krishi123';
GRANT ALL PRIVILEGES ON krishimitra.* TO 'krishi'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Backend

```bash
cd backend
pip install -r requirements.txt

# Optional: create .env
# DATABASE_URL=mysql+pymysql://krishi:krishi123@localhost:3306/krishimitra

# Run
PYTHONPATH=. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: http://localhost:8000/docs

**Demo credentials (auto-seeded on first run):**
- Email: `rahul@krishimitra.ai`
- Password: `rahul123`

### 4. Frontend

Simply open `web/index.html` in a browser **or** serve it:

```bash
cd web
python -m http.server 3000
# Open http://localhost:3000
```

> The frontend talks to `http://localhost:8000`. Change `API_BASE` in `index.html` if needed.

## API Endpoints

| Method | Endpoint              | Description                |
|--------|-----------------------|----------------------------|
| POST   | /api/auth/register    | Register new farmer        |
| POST   | /api/auth/login-json  | Login (JSON)               |
| GET    | /api/auth/me          | Current user               |
| GET    | /api/dashboard        | Full dashboard payload     |
| POST   | /api/chat             | AI farming chat            |
| GET    | /api/chat/history     | Chat history               |
| GET    | /api/fields           | List fields                |
| GET    | /api/soil/{field_id}  | Soil data                  |
| GET    | /api/weather          | Weather data               |

## AI Recommendations

The chat assistant currently uses a lightweight rule-based engine (`ai_service.py`) that handles:

- Aphids / Whitefly / Blight / Powdery mildew
- Tomato leaf issues
- Irrigation & fertilizer advice
- Yield improvement tips

You can easily replace `get_ai_response()` with OpenAI, Google Gemini, or any local LLM.

## Environment Variables

```env
DATABASE_URL=mysql+pymysql://krishi:krishi123@localhost:3306/krishimitra
SECRET_KEY=your-secret-key-change-in-production
```

## License

MIT – Built for farmers with ❤️
```
