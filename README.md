# VisionTrack - YOLO Object Tracking

Real-time object detection and tracking using Ultralytics YOLO models.

## Features

- ✅ Real-time object detection with YOLOv8/v10
- ✅ Multi-object tracking with persistent IDs
- ✅ Interactive object class selection
- ✅ Support for Webcam, Video Files, and Images
- ✅ Real-time FPS and statistics display
- ✅ **On-the-fly parameter adjustment** (no restart needed!)
- ✅ Adjustable confidence threshold
- ✅ Configurable IOU threshold for tracking accuracy
- ✅ Frame skip option for performance optimization
- ✅ Fast webcam startup with caching
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
3. **Adjust Settings** (can be changed in real-time!): 
   - **Confidence Threshold**: Minimum confidence for detections (0.1-1.0)
   - **IOU Threshold**: Intersection over Union for tracking (0.1-0.9)
   - **Frame Skip**: Skip frames to improve performance (0-5)
4. **Start Tracking**: Click "▶️ Start Webcam" or upload a file
5. **Adjust parameters while running** - changes apply immediately!

### Performance Tips

- **Low FPS?** Try increasing **Frame Skip** to 1 or 2
- **Missing tracks?** Reduce **IOU Threshold** to 0.2-0.25
- **Too many false positives?** Increase **Confidence Threshold** to 0.6-0.7
- **Parameters can be adjusted in real-time** - no need to stop/restart!
- **First load is slow?** Model is cached after first load, subsequent runs are fast

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
