from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from pymongo import MongoClient
import datetime

app = FastAPI()

# Load Scam Detection Model (Simple text classification)
scam_detector = pipeline("text-classification", model="facebook/bart-large-mnli")

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["scam_db"]
collection = db["scam_reports"]

# Request model
class ScamCheckRequest(BaseModel):
    message: str
    user_id: str

@app.post("/check_scam")
def check_scam(request: ScamCheckRequest):
    result = scam_detector(request.message)
    label = result[0]['label']
    score = result[0]['score']

    scam_detected = label.lower() in ["scam", "fraud", "phishing"]

    if scam_detected:
        # Store in DB
        collection.insert_one({
            "user_id": request.user_id,
            "message": request.message,
            "detected_scam": scam_detected,
            "timestamp": datetime.datetime.now()
        })
        return {"alert": "⚠️ This message might be a scam!", "confidence": score, "scam_detected": scam_detected}

    return {"alert": "✅ No scam detected.", "confidence": score, "scam_detected": scam_detected}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
