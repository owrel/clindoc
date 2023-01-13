#include "encoding/sudoku.lp".


%@usage(clingo sudoku.lp instance.lp 1, console) -> To solve an instance we use the ASP solver clingo, with the following commandline

%@installation(git clone https://github.com/Owrel/ReadTheClindoc.git , console) -> To use the sudoku solver, clone the git repo:

%@example(instance(2,3,7). instance(3,3,6). instance(4,3,5). instance(5,3,1). instance(6,3,8). ..., cplint) -> An instance
%@example(clingo sudoku.lp instance.lp 1,console) -> Commandline
%@example(sudoku(2,3,7) sudoku(3,3,6) sudoku(4,3,5) sudoku(5,3,1)... ,cplint) -> The output
