#!/bin/env python3

import setuptools

with open("readme.md", "r") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name="bitwarden-rofi", # Replace with your own username
    version="0.0.1",
    author="Adrián Lattes",
    author_email="adrianlattes@disroot.org",
    description="bitwarden-cli rofi wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haztecaso/bitwarden-rofi",
    packages=setuptools.find_packages(),
    entry_points={ "console_scripts": ["bwmenu = bwmenu.__main__:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    python_requires='>=3.6',
)

