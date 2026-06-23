
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="portscanner-edu",
    version="1.0.0",
    author="Educational Port Scanner",
    description="A friendly, educational port scanner for learning networking concepts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/F0CUSMSK/PortScanner",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: System :: Networking",
        "Intended Audience :: Education",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "portscanner=main:main",
        ],
    },
)
