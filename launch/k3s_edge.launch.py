from launch import LaunchDescription
from launch.actions import LogInfo


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        LogInfo(msg='K3s edge orchestration launch stub. Apply manifests in k8s/ for deployment.'),
    ])
