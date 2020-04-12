from setuptools import find_packages, setup

setup(
    name="covid19-estimator-py",
    packages=find_packages(),
    install_requires=["flask", "flask-API", "dicttoxml"],
)
