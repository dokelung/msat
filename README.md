msat
======

Multiset Constraint Solver for Multi-SAT (Version-1.1)

* [Environments](#environments)
 * [Python](#python)
* [How to get msat](#how-to-get-msat)
* [Run msat](#run-msat)
* [List commands and get help](#list-commands-and-get-help)
* [Solve a multiset constraint problem](#solve-a-multiset-constraint-problem)
 * [Standard file format of multiset constraint problem](#standard-file-format-of-multiset-constraint-problem)
 * [Solve it](#solve-it)
 * [Log and log file](#log-messages-and-log-file)

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

Let's see following example:

```
# example.mc
e 5 6 18 44 12 3 33 11 45
e 7 9 8 10 8 11 32 15 23 24 1 1 2 2 4 6 8 4 55 12 79 86 12 15 16 33 12 13
t 11 74 36 56 15 9
t 10 8 43 15 47 2 14 12 67 79 98 31 45 13 2
r =
s PROGRESS = False
s ELEMENTS_ORDER = 'increase' # increase/decrease/no
s TARGETS_ORDER = 'increase'  # increase/decrease/no
```

It is a standard-format file of a multiset constraint problem.<br />
User should use `e`, `t`, `r`, `s`, and `#` as the first non-blank char of a line.<br />
We call these chars as "line keyword".<br />
keyword `e` is used to specify elements (element set).<br />
Keyword `t` is used to specify targets (target set).<br />
Keyword `r` is used to specify the relation between multi-subset and its corresponding target.
Keyword `s` is used to do solver settings for a specific multiset constraint problem.<br />
Finally, `#` is used to write down comments.

Note that we could use multiple "e lines" or "t lines" to describe an element set and target set respectively and the setting statements are also allowed with comment.

#### Solve it

#### Log and log file

---
