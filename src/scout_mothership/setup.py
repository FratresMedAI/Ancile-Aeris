from setuptools import setup


setup(
    name="scout_mothership",
    version="0.1.0",
    packages=[],
    data_files=[("share/scout_mothership", ["package.xml"])],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Ancile Aeris Team",
    maintainer_email="maintainer@example.com",
    description="Mesh-capable high-altitude scout mothership ISR simulation for Ancile Aeris.",
    license="Apache-2.0",
)
