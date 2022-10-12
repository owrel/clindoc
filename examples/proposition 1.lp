%*

@desc Sudoku solver. Takes as input *instance* predicates, it also takes as option *dim* representing the dimension of the sudoku grid. *instance* predicates represetn a value of cell at a given position. The solver will always return a solution if a solution exist 

@input instance(X,Y,V) -> input predicate trepresenting the value of a cell at a given position, "the cell at position (X,Y) has an initial value of V
    @arg X ->  x position of the cell
    @arg Y ->  y position of the cell
    @arg V ->  value of the cell

@output sudoku(X,Y,V) -> predicate representing the value of a cell at a given position
@option dim -> The dimension of the sudoku : (dim*dim) x (dim*dim)


@example
    """
    instance(1,1,1), instance(2,2,2) ...
    """
    
    sudoku(1,1,1), sudoku(2,2,2) ...


@author Potsdam University

@author Potassco S.

*%




%--- `instance(X,Y,V)` The cell (`X`, `Y`) has an initial value of `V`
#defined instance/3.

%--- The dimension of the Sudoku: `dim*dim x dim*dim grid
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


%- translation
sudoku(X,Y,V) :- initial(X,Y,V).


#show sudoku(X,Y,V):sudoku(X,Y,V),V=9. 
