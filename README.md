
## Zoeppritz Energy Explorer

Zoeppritz Energy Explorer is an interactive tool for exploring the partitioning of seismic energy at a plane boundary between two rocks. It plots the (normalized) reflected and transmitted p and s wave energy coefficients as a function of the incident angle of the incident p-wave. It allows the user to set properties of the two rocks and updates the graph in real time. 

![Screenshot](/screenshot.png?raw=true)

## Installation (Ubuntu/Debian)
The following steps use [pyenv](https://github.com/pyenv/pyenv#installation) for python version management and [pipenv](https://pypi.org/project/pipenv/) for package management. If you don't have them installed check them out first.

### Install system dependencies
There are system dependencies for pycairo and pygobject. To install them: 

```sh
$ sudo apt-get install -y libgirepository1.0-dev build-essential \
  libbz2-dev libreadline-dev libssl-dev zlib1g-dev libsqlite3-dev wget \
  curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libcairo2-dev \
```

Python 3.9.7 is recommended. To install and activate a virtual environment with pyenv:
```sh
$ pyenv install 3.9.7
$ pyenv activate
```

### Install package dependencies
```sh
$ pipenv install
```

## Running
From the `zoeppritz` directory run:
```sh
$ python main.py
```


