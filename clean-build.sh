#!/bin/bash
cd /opt/ancile_aeris_ws
source /opt/ros/kilted/setup.bash
rm -rf build/ install/ log/ 2>/dev/null || true
colcon build --symlink-install --packages-up-to ancile_aeris_bringup
source install/setup.bash
echo "✅ Clean build complete. Run: ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py"
