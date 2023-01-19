# Clindoc
Documentation framework for ASP, from user to contributor.

# Installation

To install Clindoc, you can clone it from the git repository:
```bash
git clone https://github.com/Owrel/clindoc.git
```

Then navigate to the Clindoc directory:

```bash
cd clindoc
```

Finally, install the package by running:

```bash
pip install .
```

# Usage

To see all of the available options for Clindoc, you can run:

```bash
python -m clindoc -h
```

Clindoc allows you to create custom documentation by specifying different options.


### Basic usage

For example, given a folder structure like:

```
sudoku
├── encoding
│   └── sudoku.lp
└── input.lp
```

You can generate documentation for the sudoku folder with the following command (assuming you are in the clindoc/examples/sudoku directory):

```bash
python -m clindoc 
```

# Documenting an encoding

## Directives

Directives are special comments, they are identified as such:
```prolog
%@directive(param_1,...,param_n)
```

or with an optional description

```prolog
%@directive(param_1,...,param_n) -> Description
```

---
**NOTE**

Here's the associated regex expression (with named groups):
```regex
 *@ *(?P<tag_name>[a-zA-Z]+) *\((?P<parameters>[^\-\>]*)\) *(\-\> *(?P<description>[^\\n]*))?
```
---

### Sections

It is possible to split the encoding by sections, to do so, you can add the directive `section/1`, where it takes as parameter the name of the section. For instance such:

```prolog
%@section(Constraints) -> List all of the integrity constraints
:- ...
:- ...
```

### Terms

It is possible to give a definition of the variables used for a better understanding of the code, the `term` directive takes as unique parameter a variable (capitalized), for instance

```prolog
%@term(X) -> X refer the the x axis position
```


### Predicate

It is also possible to give a definition to a predicate, in other words, what the predicate means, where `predicate` directive takes 2 arguments: the signature (works as identifier) and the default variables. For instance (issued from the sudoku example): 

```prolog
%@predicate(sudoku/3,sudoku(X,Y,V) ) -> The cell (`X`, `Y`) has value `V` with `0<V<=dim*dim`
```


## Comments

it is also possible to comment specific lines in order to add explanation of what a specific line is doing, for instance (issued form the sudoku example):

 
```prolog
%- Can't repeat values per row
:- sudoku(X,Y,V), sudoku(X'',Y,V), X != X''.
```






## Options

Here's all the option available:

```
Clindoc - Generate documentation for ASP files

options:
  -h, --help            show this help message and exit

Global Clindoc parameters:
  --project_name PROJECT_NAME, -p PROJECT_NAME
                        Name of the project
  --src_dir SRC_DIR, -s SRC_DIR
                        Directory containing the LP files from which to generate the documentation
  --description DESCRIPTION, --desc DESCRIPTION
                        Description of the project
  --doc-dir DOC_DIR, -d DOC_DIR
                        The folder where the documentation in rst format will be generated. If not specified, it will default to [src-dir]/docs/)
  --out-dir OUT_DIR, -b OUT_DIR
                        Directory where Sphinx will output the generated documentation (if not specified, defaults to [src-dir]/docs/build)
  --builder BUILDER     Sphinx output format parameter (refer to parameter builder sphinx. Can be any builder supported by Sphinx)
  --clean               (flag) remove [doc-dir] and [out-dir] before running. Please be sure that you saved any hand-made modification
  --no-sphinx-build     (flag,debug) skip Sphinx build
  --no-rst-build        (flag,debug) skip rst build section
  --conf-path CONF_PATH
                        Path to a configuration file (json format). It can be created from the --dump-conf [path_to_conf] command. Any parameters entered in the command line will be ignored.
  --dump-conf DUMP_CONF
                        Path of a file where the configuration will be dumped. The json file will include all of the configuration you've entered in the command line. It can be used later as default configuration using --path-conf [path_to_conf]
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

KRR@UP - https://github.com/krr-up

```


# Python script

Clindoc can also be used in a python script by importing the Clindoc module and providing it with the desired parameters.

```python
import os
from clindoc import Clindoc

print(os.getcwd()) # /path/to/clindoc
c = Clindoc({'src_dir' : 'examples/mapf'})
c.build_documentation()
```

The parameters contained in the dict are the same as the options available in the command line. However, the - character must be replaced by _ and . should be replaced by a sub directory. For example, the following command line:

```bash
python -m clindoc --contributordoc.hide-code
```

Will result in python:

```python
c = Clindoc({'contributordoc' : 
  {'hide_code' : True}
})
c.build_documentation()
```

This allows for more flexibility and automation when creating your documentation, as it can be integrated into your existing python scripts and automation processes.


The file "test.py" contains examples of different parameters hat can be used. 


## Author
Potsdam University | Potassco Solutions
