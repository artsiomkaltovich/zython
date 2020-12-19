flake8 zython --count --max-complexity=10 --max-line-length=120 --statistics &&
pytest doc --doctest-glob=*.rst --doctest-modules &&
tox
