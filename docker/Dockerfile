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

WORKDIR /opt/counterdrone_ws
COPY . /opt/counterdrone_ws

RUN source /opt/ros/kilted/setup.bash && colcon build --symlink-install

CMD ["bash", "-lc", "source /opt/ros/kilted/setup.bash && source /opt/counterdrone_ws/install/setup.bash && ros2 launch counterdrone_core full_system.launch.py sim_mode:=${ANCILE_SIM_MODE:-true} payload:=${ANCILE_PAYLOAD:-cuas}"]
