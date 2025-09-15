import requests
from fastapi import FastAPI, HTTPException
from weather import realtime_weather
from pydantic import BaseModel
import uvicorn
from password_gen import random_password

app = FastAPI()

class PasswordRequest(BaseModel):
    length: int = 12

class PasswordResponse(BaseModel):
    password: str

@app.get("/weather/{city}")
async def get_weather(city: str):
    weather_data = realtime_weather(city)
    if "error" in weather_data:
        raise HTTPException(status_code=400, detail=weather_data["error"])
    return weather_data

@app.post("/generate-password", response_model=PasswordResponse)
async def generate_password(request: PasswordRequest):
    try:
        password = random_password(request.length)
        return PasswordResponse(password=password)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
