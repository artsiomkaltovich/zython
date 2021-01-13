cd doc &&
sudo apt-get install python3-sphinx &&
sphinx-apidoc ../zython -d 2 -o source/api --force &&
make github
