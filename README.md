# VisionTrack - YOLO Object Tracking

Real-time object detection and tracking using Ultralytics YOLO models.

## Features

- Real-time object detection with YOLOv8/v10
- Multi-object tracking across video frames
- Simple text-based object selection interface
- Streamlit web interface

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Project Structure

```
yolodemo/
├── src/              # Source code
├── tests/            # Test files
├── models/           # YOLO model weights
├── config.yaml       # Configuration
└── app.py           # Main application
```

## Documentation

See [AGENTS.md](AGENTS.md) for development guidelines.
