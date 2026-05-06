from setuptools import setup


setup(
    name="baby_interceptor",
    version="0.1.0",
    packages=[],
    data_files=[("share/baby_interceptor", ["package.xml"])],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Ancile Aeris Team",
    maintainer_email="maintainer@example.com",
    description="Simulation-only optional baby interceptor for Ancile Aeris counter-UAS stack.",
    license="Apache-2.0",
)
