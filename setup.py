"""Project setup configuration."""

from setuptools import setup, find_packages

setup(
    name="spacex-landing-predictor",
    version="2.0.0",
    description="SpaceX Falcon 9 Landing Prediction using ML",
    author="Data Science Capstone Project",
    packages=find_packages(exclude=["tests", "notebooks"]),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "pandas>=1.5.0",
        "numpy>=1.23.0",
        "matplotlib>=3.6.0",
        "seaborn>=0.12.0",
        "scikit-learn>=1.2.0",
        "jupyter>=1.0.0",
        "ipython>=8.0.0",
        "python-dotenv>=0.21.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=5.0.0",
            "mypy>=0.990",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
