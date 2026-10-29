from setuptools import find_packages, setup
from pathlib import Path
from typing import List


HYPEN_E_DOT = "-e ."

def get_requirements(file_path: str) -> List[str]:
    requirements = []

    with open(file_path, "r") as file_obj:
        requirements = [req.strip() for req in file_obj.readlines()]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements
       
        


setup(
    name="MLProject",
    version="0.0.1",
    author="Sheshpal",
    author_email="sheshpalsingh2024@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
    
    
)