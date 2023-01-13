%*

@title SUDOKU 

@description 
    Sudoku solver. Takes as input *instance* predicates, it also takes as option *dim* representing the dimension of the sudoku grid. *instance* predicates represent a value of cell at a given position. The solver will always return a solution if a solution exist

@example
    instance(2,3,8). instance(3,3,9). instance(5,4,1). instance(6,4,2). instance(4,4,3). instance(1,4,4). instance(8,4,5). instance(7,4,6). instance(3,4,7). instance(9,4,8). instance(2,4,9). instance(1,5,1). instance(2,5,2). instance(3,5,3). instance(7,5,4). 

@usage
    clingo sudoku.lp [instance] [-c dim=3]

@dependencies
    None

@background 
    https://en.wikipedia.org/wiki/Sudoku

@dev
    https://github.com/...

@author Uni-Potsdam 

*%


#defined instance/3.
#const dim = 3.
val(1..dim*dim).
pos(X,Y) :- val(X), val(Y).
%- `subgrid(X,Y,S)` The cell (`X`, `Y`) is in subgrid `S`
subgrid(X,Y,(((X-1)/dim)*dim+((Y-1)/dim))) :- pos(X,Y).
%- `sudoku(X,Y,V)` The cell (`X`, `Y`) has value `V` with `0<V<=dim*dim`
1 { sudoku(X,Y,V) : val(V) } 1 :- pos(X,Y).
%- Can't repeat values per row
:- sudoku(X,Y,V), sudoku(X',Y,V), X != X'.
%- Can't repeat values per column
:- sudoku(X,Y,V), sudoku(X,Y',V), Y != Y'.
%- Can't repeat values per subgrid
:- sudoku(X,Y,V), sudoku(X',Y',V), subgrid(X,Y,S), subgrid(X',Y',S), (X,Y)!=(X',Y').

sudoku(X,Y,V) :- instance(X,Y,V).


#show sudoku(X,Y,V): sudoku(X,Y,V).

