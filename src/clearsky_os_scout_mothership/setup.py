from setuptools import find_packages, setup


setup(
    name="clearsky_os_scout_mothership",
    version="0.1.0",
    packages=find_packages(exclude=["tests"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/clearsky_os_scout_mothership"]),
        ("share/clearsky_os_scout_mothership", ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="ClearSky OS Team",
    maintainer_email="maintainers@fratres-x.ai",
    description="Mesh-capable high-altitude scout mothership ISR simulation for ClearSky OS.",
    license="Apache-2.0",
)
