from setuptools import setup,find_packages
from typing import List

HYPHEN_E_DOT = "-e ."

def get_requirements(file_path: str) -> List[str]:
    requirements = []
    with open(file_path) as file:
        requirements = file.readlines()
        requirements = [req.strip() for req in requirements]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements

setup(
    name="Lung-Xray",
    version='0.0.1',
    author='Akash',
    author_email='akashmukherjee0000@gmail.com',
     description="A small python package for ml app",
    package_dir={"": "src"},
    packages=find_packages(where="src")
)