from setuptools import setup


package_name = "clearsky_os_operator_copilot"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="ClearSky-OS Team",
    maintainer_email="maintainers@fratres-x.ai",
    description="Edge operator co-pilot query service for ClearSky OS.",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "clearsky_os_operator_copilot_node = clearsky_os_operator_copilot.copilot_node:main",
        ],
    },
)
