import os
import io
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from PIL import Image
from ultralytics import YOLO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
MODEL_PATH = os.getenv("MODEL_PATH", "/app/models/yolov8n.pt")
CONFIDENCE_THRESHOLD_DEFAULT = float(os.getenv("CONFIDENCE_THRESHOLD_DEFAULT", 0.25))
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/app/output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI(title="YOLOv8 Object Detection API")
model = None

@app.on_event("startup")
def load_model():
    global model
    logger.info(f"Loading model from {MODEL_PATH}")
    try:
        model = YOLO(MODEL_PATH)
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise e

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/detect")
async def detect_objects(
    image: UploadFile = File(...),
    confidence_threshold: float = Form(CONFIDENCE_THRESHOLD_DEFAULT)
):
    # Validate file type
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image")

    try:
        # Read image
        contents = await image.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {e}")

    # Run inference
    try:
        results = model(img, conf=confidence_threshold)
    except Exception as e:
        logger.error(f"Inference error: {e}")
        raise HTTPException(status_code=500, detail="Inference failed")

    # Parse results
    detections = []
    summary = {}
    if len(results) > 0 and results[0].boxes is not None:
        boxes = results[0].boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            detection = {
                "box": [x1, y1, x2, y2],
                "label": label,
                "score": conf
            }
            detections.append(detection)
            summary[label] = summary.get(label, 0) + 1

    # Save annotated image
    try:
        annotated = results[0].plot()  # returns BGR numpy array
        annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        img_annotated = Image.fromarray(annotated_rgb)
        output_path = os.path.join(OUTPUT_DIR, "last_annotated.jpg")
        img_annotated.save(output_path)
        logger.info(f"Annotated image saved to {output_path}")
    except Exception as e:
        logger.error(f"Failed to save annotated image: {e}")
        # Not critical, continue

    return {
        "detections": detections,
        "summary": summary
    }