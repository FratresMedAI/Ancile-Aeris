from setuptools import find_packages, setup


setup(
    name="baby_interceptor",
    version="0.1.0",
    packages=find_packages(exclude=["tests"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/baby_interceptor"]),
        ("share/baby_interceptor", ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Ancile Aeris Team",
    maintainer_email="maintainers@fratres-x.ai",
    description="Simulation-only optional baby interceptor for Ancile Aeris counter-UAS stack.",
    license="Apache-2.0",
)
