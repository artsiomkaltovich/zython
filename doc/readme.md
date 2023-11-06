To generate sphinx documentation from source doc comments 
you should run following command (from project root)

```shell
sphinx-apidoc -f -o docs/source/api zython
```

To build html doc (which will be in doc/build/html/index.html):

```shell
python -m sphinx -T -E -b html -d _build/doctrees -D language=en doc/source doc/build/html
```
