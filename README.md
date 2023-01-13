# Clindoc
Documentation framework for ASP, from user to contributor.

# Installation

Cloning from git:
```bash
git clone https://github.com/Owrel/clindoc.git
```

Moving to the Clindoc directory

```bash
cd clindoc
```

Installing the package:

```bash
pip install .
```

# Usage

First you can see all of the help

```bash
python -m clindoc -h
```

There few options for clindoc that allows you to create custom documentation.


## Basic usage

Given a folder like :

```
sudoku
├── encoding
│   └── sudoku.lp
└── input.lp
```

*It can be any folder, this folder layout is just for the example*


We can generate documentation of the folder sudoku with the following command (from the examples folder of the package *clindoc/examples*):

```bash
python -m clindoc "Encoding Title: Sudoku" ./sudoku/ 
```


## Options

Here's all the option available:

```
Global Clindoc parameters:
  project_name          Name of the project
  src_dir               Directory containing the LP files from which to generate the documentation
  --description DESCRIPTION, --desc DESCRIPTION
                        Description of the project
  --doc-dir DOC_DIR, -d DOC_DIR
                        The folder where the documentation in rst format will be generated. If not specified, it will default to [src-dir]/docs/source.)
  --out-dir OUT_DIR, -b OUT_DIR
                        Directory where Sphinx will output the generated documentation (if not specified, defaults to [src-dir]/docs/build)
  --builder BUILDER     Sphinx output format parameter (refer to parameter builder sphinx. Can be any builder supported by Sphinx)
  --clean               (flag) remove [doc-dir] and [out-dir] before running. Please be sure that you saved any hand-made modification
  --no-sphinx-build     (flag,debug) skip Sphinx build
  -v, --version         Print the version and exit

User Documentation parameters:
  --userdoc.exclude     (flag) component will be excluded from the documentation

Contributor Documentation parameters:
  --contributordoc.exclude
                        (flag) component will be excluded from the documentation
  --contributordoc.group-by CONTRIBUTORDOC.GROUP_BY
                        How the contributor documentation will group the different elements. "section" or "type"
  --contributordoc.hide-uncommented
                        (flag) hide non-commented or non-defined term, rules...
  --contributordoc.hide-code
                        (flag) hide source code

Dependency graph parameters:
  --dependencygraph.exclude
                        (flag) component will be excluded from the documentation
  --dependencygraph.format DEPENDENCYGRAPH.FORMAT
                        Format of the graphs

Source files parameters:
  --source.exclude      (flag) component will be excluded from the documentation
  --source.exclude-file [SOURCE.EXCLUDE_FILE ...]
                        source file(s) that will be excluded from source documentation section

```

## Author
Potsdam University | Potascco Solution
