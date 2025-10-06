# AGENTS.md VisionTrack (YOLO Object Tracking)

## Project Guidelines for AI Agents

### Build/Run Commands
- **Install**: `pip install -r requirements.txt`
- **Run app**: `python main.py` or `streamlit run app.py`
- **Tests**: `pytest tests/` (single test: `pytest tests/test_detection.py::test_yolo_inference`)
- **Lint**: `ruff check .` or `pylint src/`
- **Format**: `black . && isort .`

### Code Style
- **Python 3.10+**, type hints required for all functions
- **Imports**: stdlib → third-party → local (grouped, sorted via `isort`)
- **Naming**: `snake_case` for functions/vars, `PascalCase` for classes
- **No comments** unless complex logic requires explanation
- **Error handling**: Use specific exceptions, log errors with context
- **YOLO models**: Use `ultralytics` library, store weights in `models/`
- **Config**: Store hyperparameters in `config.yaml`, never hardcode paths

### Notes
- Keep `todo.md` and `communications.md` updated with progress
- Use `gh` CLI for GitHub operations
- **Current Status**: 5 core agents implemented (71 tests, 94% coverage)
- **App Status**: Full Streamlit app with performance optimizations (IOU threshold, frame skip)

---

## Available Subagents

Invoke subagents by mentioning them with `@agent-name` in your messages. Each subagent has specialized expertise.

### Core Development
- **@python-pro** (sonnet) - Modern Python 3.12+ development, async patterns, FastAPI, type hints, modern tooling (uv, ruff)
- **@ml-engineer** (sonnet) - Production ML systems, PyTorch 2.x, model serving, feature engineering, A/B testing, monitoring

### Quality & Testing
- **@code-reviewer** (sonnet) - AI-powered code review, security scanning, OWASP compliance, performance analysis
- **@test-automator** (sonnet) - Test automation with pytest, TDD orchestration, AI-powered testing, CI/CD integration
- **@performance-engineer** (sonnet) - Performance optimization, OpenTelemetry, distributed tracing, caching strategies, Core Web Vitals

### UI/UX & Design
- **@ui-ux-designer** (sonnet) - Interface design, wireframes, design systems, accessibility standards, user research
- **@ui-visual-validator** (sonnet) - Visual regression testing, design system compliance, accessibility verification, UI validation

### Documentation
- **@api-documenter** (sonnet) - OpenAPI specs, interactive docs, SDK generation, developer portals
- **@docs-architect** (sonnet) - Comprehensive technical documentation, architecture guides, long-form manuals

### Usage Examples
```
@python-pro implement the DetectionAgent with async YOLO inference
@ml-engineer optimize the tracking algorithm for real-time performance
@code-reviewer analyze the detection module for security and performance issues
@test-automator create comprehensive tests for the tracking system
@performance-engineer profile and optimize the video processing pipeline
@ui-ux-designer design the object tracking visualization interface
@ui-visual-validator verify the detection overlay rendering is correct
@api-documenter create OpenAPI spec for the REST API endpoints
@docs-architect generate complete system architecture documentation
```
