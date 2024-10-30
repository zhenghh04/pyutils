from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="timeline",  # Replace with your package's name
    version="0.1.0",  # Initial version
    author="Huihuo Zheng",
    author_email="zhenghh04@gmail.com",
    description="A package for generating and visualizing timelines.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/timeline",  # Replace with your repo URL
    packages=find_packages(),  # Automatically find packages in your project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "matplotlib>=3.0",  # Example dependency for plotting timelines
        "pandas>=1.0",      # Example dependency for data manipulation
    ],
    entry_points={
        "console_scripts": [
            "merge_trace=timeline.merge_trace:main",  # Exposes a command-line tool if needed
        ],
    },
)
