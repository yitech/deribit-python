from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="deribit-python",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python wrapper for the Deribit cryptocurrency exchange API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/deribit-python",
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
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "websockets>=10.0",
        "aiohttp>=3.8.0",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.16.0",
            "black>=21.0",
            "isort>=5.0",
            "mypy>=0.900",
            "flake8>=3.9",
        ],
    },
) 