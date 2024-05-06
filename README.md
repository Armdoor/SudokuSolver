# SudokuSolver

Sudoku Solver Sudoku is a logic-based combinatorial number-placement puzzle. The code implements two algorithms to solve Sudoku puzzles:

AC-3 Algorithm: This algorithm enforces arc consistency and propagates constraints to reduce the domain size of variables by ensuring the consistency of assignments. It iteratively removes values from the domain of variables based on constraints until a solution is found or it determines that no solution exists. Backtracking with Minimum Remaining Values (MRV) Heuristic: This algorithm recursively searches for a solution by assigning values to empty cells and backtracking when a solution is not valid. It selects the next cell to be assigned a value based on the MRV heuristic, which prioritizes cells with the fewest remaining valid values. We have included a set of predefined Sudoku puzzles stored as lists of lists. The main block allows the user to choose a puzzle to solve interactively by inputting a number between 1 and 100.

Group members: Ju Won Kim, Matt Coley, Avni Gulrajani, Sue Kim, Aarambh Sanoria 


Try the solver: 
https://colab.research.google.com/drive/1NVO3W0-mAX2bLB0z7dQzW-2prCUO3E9j?authuser=2#scrollTo=BC_PXwqquUL7
