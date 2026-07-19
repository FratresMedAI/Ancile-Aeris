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

# Optional ML stack: docker build --build-arg CLEARSKY_INSTALL_ML=1
ARG CLEARSKY_INSTALL_ML=0

WORKDIR /opt/clearsky_os_ws
COPY requirements-ml.txt /opt/clearsky_os_ws/requirements-ml.txt

RUN python3 -m venv /opt/clearsky_venv \
    && /opt/clearsky_venv/bin/pip install --no-cache-dir streamlit \
    && if [ "$CLEARSKY_INSTALL_ML" = "1" ]; then \
         /opt/clearsky_venv/bin/pip install --no-cache-dir -r /opt/clearsky_os_ws/requirements-ml.txt; \
       fi

ENV PATH="/opt/clearsky_venv/bin:${PATH}"

COPY . /opt/clearsky_os_ws

RUN chmod +x /opt/clearsky_os_ws/clean-build.sh \
    && rm -rf /opt/clearsky_os_ws/build /opt/clearsky_os_ws/install /opt/clearsky_os_ws/log \
    && cd /opt/clearsky_os_ws && ./clean-build.sh

CMD ["bash", "-lc", "source /opt/ros/kilted/setup.bash && source /opt/clearsky_os_ws/install/setup.bash && ros2 launch clearsky_os_bringup clearsky_os_basic_demo.launch.py"]
