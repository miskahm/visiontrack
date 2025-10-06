# VisionTrack - YOLO Object Tracking

Real-time object detection and tracking using Ultralytics YOLO models.

## Features

- ✅ Real-time object detection with YOLOv8/v10
- ✅ Multi-object tracking with persistent IDs
- ✅ Interactive object class selection
- ✅ Support for Webcam, Video Files, and Images
- ✅ Real-time FPS and statistics display
- ✅ Adjustable confidence threshold
- ✅ Clean Streamlit web interface

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Select Input Source**: Choose between Webcam, Video File, or Image
2. **Select Objects**: Pick which object classes to track (person, car, etc.)
3. **Adjust Settings**: Set confidence threshold and visualization options
4. **Start Tracking**: Click "Start Webcam" or upload a file

## Project Architecture

```
yolodemo/
├── src/
│   ├── detection_agent.py      # YOLO inference (76% coverage)
│   ├── tracking_agent.py        # Multi-object tracking (99% coverage)
│   ├── model_manager_agent.py   # Model loading (90% coverage)
│   ├── label_agent.py           # Class validation (98% coverage)
│   └── logging_agent.py         # Logging & metrics (100% coverage)
├── tests/                       # 71 tests, 94% coverage
├── models/                      # YOLO model weights
├── config.yaml                  # Configuration
└── app.py                       # Streamlit application
```

## Configuration

Edit `config.yaml` to customize:
- Model selection (YOLOv8n/s/m/l/x)
- Confidence thresholds
- Tracking parameters (IOU, max age, min hits)
- UI settings

## Development

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Lint code
ruff check .

# Format code
black . && isort .
```

## Testing

- **71 tests** with **94% code coverage**
- All agents have comprehensive unit tests
- See [AGENTS.md](AGENTS.md) for development guidelines

## License

MIT License
