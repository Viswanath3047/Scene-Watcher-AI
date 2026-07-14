from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cv2

from routes.stream import router as stream_router, latest_data
from database.db import init_db, get_alerts, get_analytics, get_chart_data, register_user, login_user

app = FastAPI(title="Scene Watcher AI")
init_db()

# Register the video streaming router
app.include_router(stream_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Scene Watcher AI Backend Running"}


@app.get("/health")
def health():
    return {"status": "OK", "AI": "Ready"}


@app.get("/detect")
def detect():
    return latest_data

@app.get("/analytics")
def analytics():
    return get_analytics()


@app.get("/history")
def history():

    rows = get_alerts()

    history = []

    for row in rows:
        history.append({
            "id": row[0],
            "object": row[1],
            "confidence": row[2],
            "status": row[3],
            "time": row[4]
        })

    return history

@app.get("/charts")
def charts():
    return get_chart_data()

@app.post("/register")
def register(data: dict):

    try:

        register_user(
            data["fullname"],
            data["username"],
            data["email"],
            data["password"]
        )

        return {
            "success": True,
            "message": "Registration Successful"
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@app.post("/login")
def login(data: dict):

    user = login_user(
        data["email"],
        data["password"]
    )

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return {
        "success": True,
        "user": {
            "id": user[0],
            "fullname": user[1],
            "username": user[2],
            "email": user[3]
        }
    }