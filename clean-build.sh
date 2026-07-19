#!/bin/bash
cd /opt/clearsky_os_ws
source /opt/ros/kilted/setup.bash
rm -rf build/ install/ log/ 2>/dev/null || true
colcon build --symlink-install --packages-up-to clearsky_os_bringup
source install/setup.bash
echo "✅ Clean build complete. Run: ros2 launch clearsky_os_bringup clearsky_os_basic_demo.launch.py"
