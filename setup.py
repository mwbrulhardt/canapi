import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="canapi",
    version="0.0.1",
    description="A universal client api generator.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/finverse/canapi",
    author="Matthew Brulhardt",
    author_email="mwbrulhardt@finverselabs.com",
    license="Apache 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True
)
