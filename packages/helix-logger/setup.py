"""
🌀 Helix Logger - Enhanced logging for the Helix ecosystem
"""

from setuptools import find_packages, setup

setup(
    name="helix-logger",
    version="1.0.0",
    description="Helix Logger - Enhanced logging with consciousness metrics",
    long_description=open("README.md").read() if __file__ else "",
    long_description_content_type="text/markdown",
    author="Helix Collective",
    author_email="contact@helix.ai",
    url="https://github.com/helix/helix-logger",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "colorama>=0.4.6",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="logging helix consciousness metrics",
    license="MIT",
)
