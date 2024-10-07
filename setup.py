# setup.py

from setuptools import setup, find_packages

setup(
    name='your_project',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'torch',
        'vispy',
        'PyYAML',
        'tk'
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='Reinforcement Learning Simulation with Predator-Prey Agents',
    url='https://github.com/yourusername/your_project',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
