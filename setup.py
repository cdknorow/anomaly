import sys
import os
from setuptools import setup, find_packages

__version__ = "0.1"

# 'setup.py publish' shortcut.
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    sys.exit()

# 'setup.py test' shortcut.
# !pip install --index-url https://test.pypi.org/simple/ sensiml -U
if sys.argv[-1] == "test":
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload --repository-url https://test.pypi.org/legacy/ dist/*")
    sys.exit()

setup(
    name="Anomaly",
    description="Generate Anomaly data for time-series sensor data",
    version=__version__,
    author="SensiML",
    author_email="chris.knorowski@sensiml.com",
    license="MIT",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=["*test*"]),
    include_package_data=True,
    long_description=open("README.md").read(),
    install_requires=["scipy", "numpy>=1.13", "pandas>=0.20.3"],
)
