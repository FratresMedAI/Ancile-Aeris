# syntax=docker/dockerfile:1.7
FROM ros:kilted-ros-base AS base

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.12 python3-pip python3.12-venv python3-colcon-common-extensions \
    build-essential cmake git \
    ros-kilted-rmw-fastrtps-cpp \
    ros-kilted-rmw-cyclonedds-cpp \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/clearsky_venv \
    && /opt/clearsky_venv/bin/pip install --no-cache-dir streamlit

WORKDIR /opt/clearsky_os_ws
COPY . /opt/clearsky_os_ws

RUN chmod +x /opt/clearsky_os_ws/clean-build.sh \
    && rm -rf /opt/clearsky_os_ws/build /opt/clearsky_os_ws/install /opt/clearsky_os_ws/log \
    && cd /opt/clearsky_os_ws && ./clean-build.sh

CMD ["bash", "-lc", "source /opt/ros/kilted/setup.bash && source /opt/clearsky_os_ws/install/setup.bash && ros2 launch clearsky_os_bringup clearsky_os_basic_demo.launch.py"]

