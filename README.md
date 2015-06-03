msat
======

Multiset Constraint Solver for Multi-SAT (Version-1.1)

* [Environments](#environments)
 * [Python](#python)
* [How to get msat](#how-to-get-msat)
* [Run msat](#run-msat)
* [List commands and get help](#list-commands-and-get-help)
===

### Environments

#### Python

You have to install `Python3`.
* [Python](https://www.python.org/)

---

### How to get msat

Just download from github tarball:
* [download msat](https://github.com/dokelung/msat/tarball/v1.1)

User also can install msat from pip (Python3 Version, sometimes called pip3):

```sh
$ pip install msat
```
If there is new version, use upgrade:

```sh
$ pip install msat --upgrade
```
Here is the pypi page of msat:

* [PyPI page of msat](https://pypi.python.org/pypi/msat)

Note that if you install msat from pip, you will not get benches here.

---

### Run msat

If you do not install the packages and script, just `cd` to the top directory:

```sh
$ ./ms
```

If you have already installed it, just type `ms`:

```sh
$ ms
```

You will see following info:

```sh
M-SAT:
    python3 ms <cmd> [options or others]
          ./ms <cmd> [options or others]
    Please use "cmd" to list all avalible commands
```

The format of ms command is:

```sh
ms <cmd> [options or others]
```

`ms` is the main script name.
`cmd` is the msat command.
`options and others` is options or target objects of the corresponding "cmd".

---

### List commands and get help

We can use "cmd" to list all avalible msat commands:

```sh
$ ms cmd
cmd          : list all avalible commands and their short usage
solve        : solve a mc problem
set          : edit the settings.py
help         : show the full infomation of a command
```

---
