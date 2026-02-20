# YOLOv8 Object Detection API & Web Application

This project implements a production-ready object detection service that allows users to upload images and detect objects using the state-of-the-art YOLOv8 model. The system consists of two main components:

- **Backend API**: FastAPI service that loads a pre-trained YOLOv8 model and exposes detection endpoints
- **Frontend UI**: Streamlit web application that provides an intuitive interface for users to upload images and view results

##  Features

- **Real-time Object Detection**: Powered by YOLOv8n (lightweight model)
- **RESTful API**: FastAPI backend with automatic Swagger documentation
- **Interactive Web UI**: User-friendly Streamlit interface
- **Confidence Threshold Control**: Adjust detection sensitivity in real-time
- **Class Summary**: Get count of detected objects per class
- **Annotated Images**: Save images with bounding boxes and labels
- **Docker Containerization**: Easy deployment with Docker Compose
- **Health Checks**: Automatic service monitoring
- **Environment Configuration**: Flexible setup via environment variables

## Architecture

```
┌─────────┐     ┌──────────┐     ┌──────────┐
│ Streamlit│────▶│  FastAPI │────▶│  YOLOv8  │
│    UI    │◀────│ Backend  │◀────│  Model   │
└─────────┘     └──────────┘     └──────────┘
     │                │                │
     ▼                ▼                ▼
  User            Detection        Object
Interface          Logic          Detection
```

## Quick Start

### Prerequisites

- Docker and Docker Compose installed on your system
- Git (optional, for cloning)

### Installation

1. **Clone or download the project**
   ```bash
   git clone <your-repository-url>
   cd web-app-with-yolov8
   ```

2. **Create environment configuration**
   ```bash
   cp .env.example .env
   ```

3. **Build and start the containers**
   ```bash
   docker-compose up --build -d
   ```

4. **Access the applications**
   - **Web UI**: http://localhost:8501
   - **API Documentation**: http://localhost:8000/docs
   - **API Health Check**: http://localhost:8000/health

5. **Stop the services**
   ```bash
   docker-compose down
   ```

## Usage Guide

### Using the Web Interface

1. Open http://localhost:8501 in your browser
2. Upload an image (JPG, JPEG, or PNG)
3. Adjust the confidence threshold using the slider
4. Click "Detect Objects"
5. View results including:
   - Detection summary by class
   - Individual detection details with confidence scores
   - Bounding box coordinates

### Using the API Directly

**Health Check**
```bash
curl http://localhost:8000/health
```

**Object Detection**
```bash
curl -X POST "http://localhost:8000/detect" \
  -H "accept: application/json" \
  -F "image=@/path/to/your/image.jpg" \
  -F "confidence_threshold=0.25"
```

**Example Response**
```json
{
  "detections": [
    {
      "box": [150.5, 200.3, 350.8, 450.2],
      "label": "person",
      "score": 0.92
    },
    {
      "box": [300.1, 150.7, 450.3, 250.9],
      "label": "car",
      "score": 0.88
    }
  ],
  "summary": {
    "person": 1,
    "car": 1
  }
}
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_PORT` | Port for the FastAPI backend | 8000 |
| `UI_PORT` | Port for the Streamlit frontend | 8501 |
| `MODEL_PATH` | Path to YOLO model inside container | /app/models/yolov8n.pt |
| `CONFIDENCE_THRESHOLD_DEFAULT` | Default confidence threshold | 0.25 |

### Project Structure

```
├── api/
│   ├── Dockerfile           # API container configuration
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Python dependencies for API
├── ui/
│   ├── Dockerfile           # UI container configuration
│   ├── app.py               # Streamlit application
│   └── requirements.txt     # Python dependencies for UI
├── scripts/
│   └── download_model.sh    # Model download script
├── models/                  # Directory for YOLO model (created on first run)
├── output/                  # Directory for annotated images
├── docker-compose.yml       # Docker services orchestration
├── .env.example             # Environment variables template
└── README.md                # Project documentation
```

## 🔧 Development

### Running Without Docker

**Backend API**
```bash
cd api
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

**Frontend UI**
```bash
cd ui
pip install -r requirements.txt
streamlit run app.py --server.port=8501
```

### Adding New Features

1. **Model Customization**: Update `MODEL_URL` in `scripts/download_model.sh` to use different YOLO versions
2. **API Endpoints**: Add new routes in `api/main.py`
3. **UI Enhancements**: Modify `ui/app.py` for frontend changes

## 🐛 Troubleshooting

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Docker build fails | Run `docker system prune -a` and rebuild |
| Model not downloading | Check internet connection or manually download model |
| API health check failing | Verify model exists at specified path in container |
| UI cannot connect to API | Ensure `API_URL` in `.env` is correct |
| Out of memory | Reduce model size or increase Docker memory limit |

### Viewing Logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs api
docker-compose logs ui

# Follow logs in real-time
docker-compose logs -f
```