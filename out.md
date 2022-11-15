
# Contributor documentation
## Inputs
Showing all inputs 

| **Signature** | **Location** | **Doc** |
|---------------|--------------|---------|
| instance/3 | Line; 2 | ['-- `instance(X,Y,V)` The cell (`X`, `Y`) has an initial value of `V`'] |

## Facts
Showing all facts

| **Signature** | **Location** | **Doc** |
|---------------|--------------|---------|
| val/1 | Line; 6 | [] |

## Rules
Showing all rules

| **Signature** | **Depends** | **Location** | **Doc** |
|---------------|-------------|--------------|---------|
| pos/2 | val/1 | Line; 7 | [] |
| subgrid/3 | pos/2 | Line; 10 | [' `subgrid(X,Y,S)` The cell (`X`, `Y`) is in subgrid `S`'] |
| sudoku/3 | val/1 pos/2 | Line; 13 | [' `sudoku(X,Y,V)` The cell (`X`, `Y`) has value `V` with `0<V<=dim*dim`'] |
| sudoku/3 | instance/3 | Line; 22 | [] |

## Constraints
Showing all constraints 

| **Signature** | **Dependencies** | **Location** | **Doc** |
|---------------|------------------|--------------|---------|
| constraint#0 | sudoku/3 | Line; 16 | [" Can't repeat values per row"] |
| constraint#1 | sudoku/3 | Line; 18 | [" Can't repeat values per column"] |
| constraint#2 | sudoku/3 subgrid/3 | Line; 20 | [" Can't repeat values per subgrid"] |

## Outputs
Showing all outputs 

| **Signature** | **Location** | **Doc** |
|---------------|--------------|---------|
| sudoku/3 | Line; 24 | [] |


![Definition Dependency Graph](DefinitionDependencyGraph.png)
![Rule Dependency Graph](RuleDependencyGraph.png)