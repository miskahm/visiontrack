# VisionTrack - Real-time Object Detection & Tracking System

A production-ready computer vision system for real-time object detection and multi-object tracking, built with YOLOv8 and Streamlit. This project demonstrates clean architecture, comprehensive testing, and modern ML engineering practices.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Tests](https://img.shields.io/badge/tests-71%20passed-brightgreen.svg)
![Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎯 Key Features

- **Real-time Object Detection**: YOLOv8-powered detection with adjustable confidence thresholds
- **Multi-Object Tracking**: Persistent object tracking across frames with unique IDs
- **Multiple Input Sources**: Support for webcam streams, video files, and static images
- **Interactive Web UI**: Clean Streamlit interface with real-time parameter adjustment
- **Performance Optimization**: Frame skipping, model caching, and IOU threshold tuning
- **Comprehensive Testing**: 71 tests with 94% code coverage
- **Modular Architecture**: Five specialized agents for separation of concerns
- **Production-Ready**: Type hints, error handling, logging, and configuration management

## 🚀 Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd yolodemo

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The application will launch in your default browser at `http://localhost:8501`.

## 📋 Technology Stack

### Core Technologies
- **Python 3.10+**: Modern Python with full type hint support
- **YOLOv8 (Ultralytics)**: State-of-the-art object detection
- **OpenCV**: Computer vision and video processing
- **Streamlit**: Interactive web interface
- **PyYAML**: Configuration management

### Development & Testing
- **pytest**: Testing framework with 71 comprehensive tests
- **pytest-cov**: Code coverage analysis (94% coverage)
- **ruff**: Fast Python linter
- **black & isort**: Code formatting

## 🏗️ Architecture Overview

VisionTrack follows a clean, modular architecture with five specialized agent modules:

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit UI (app.py)                │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Detection  │    │   Tracking   │    │    Label     │
│    Agent     │───▶│    Agent     │    │    Agent     │
│  (YOLO)      │    │  (Multi-Obj) │    │ (Validation) │
└──────────────┘    └──────────────┘    └──────────────┘
        │                                       
        ▼                                       
┌──────────────┐    ┌──────────────┐           
│ Model Manager│    │   Logging    │           
│    Agent     │    │    Agent     │           
│  (Caching)   │    │  (Metrics)   │           
└──────────────┘    └──────────────┘           
```

### Agent Modules

| Agent | Responsibility | Test Coverage |
|-------|---------------|---------------|
| **DetectionAgent** | YOLO inference, confidence filtering | 76% |
| **TrackingAgent** | Multi-object tracking with IOU matching | 99% |
| **LabelAgent** | Class name validation and filtering | 98% |
| **LoggingAgent** | Event logging and metrics collection | 100% |
| **ModelManagerAgent** | Model loading, caching, configuration | 90% |

## 📁 Project Structure

```
yolodemo/
├── src/                          # Source code modules
│   ├── detection_agent.py        # YOLO object detection
│   ├── tracking_agent.py         # Multi-object tracking logic
│   ├── label_agent.py            # Class filtering and validation
│   ├── logging_agent.py          # Logging and metrics
│   └── model_manager_agent.py    # Model loading and config
├── tests/                        # Comprehensive test suite
│   ├── test_detection_agent.py   # Detection unit tests
│   ├── test_tracking_agent.py    # Tracking unit tests
│   ├── test_label_agent.py       # Label validation tests
│   ├── test_logging_agent.py     # Logging tests
│   └── test_model_manager_agent.py # Model manager tests
├── models/                       # YOLO model weights directory
├── app.py                        # Streamlit web application
├── config.yaml                   # Application configuration
├── requirements.txt              # Python dependencies
├── agents.md                     # AI agent guidelines
└── README.md                     # This file
```

## 💻 Usage

### Web Interface

1. **Launch the app**: `streamlit run app.py`
2. **Select Input Source**: Choose from Webcam, Video File, or Image
3. **Configure Detection**:
   - Select object classes to track (person, car, dog, etc.)
   - Adjust confidence threshold (0.1-1.0)
   - Tune IOU threshold for tracking accuracy (0.1-0.9)
   - Enable/disable frame skipping for performance
4. **Start Processing**: Click "Start Webcam" or upload a file
5. **Real-time Adjustment**: All parameters can be changed during processing

### Configuration

Edit `config.yaml` to customize default settings:

```yaml
model:
  name: "yolov8n.pt"              # Model size (n/s/m/l/x)
  confidence_threshold: 0.5       # Detection confidence
  
tracking:
  iou_threshold: 0.3              # Tracking IOU threshold
  max_age: 30                     # Max frames before track deletion
  min_hits: 3                     # Min detections before track creation
  
ui:
  theme: "light"                  # UI theme
  show_confidence: true           # Display confidence scores
```

## 🧪 Testing

VisionTrack includes comprehensive test coverage for all agent modules:

```bash
# Run all tests
pytest tests/ -v

# Run tests with coverage report
pytest tests/ --cov=src --cov-report=term-missing

# Run specific test module
pytest tests/test_detection_agent.py -v

# Run single test
pytest tests/test_tracking_agent.py::test_track_persistence -v
```

### Test Statistics
- **Total Tests**: 71
- **Code Coverage**: 94%
- **Test Types**: Unit tests, integration tests, edge case handling

## 🎨 Performance Features

### Optimization Techniques
- **Model Caching**: YOLO model loaded once and cached in Streamlit session
- **Frame Skipping**: Process every Nth frame for performance boost
- **IOU Threshold Tuning**: Adjustable tracking accuracy vs. speed tradeoff
- **Buffer Management**: Minimal webcam buffer for reduced latency
- **Real-time Parameter Adjustment**: No restart required for configuration changes

### Performance Tips
- **Low FPS?** Increase frame skip to 1-2
- **Missing objects?** Reduce IOU threshold to 0.2-0.25
- **False positives?** Increase confidence threshold to 0.6-0.7
- **First load slow?** Normal - model is cached for subsequent runs

## 📸 Screenshots & Demo

### Main Interface
<img width="1797" height="1102" alt="image" src="https://github.com/user-attachments/assets/2c003df5-eb7f-4997-ac2e-37bd72afbe8d" />


### Detection Results
![Detection Results Placeholder]
*Coming soon: Sample detection results with bounding boxes*

### Real-time Tracking
![Real-time Tracking Placeholder]
*Coming soon: Multi-object tracking demonstration*

## 🎓 Portfolio Context

This project was built to demonstrate:

### Software Engineering Practices
- **Clean Architecture**: Modular design with single-responsibility agents
- **Type Safety**: Full type hints for all functions and methods
- **Error Handling**: Comprehensive exception handling with informative messages
- **Code Quality**: Consistent style enforced by ruff, black, and isort
- **Documentation**: Clear docstrings, README, and inline documentation

### ML Engineering Practices
- **Model Management**: Efficient loading, caching, and configuration
- **Real-time Inference**: Optimized pipeline for video stream processing
- **Performance Tuning**: Frame skipping, threshold optimization, buffer management
- **Metrics Tracking**: FPS monitoring, detection counts, track persistence

### Testing & Quality Assurance
- **High Coverage**: 94% code coverage across all modules
- **Comprehensive Tests**: 71 tests covering unit, integration, and edge cases
- **CI/CD Ready**: pytest-based test suite for automated testing
- **Quality Gates**: Linting and formatting checks

### Production Readiness
- **Configuration Management**: YAML-based configuration system
- **Logging & Monitoring**: Structured logging with metrics collection
- **Error Recovery**: Graceful handling of camera failures, file errors
- **User Experience**: Real-time feedback, performance metrics, intuitive UI

## 🔮 Future Improvements

### Planned Features
- [ ] Export tracking results to JSON/CSV
- [ ] Custom YOLO model training interface
- [ ] Multi-camera support for simultaneous streams
- [ ] Detection zone configuration (ignore regions)
- [ ] Advanced analytics dashboard (heatmaps, trajectory plots)
- [ ] REST API for programmatic access
- [ ] Docker containerization
- [ ] Cloud deployment (AWS/GCP/Azure)

### Performance Enhancements
- [ ] GPU acceleration support (CUDA)
- [ ] TensorRT optimization for inference
- [ ] Batch processing for video files
- [ ] Parallel processing for multiple streams

### ML Improvements
- [ ] Support for YOLOv9, YOLOv10, and other models
- [ ] Custom class training workflow
- [ ] Model quantization for edge deployment
- [ ] Ensemble model support

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for new functionality
4. Ensure all tests pass (`pytest tests/`)
5. Run linting (`ruff check .`) and formatting (`black . && isort .`)
6. Commit changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📝 Development Guidelines

See [agents.md](agents.md) for detailed development guidelines, including:
- Build and run commands
- Code style requirements
- Testing requirements
- Available AI subagents for development assistance

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Ultralytics**: YOLOv8 object detection framework
- **Streamlit**: Interactive web application framework
- **OpenCV**: Computer vision library
- **pytest**: Testing framework

## 📧 Contact

For questions, feedback, or collaboration opportunities, please open an issue or reach out via the repository contact methods.

---

**Built with ❤️ to demonstrate production-ready ML engineering practices**
