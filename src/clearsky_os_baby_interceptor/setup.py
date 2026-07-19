from setuptools import find_packages, setup


setup(
    name="clearsky_os_baby_interceptor",
    version="0.1.0",
    packages=find_packages(exclude=["tests"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/clearsky_os_baby_interceptor"]),
        ("share/clearsky_os_baby_interceptor", ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="ClearSky OS Team",
    maintainer_email="maintainers@fratres-x.ai",
    description="Simulation-only optional baby interceptor for ClearSky OS counter-UAS stack.",
    license="Apache-2.0",
)
