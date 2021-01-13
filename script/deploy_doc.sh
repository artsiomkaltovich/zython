cd doc &&
sphinx-apidoc ../zython -d 2 -o source/api --force &&
make github
