# TODO

## 🚀 Project Setup
- [x] Create `requirements.txt` with dependencies (ultralytics, opencv-python, streamlit, etc.)
- [x] Set up project structure (src/, tests/, models/, config/)
- [x] Create `config.yaml` for hyperparameters
- [x] Add `.gitignore` for Python project
- [x] Initialize git repository
- [x] Create GitHub repository

## 🔧 Core Implementation
- [x] Implement `DetectionAgent` for YOLO inference (8 tests, 76% coverage)
- [x] Implement `TrackingAgent` for object tracking across frames (11 tests, 99% coverage)
- [x] Implement `ModelManagerAgent` for loading/switching YOLO models (12 tests, 90% coverage)
- [x] Implement `LabelAgent` for validating object names (22 tests, 98% coverage)
- [x] Implement `LoggingAgent` for logging and metrics (18 tests, 100% coverage)
- [x] Create main `app.py` for Streamlit application
- [x] Integrate all agents in working demo
- [x] Fix crash when removing all tracked objects
- [x] Add performance optimizations (IOU threshold, frame skip)

## 🧪 Testing & Quality
- [x] Write unit tests for detection (8 tests)
- [x] Write unit tests for tracking (11 tests)
- [x] Write unit tests for model manager (12 tests)
- [x] Set up linting (ruff)
- [x] Set up formatting (black, isort)
- [x] Achieve 91% code coverage

## 📝 Documentation
- [x] Write README.md with setup instructions
- [ ] Document API/module interfaces
- [ ] Add usage examples
