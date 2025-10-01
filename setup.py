"""Setup script for termicode - Terminal Coding Assistant"""
from setuptools import setup, find_packages

setup(
    name="termicode",
    version="1.0.0",
    description="AI-powered terminal coding assistant",
    author="Tris",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        'console_scripts': [
            'termicode=termicode.cli:main',
        ],
    },
    python_requires='>=3.8',
)
