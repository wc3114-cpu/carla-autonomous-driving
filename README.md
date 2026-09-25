# CARLA Autonomous Driving Project

Four-week autonomous driving simulation project based on CARLA 0.9.15.

## Week 1

Completed:

- WSL2 and Ubuntu 22.04 development environment
- Python 3.10 virtual environment
- CARLA 0.9.15 simulator setup
- CARLA Python API connection
- Official `generate_traffic.py` example
- Official `manual_control.py` example
- RGB camera configuration
- 1000-frame simulation dataset collection
- YOLO annotation generation
- KITTI-style annotation generation
- Annotation visualization and inspection

## Environment

- Windows 11
- WSL2
- Ubuntu 22.04.5 LTS
- Python 3.10
- CARLA 0.9.15
- NVIDIA GPU

## Main Scripts

- `01_spawn_vehicle.py` — vehicle spawning and autopilot
- `02_rgb_camera.py` — RGB camera test
- `03_collect_1000.py` — 1000-frame dataset collection
- `check_labels.py` — annotation visualization

## Week 1 Dataset

- 1000 RGB images
- 1000 YOLO annotation files
- 1000 KITTI-style annotation files
- 660 frames with vehicle annotations
- 340 negative frames without vehicle annotations

## Next Step

Week 2 will focus on YOLOv8 object detection and semantic segmentation.

---

## Week 1 Deliverables

- [开发环境搭建文档](docs/week1_environment_setup.md)
- [智能驾驶技术分析笔记](docs/intelligent_driving_notes.md)
- [第一周实验报告](reports/week1_report.md)
- [CARLA 30 秒演示视频](media/week1_carla_demo.mp4)

### Screenshots

- [CARLA Simulator](media/screenshots/01_carla_simulator.png)
- [Official generate_traffic.py Example](media/screenshots/02_generate_traffic.png)
- [Official manual_control.py Example](media/screenshots/03_manual_control.png)
- [CARLA Python API Connection](media/screenshots/04_python_connection.png)
