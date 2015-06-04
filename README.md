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
 * [Log and log file](#log-and-log-file)
* [Settings](#settings)

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
User should use `e`, `t`, `r`, `s`, and `#` as the first non-blank char of a line.

We call these chars as "line keyword":
* keyword `e` is used to specify elements (element set).<br />
* Keyword `t` is used to specify targets (target set).<br />
* Keyword `r` is used to specify the relation between multi-subset and its corresponding target.
* Keyword `s` is used to do solver settings for a specific multiset constraint problem.
* Keyword, `#` is used to write down comments.

Note that we could use multiple "e lines" and "t lines" to describe element set and target set respectively. Also, the setting statements are allowed with comment.

#### Solve it

Solve a multiset constraint file (mc file) is easy. Use command `solve`:

```
$ ms solve example.mc
```

#### Log and log file

Let's introduce the log of solving. Take above mc problem as example, the log is like following:

```
================================================================================
|               MSAT - Multiset Constraint Solver for Multi-SAT                |
================================================================================
| % MC file             : test2.mc                                             |
| % Elements (Num:37)   : [5, 6, 18, 44, 12, 3, 33, 11, 45, 7, 9, 8, ... more  |
| % Targets  (Num:21)   : [11, 74, 36, 56, 15, 9, 10, 8, 43, 15, 47, ... more  |
| % Relation            : =                                                    |
--------------------------------------------------------------------------------
|                       Mc Settings specified in Mc File                       |
--------------------------------------------------------------------------------
| S TARGETS_ORDER = 'increase'         || S ELEMENTS_ORDER = 'increase'        |
| S PROGRESS = False                   ||                                      |
--------------------------------------------------------------------------------
|                           MC Table & MC Dictionary                           |
--------------------------------------------------------------------------------
| % Table Size          : 38*686 = 26068                                       |
| % Elements Order      : increase                                             |
| % J-range Min         : False                                                |
| % Build Time          : 0.13407                                              |
--------------------------------------------------------------------------------
|                         Multiset Constraint Solving                          |
--------------------------------------------------------------------------------
| % Satisfiability      : False                                                |
| % Solving Time        : 0.00018                                              |
--------------------------------------------------------------------------------
|                              Profiling Summary                               |
--------------------------------------------------------------------------------
| % backtrack_num       : 1                                                    |
| % check_sum_fail_num  : 1                                                    |
| % check_sum_comb_fail_num: 0                                                 |
| % check_distance_fail_num: 0                                                 |
| % forbiden_combination_num: 0                                                |
================================================================================
```

First, solver lists the basic info of the multiset constraint problem including the file's name, elements (and it's number), targets (and it's number) and the relation.

Then the settings specified in the MC file are listed. Solver doesn't show the default settings in `settings.py`.

The next block shows the info of MC table and MC dictionary including:
* Table size: with the form of `row number X column number = table entry number`
* Elements order: the order of elements for building the table and dictionary.
* J-range min: this value is True if solver minimizes the column size.
* Build Time: cost time for building the table and dictionary.

When solving is finished, solver will show the satisfiability of this MC problem and the solving time.

Finally, the profiling summary is given.

If you want to dump the log in to a file, just use redirection:

```sh
$ mc solve example.mc > example.log
```

---

### Settings

We can modify the solver settings by modify the file `settings.py` in the module directory of `msat`.

If msat is not installed by `pip` and user have the editor `vim`, we can use msat command set to help us:

```
$ ms set
```

Let me introduce all avalible solver settings to you.

#### Solver display

There are two width param for us to modify the size of log window.

* SOLVER_WIDTH
 * width of solver window
 * is an even

* SOLVER_ITEM_WIDTH
 * width of an item name like "Table Size" or "Satisfiability"
 * is an integer

```python
SOLVER_WIDTH = 80 # should be even
SOLVER_ITEM_WIDTH = 20
```

#### MC table

When solver constructs the MC table, it fix the orders of element set and target set first.

* ELEMENTS_ORDER
 * order of elements for building the MC table
 * 3 strings are allowed: `'increase'`, `'decrease'` and `'no'`
 * for example, elements set = `(2, 4, 5, 1, 3)`
   * use `increase` => elements list = `[1, 2, 3, 4, 5]`
   * use `decrease` => elements list = `[5, 4, 3, 2, 1]`
   * use `no`       => elements list = `[2, 4, 5, 1, 3]` (original order)

* TARGETS_ORDER
 * order of targets for building the MC table
 * this order just affects the choose process
 * 3 strings are allowed: `'increase'`, `'decrease'` and `'no'` (the meaning just as `ELEMENTS_ORDER`)

When building MC table, we could decide whether minize the column number of MC table. If the value is true, we could build a smaller MC table with less memory use and less building time. But set this value True can speed up the searching time when quering value of MC table.

* JRANGE_MIN
 * is a boolean value

```python
ELEMENTS_ORDER = 'increase' # increase/decrease/no
TARGETS_ORDER = 'increase'  # increase/decrease/no
JRANGE_MIN = False
```

#### Search

When doing search, solver tries to choose a target (or choose nothing) picking row element in each level. The strategy of choose can decided by user.

* CHOOSE_NOUSE_FIRST
 * let solver try to choose nothing first
 * is a boolean value
 
* CHOOSE_FROM_MAX_OR_MIN
 * let solver try to choose target with max(min) current value first
 * 3 strings are allowed: `'max'`, `'min'` and `'no'`
 * for example, current values of all targets are `[1, 2, 3, 4, 5]`
   * use `max` => try to choose from 5 to 1
   * use `min` => try to choose from 1 to 5
   * use `no`  => use the original order for choosing

```python
CHOOSE_NOUSE_FIRST = False
CHOOSE_FROM_MAX_OR_MIN = 'max' # max/min/no
```

#### Other constraint

```python
ALL_USE_RULE = False
```

```python
EARLY_CHECK_SATISFIABILITY = False
```

```python
CHECK_FOR_EARLY_BACKTRACK = True
CHECK_SUM = True
CHECK_SUM_COMB = True
CHECK_SUM_COMB_NUM = 6
CHECK_DISTANCES = True
CHECK_FORBIDEN = True
```

```python
PROGRESS = False
```

#### Judge satisfiability

#### Early backtrack set

#### Progress

#### Profiling

#### Debug

---
