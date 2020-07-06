""" Setup configuration for ProductsAPI """
from setuptools import find_packages, setup

setup(
    name="ProductsAPI",
    version="0.0.1",
    description="Small API that works with products read from json file.",
    author="sWallyx <mikelsmartinez@aol.com>",
    keywords=["python", "scripts", "api"],
    classifiers=[],
    install_requires=["pandas", "requests", "Flask", "flask_jsonpify"],
    setup_requires=[],
    tests_require=[],
    packages=find_packages(),
)
