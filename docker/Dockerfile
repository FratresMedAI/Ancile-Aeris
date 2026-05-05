# syntax=docker/dockerfile:1.7
FROM ros:kilted-ros-base AS base

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.12 python3-pip python3.12-venv python3-colcon-common-extensions \
    build-essential cmake git \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/ancile_venv \
    && /opt/ancile_venv/bin/pip install --no-cache-dir streamlit

WORKDIR /opt/ancile_aeris_ws
COPY . /opt/ancile_aeris_ws

RUN rm -rf build install log && source /opt/ros/kilted/setup.bash && colcon build --symlink-install

CMD ["bash", "-lc", "source /opt/ros/kilted/setup.bash && source /opt/ancile_aeris_ws/install/setup.bash && ros2 launch ancile_aeris_bringup bringup.launch.py"]

