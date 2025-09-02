"""
Copyright (c) 2025 MPI-M, Clara Bayley

----- ValidatingCLEO -----
File: setup.py
Project: ValidatingCLEO
Created Date: Friday 11th April 2025
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Friday 11th April 2025
Modified By: CB
-----
License: BSD 3-Clause "New" or "Revised" License
https://opensource.org/licenses/BSD-3-Clause
-----
File Description:
setup for pre-commit tool
"""


from setuptools import setup, find_packages

setup(
    name="ValidatingCLEO",
    version="0.6.0",
    packages=find_packages(),
    install_requires=[
        "pytest",
        "sphinx",
    ],
)
