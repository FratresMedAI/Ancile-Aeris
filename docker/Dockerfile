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

RUN python3 -m venv /opt/ancile_venv \
    && /opt/ancile_venv/bin/pip install --no-cache-dir streamlit

WORKDIR /opt/ancile_aeris_ws
COPY . /opt/ancile_aeris_ws

RUN chmod +x /opt/ancile_aeris_ws/clean-build.sh \
    && rm -rf /opt/ancile_aeris_ws/build /opt/ancile_aeris_ws/install /opt/ancile_aeris_ws/log \
    && cd /opt/ancile_aeris_ws && ./clean-build.sh

CMD ["bash", "-lc", "source /opt/ros/kilted/setup.bash && source /opt/ancile_aeris_ws/install/setup.bash && ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py"]

