#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
from pathlib import Path

import zython
from setuptools import setup, find_packages

setup(
    name="zython",
    version=zython.__version__,
    python_requires=">=3.6",
    author="Artsiom Kaltovich",
    author_email="kaltovichartyom@gmail.com",
    description="Express constraint programming problem with python and solve it with minizinc",
    long_description=Path("README.md").read_text(encoding="UTF-8"),
    long_description_content_type="text/markdown",
    url="TBD",
    project_urls={
        "Bug Tracker": "https://github.com/ArtyomKaltovich/zython/issues",
        "Documentation": "TBD",
        "Source": "https://github.com/ArtyomKaltovich/zython",
    },
    packages=[p for p in find_packages() if p.startswith("zython")],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    install_requires=[
        "wheel",
        "minizinc >= 0.4.2",
    ]
)
