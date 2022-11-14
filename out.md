# SUDOKU
## Description 
Sudoku solver. Takes as input *instance* predicates, it also takes as option *dim* representing the dimension of the sudoku grid. *instance* predicates represetn a value of cell at a given position. The solver will always return a solution if a solution exist
## Usage 
```bash 
clingo sudoku.lp [instance] [-c dim=3] 
```
## Example  
 ```prolog
instance(1,1,1), instance(2,2,2) ...
    sudoku(1,1,1), sudoku(2,2,2) ...
```
## Dependencies 
None
## Background 
https://en.wikipedia.org/wiki/Sudoku
### Dev 
https://github.com/...
##Author(s) 

Potsdam University
@author Potassco S.

