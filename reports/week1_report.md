# 第一周实验报告

## 1. 本周目标

本周主要目标是完成 CARLA 自动驾驶项目的基础环境搭建，并熟悉 CARLA 仿真平台的基本使用方法。

主要任务包括：

- 配置 WSL2 和 Ubuntu 22.04
- 配置 Python 3.10 开发环境
- 安装 CARLA 0.9.15
- 配置 CARLA Python API
- 运行 CARLA 官方示例
- 熟悉车辆控制和交通流生成
- 初步完成 RGB Camera 数据采集
- 建立 GitHub 项目仓库

## 2. 开发环境搭建

本周首先完成了 WSL2 和 Ubuntu 22.04.5 LTS 的安装与配置。

Python 版本为：

Python 3.10.12

同时创建了独立的 Python 虚拟环境，用于安装 CARLA 项目相关依赖。

在 Ubuntu 中成功使用 `nvidia-smi` 识别 NVIDIA GPU。

最开始尝试直接在 WSL2 中运行 CARLA Linux Server，但测试发现 Vulkan 使用 llvmpipe 软件渲染，CARLA 无法正常启动。

因此最终采用：

Windows 运行 CARLA Simulator Server，Ubuntu / WSL2 运行 Python Client。

通过这种方式成功完成 CARLA Server 与 Ubuntu Python 环境之间的连接。

## 3. CARLA 官方示例

为了熟悉 CARLA 的基本操作，本周运行了两个官方示例。

### generate_traffic.py

运行官方交通流生成程序：

`generate_traffic.py`

成功生成：

- 20 辆车辆
- 5 个行人

通过该程序了解了 CARLA 中 NPC 车辆和行人的生成方法。

### manual_control.py

运行官方手动驾驶程序：

`manual_control.py`

成功进入车辆驾驶界面，并通过键盘完成车辆加速、刹车、转向以及 Autopilot 的切换。

通过这个示例对 CARLA 的车辆操作和仿真场景有了更直观的认识。

## 4. RGB Camera 与数据采集

在熟悉 CARLA 基础操作后，通过 CARLA Python API 给车辆添加了 RGB Camera。

相机主要参数为：

- 图像分辨率：800 × 600
- FOV：90°
- 传感器类型：RGB Camera

首先进行了 100 张图像的小规模采集测试，确认相机和图像保存流程能够正常工作。

之后进一步进行了 1000 帧道路图像采集，并同步生成车辆目标的 YOLO 和 KITTI-style 标注。

最终获得：

- 1000 张 RGB 图像
- 1000 个 YOLO 标注文件
- 1000 个 KITTI-style 标注文件

其中：

- 660 帧包含车辆目标
- 340 帧为无车辆目标的负样本

## 5. 标注结果检查

为了检查自动生成的标注是否正常，编写了标注可视化程序，将 YOLO Bounding Box 重新绘制到原始 RGB 图像中。

抽样检查发现，大部分近距离车辆的标注效果较好。

同时也发现部分距离较远或者遮挡较严重的车辆存在 Bounding Box 不够准确的问题。

因此后续正式训练目标检测模型之前，还需要进一步进行数据清洗和标注质量检查。

## 6. GitHub 项目管理

本周建立了 GitHub 项目仓库：

`carla-autonomous-driving`

并上传了主要 Python 程序、README、标注检查结果以及项目说明。

由于原始图像和标注数据文件数量较多，因此通过 `.gitignore` 排除了大规模数据集，只在仓库中保留代码和部分结果示例。

## 7. 本周遇到的问题

本周最主要的问题是 CARLA Linux Server 无法直接在当前 WSL2 环境中运行。

虽然 WSL2 能够识别 NVIDIA GPU，但 Vulkan 最终使用的是 llvmpipe 软件渲染。

经过检查和尝试后，最终采用 Windows CARLA Server + Ubuntu Python Client 的方式解决。

另外，在自动生成车辆 Bounding Box 时，也发现了部分远距离车辆标注不准确的问题。

这些问题也让我对 CARLA 的运行结构、GPU 图形环境以及自动标注过程有了更具体的理解。

## 8. 本周完成情况

本周已经完成：

- WSL2 + Ubuntu 22.04 环境搭建
- Python 3.10 虚拟环境配置
- CARLA 0.9.15 安装
- CARLA Python API 安装
- Windows CARLA Server 与 Ubuntu Python Client 连接
- CARLA 官方 traffic 示例
- CARLA 官方 manual control 示例
- RGB Camera 配置
- 1000 帧仿真数据采集
- YOLO / KITTI-style 标注生成
- 标注结果检查
- GitHub 仓库建立

整体来看，本周已经跑通了从 CARLA 仿真环境到 Python 数据采集的基础流程。

## 9. 下一周计划

下一周主要进入视觉感知部分。

计划内容包括：

- 学习 YOLOv8 基础结构和使用方法
- 整理第一周采集的数据
- 检查和清洗车辆标注
- 使用 YOLOv8 进行目标检测实验
- 学习语义分割基本概念
- 尝试进行道路或可行驶区域分割

下一阶段的重点是从“能够采集数据”进一步进入“能够利用数据进行视觉感知”。
