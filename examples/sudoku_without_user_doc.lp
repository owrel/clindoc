%--- `instance(X,Y,V)` The cell (`X`, `Y`) has an initial value of `V`
#defined instance/3.

%--- The dimension of the Sudoku: `dim*dim x dim*dim grid
#const dim = 2. 
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

#show sudoku(X,Y,V):sudoku(X,Y,V). 
