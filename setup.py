"""Setup script for termicode - Terminal Coding Assistant"""
from setuptools import setup, find_packages

setup(
    name="termicode",
    version="1.0.0",
    description="AI-powered terminal coding assistant",
    author="Tris",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        'console_scripts': [
            'termicode=main:main',
        ],
    },
    python_requires='>=3.8',
)
