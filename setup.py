from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="haiblock",
    version="0.1.0",
    author="HaiBlock",
    author_email="support@haiblock.com",
    description="Official Python SDK for HaiBlock - AI Content Optimization Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HaiBlock/haiblock-python-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "boto3>=1.26.0",
        "pydantic>=1.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
            "twine",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/HaiBlock/haiblock-python-sdk/issues",
        "Source": "https://github.com/HaiBlock/haiblock-python-sdk",
        "Documentation": "https://docs.haiblock.com",
    },
)