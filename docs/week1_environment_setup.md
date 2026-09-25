# CARLA 开发环境搭建文档

## 1. 环境配置

本项目使用 CARLA 0.9.15 作为自动驾驶仿真平台。

最终开发环境如下：

- 主机系统：Windows 11
- Linux 环境：WSL2
- Ubuntu：22.04.5 LTS
- Python：3.10.12
- CARLA：0.9.15
- GPU：NVIDIA GeForce RTX 3070 Ti Laptop GPU

## 2. WSL2 配置

首先在 Windows 的“启用或关闭 Windows 功能”中开启：

- Windows Subsystem for Linux
- Virtual Machine Platform

重启电脑后，在管理员 PowerShell 中执行：

wsl --set-default-version 2

之后使用：

wsl -l -v

检查 Ubuntu 是否运行在 WSL2 下。

检查结果显示 Ubuntu-22.04 的 VERSION 为 2，说明 WSL2 配置成功。

## 3. Ubuntu 22.04 安装

由于 Microsoft Store 下载 Ubuntu 时出现网络问题，最后使用 Ubuntu 22.04 的 WSL 镜像手动导入。

Ubuntu 安装完成后创建个人 Linux 用户：

weiqiao

并配置 sudo 权限。

使用：

lsb_release -a

检查系统版本，结果为：

Ubuntu 22.04.5 LTS

## 4. Python 开发环境

使用以下命令检查 Python 版本：

python3 --version

结果为：

Python 3.10.12

之后创建项目目录：

mkdir -p ~/carla_project
cd ~/carla_project

创建 Python 虚拟环境：

python3 -m venv .venv

激活虚拟环境：

source .venv/bin/activate

激活后，项目相关的 Python 包都会安装在虚拟环境中，避免和系统 Python 产生冲突。

## 5. 基础开发工具安装

安装 Git、pip、venv、curl、wget 等基础工具：

sudo apt install -y git python3-pip python3-venv curl wget unzip

使用以下命令检查 Git：

git --version

使用以下命令检查 pip：

pip3 --version

确认 Git 和 pip 均能正常使用。

## 6. GPU 环境检查

在 Ubuntu 中运行：

nvidia-smi

系统能够正常识别 NVIDIA GeForce RTX 3070 Ti Laptop GPU，说明 WSL2 可以访问 NVIDIA GPU。

之后使用：

MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA glxinfo -B

进一步检查图形加速环境。

测试结果显示 OpenGL 可以正常识别 NVIDIA GPU。

## 7. CARLA Python API 安装

在 Python 虚拟环境中安装 CARLA 0.9.15 Python API：

pip install pygame numpy carla==0.9.15

之后通过以下命令检查：

python -c "import carla; print('CARLA Python API imported successfully')"

成功输出：

CARLA Python API imported successfully

说明 CARLA Python API 安装完成。

## 8. CARLA Simulator 安装与启动

最开始尝试直接在 Ubuntu / WSL2 中运行 CARLA Linux 版本。

测试过程中发现，虽然 WSL2 可以正常识别 NVIDIA GPU，但 Vulkan 仍然使用 llvmpipe 软件渲染，导致 CARLA Linux Server 无法正常启动。

因此最终采用以下开发结构：

Windows：运行 CARLA Simulator Server  
Ubuntu / WSL2：运行 Python 开发环境和 CARLA Python API

Windows 版 CARLA 0.9.15 解压目录为：

C:\CARLA_Windows\CARLA_0.9.15\WindowsNoEditor

在 PowerShell 中进入该目录：

cd C:\CARLA_Windows\CARLA_0.9.15\WindowsNoEditor

启动 CARLA：

.\CarlaUE4.exe -quality-level=Low

成功打开 CARLA 城市道路仿真场景，说明 CARLA Simulator Server 可以正常运行。

## 9. Ubuntu Python 连接 CARLA Server

由于 CARLA Server 运行在 Windows，而 Python 开发环境运行在 Ubuntu / WSL2，因此需要获取 Windows 主机在 WSL2 中的地址。

使用：

ip route | grep default

获取 Windows 主机 IP。

本次环境中使用的地址为：

172.24.208.1

之后通过 CARLA Python API 连接 Windows 中运行的 CARLA Server。

连接成功后能够读取：

CARLA Server Version: 0.9.15

Map: Carla/Maps/Town10HD_Opt

说明 Windows CARLA Server 与 Ubuntu / WSL2 Python 开发环境之间通信正常。

需要注意的是，电脑重启后 WSL2 网络地址可能发生变化，因此重新启动项目环境后需要再次检查主机 IP。

## 10. 环境搭建过程中遇到的问题

### Ubuntu 下载问题

通过 Microsoft Store 安装 Ubuntu 时出现下载和系统要求检查问题。

最终采用 Ubuntu 22.04 WSL 镜像手动导入的方式完成安装。

### WSL2 图形兼容问题

最开始尝试直接在 WSL2 中启动 CARLA Linux Server。

虽然 nvidia-smi 和 OpenGL 都能够正常识别 NVIDIA GPU，但 Vulkan 检查结果显示使用的是 llvmpipe 软件渲染。

由于 CARLA 的 Unreal Engine 依赖 Vulkan，因此 Linux Server 无法在当前 WSL2 图形环境中正常运行。

最终将 CARLA Simulator Server 改为在 Windows 中运行，Ubuntu / WSL2 继续作为 Python 开发环境。

调整后 CARLA 可以正常启动，同时 Python Client 也可以成功连接 CARLA Server。

## 11. 最终开发环境

最终项目环境结构为：

Windows 11
│
├── CARLA 0.9.15 Simulator Server
│
└── WSL2
    │
    └── Ubuntu 22.04.5 LTS
        │
        ├── Python 3.10.12
        ├── Python Virtual Environment
        └── CARLA Python API 0.9.15

目前 CARLA Simulator 可以正常启动，Ubuntu / WSL2 中的 Python 环境也能够正常连接 CARLA Server。

至此，第一周开发环境搭建完成，可以继续进行 CARLA 官方示例、传感器配置以及后续数据采集任务。
