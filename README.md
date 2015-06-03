msat
======

Multiset Constraint Solver for Multi-SAT (Version-1.1)

* [Environments](#environments)
 * [Python](#python)
* [How to get msat](#how-to-get-msat)
* [Run msat](#run-msat)
* [List commands and get help](#list-commands-and-get-help)
 * [Standard file format of multiset constraint problem](#standard-file-format-of-multiset-constraint-problem)

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

`ms` is the main script name.<br />
`cmd` is the msat command.<br />
`options and others` are options or target objects of the corresponding "cmd".<br />

---

### List commands and get help

We can use "cmd" to list all avalible msat commands:

```
$ ms cmd
cmd          : list all avalible commands and their short usage
solve        : solve a mc problem
set          : edit the settings.py
help         : show the full infomation of a command
```

If we want to know the details of a specific command, just use msat command `help`:

```
$ ms help solve

    USAGE: solve a mc problem
    SYNOPSIS:
        solve [option] <mc file>
    OPTION:
```

`USAGE` gives a brief description of this command.<br />
`SYNOPSIS` gives the format of this command.<br />

For example, if you want to use command `solve` for solving a multiset constraint problem (written in standard mc file format named example.mc) with default settings (that means you don't need to use any options), just type:

```
$ ms solve example.mc
```

---

### Solve a multiset constraint problem

First, you should have a standard mc file for describing the multiset constraint problem with some user-specified settings.

#### Standard file format of multiset constraint problem 
