# What is this?

A template for python packages

# How do I fill out this template?

1. Change the `pyproject.toml` file (package name, version, etc)
2. Change the `./main/your_package_name` folder
3. Edit the `./main/your_package_name/__init__.py` file, and change the `from your_package_name.main import *`
4. Open the `./main/setup.py` and edit the `install_requires=` part to include dependencies
5. Edit this readme (it will be the front page of the package)
6. Edit the `./main/your_package_name/main.py` to have your library in it
7. Run `project local_install` to install what you just made
8. Run `project publish` to release your package


## (Readme template below)

# What is this?

(Your answer here)

# How do I use this?

`pip install your_package_name`


```python
from your_package_name import something

# example of how to use your package here
```
