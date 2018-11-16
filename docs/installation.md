---
title: Installation  
---

The tools to validate your OSP submission files to [JSSPP](http://jsspp.org/index.php?page=cfp) are written 
in Python. Make sure you have [Python 3.7](https://www.python.org/downloads/release/python-367/) installed or setup an
appropriate virtual environment.

## Install from PyPi
Install the tools from the [PyPi](https://pypi.org/) repository using pip:
```bash
$ pip install jsspp-osp
``` 
The `jsspp-osp` command should now be available to validate the files you want to submit.

## Install manually
For manual installation, we use **Pipenv** to create and manage the virtual environment for the tools' runtime and
dependencies. Please follow the steps below to install the tools manually:

1. Install **Pipenv**. See their [Installation Guide](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv)
for instructions.
2. Download the tools by cloning the repository:
   ```bash
   $ git clone https://github.com/atlarge-research/jsspp-osp.git
   ```
   or simply [grab](https://github.com/atlarge-research/jsspp/archive/master.zip) a copy of the source code as a 
   zip file.
3. Download the required dependencies by running the following command in the source directory:
   ```bash
    $ pipenv install
   ```
4. Install the tools into the virtual environment:
   ```bash
    $ pipenv install -e .
   ```
5. Enter the virtual environment:
   ```bash
    $ pipenv shell
   ```
   The `jsspp-osp` command should now be available to validate the files you want to submit.
