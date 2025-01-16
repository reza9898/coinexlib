from setuptools import setup, find_packages

setup(
    name="coinexlib",  # Replace with your desired package name
    version="1.0.0",  # Update version as needed
    author="Reza Rizvandi",
    author_email="r.rizvandi@gmail.com",
    description="A Python library for interacting with the CoinEx API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/reza9898/coinexlib",  # Replace with your repository URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",  # Add all required dependencies
    ],
)
