
%@predicate(sudoku/3,sudoku(X,Y,V) ) -> The cell (`X`, `Y`) has value `V` with `0<V<=dim*dim`
%@term(X) -> collumn index of a cell
%@term(Y) -> row index of a cell





val(1..dim*dim).
pos(X,Y) :- val(X), val(Y).

%@section(Rules)

subgrid(X,Y,(((X-1)/dim)*dim+((Y-1)/dim))) :- pos(X,Y). %- `subgrid(X,Y,S)` The cell (`X`, `Y`) is in subgrid `S`

%- At most/least one value per cell
1 { sudoku(X,Y,V) : val(V) } 1 :- pos(X,Y).



%@section(Constraints) -> List all of the Constraints
%- Can't repeat values per row
:- sudoku(X,Y,V), sudoku(X',Y,V), X != X'.
%- Can't repeat values per column
:- sudoku(X,Y,V), sudoku(X,Y',V), Y != Y'.
%- Can't repeat values per subgrid
:- sudoku(X,Y,V), sudoku(X',Y',V), subgrid(X,Y,S), subgrid(X',Y',S), (X,Y)!=(X',Y').

%@section(Translation & Output)
sudoku(X,Y,V) :- instance(X,Y,V).

