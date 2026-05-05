from setuptools import setup


package_name = "ancile_aeris_operator_copilot"

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
    maintainer="Ancile-Aeris Team",
    maintainer_email="maintainer@example.com",
    description="Edge operator co-pilot query service for Ancile Aeris.",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "ancile_aeris_operator_copilot_node = ancile_aeris_operator_copilot.copilot_node:main",
        ],
    },
)
