import setuptools
import importlib.util
import os

def get_lib_ver():
    spec = importlib.util.spec_from_file_location("tdsbconnects.version", os.path.join(os.path.dirname(__file__), "tdsbconnects/version.py"))
    version = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(version)
    return version.__version__

lib_ver = get_lib_ver()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytdsbconnects",
    version=lib_ver,
    author="Tyler Tian",
    author_email="tylertian123@gmail.com",
    description="A basic Python TDSB Connects API using aiohttp.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tylertian123/pytdsbconnects",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    install_requires=[
        "pytz",
        "aiohttp"
    ],
    python_requires=">=3.6",
    keywords="tdsb",
    license="MIT",
    project_urls={
        "Bug Tracker": "https://github.com/tylertian123/pytdsbconnects/issues",
        "Source Code": "https://github.com/tylertian123/pytdsbconnects"
    }
)
