class SudokuSolver:
    def __init__(self):
        self.puzzle_size = 9

    def print_puzzle(self, puzzle):
        for i in range(self.puzzle_size):
            if i % 3 == 0 and i != 0:
                print("-" * 21)

            for j in range(self.puzzle_size):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")

                if j == self.puzzle_size - 1:
                    print(puzzle[i][j])
                else:
                    print(puzzle[i][j], end=" ")

    # ------ AC3 algorithm start ------ #
    # AC-3 algorithm - enforces arc consistency and propagates constraints
    # Reduces the domain size of variables by ensuring the consistency of assignments
    def apply_ac3(self, puzzle):
        queue = self.generate_arcs(puzzle)

        # x and y represent two cells that are part of arc (pair connected by constraints)
        while queue:
            x, y = queue.pop(0)

            if self.remove(puzzle, x, y):
                x_domain = puzzle[x[0]][x[1]] 

                # Check if domain is empty
                if len(x_domain) == 0 and isinstance(x_domain, list):
                    # If empty, no solution is found
                    return False  
                for neighbor in self.get_neighbors(x):
                    if neighbor != y:
                        queue.append((neighbor, x))

        return True
    
    # Returns all cells in the same row, column, and subgrid (Does not include itself)
    def get_neighbor_cells(self, cell):
        neighbor_cells = []
        row, col = cell

        for i in range(self.puzzle_size):
            if i != row:
                neighbor_cells.append((i, col))
            if i != col:
                neighbor_cells.append((row, i))

        sub_row = (row // 3) * 3
        sub_col = (col // 3) * 3

        for r in range(sub_row, sub_row + 3):
            for c in range(sub_col, sub_col + 3):
                if (r, c) != cell:
                    neighbor_cells.append((r, c))
                    
        return neighbor_cells

    # Generates all posisble arcs - variable pairs
    def generate_arcs(self, puzzle):
        arcs = []

        for i in range(self.puzzle_size):
            for j in range(self.puzzle_size):
                for adjacent in self.get_neighbor_cells((i, j)):
                    arcs.append(((i, j), adjacent))

        return arcs

    # Removes values from domain of x that are not consistent with domain of y
    def remove(self, puzzle, x, y):
        removed = False
        x_domain = puzzle[x[0]][x[1]]

        if isinstance(x_domain, int):
            # If domain has single value, return false
            return removed  

        # Iterating over the copy of the domain
        for z1 in x_domain[:]: 
            consitent = False

            for z2 in puzzle[y[0]][y[1]]:
                if z1 != z2:
                    consitent = True
                    break

            if not consitent:
                x_domain.remove(z1)
                removed = True

        return removed
    
    # ------ AC3 algorithm end ------ #

    # ------ Backtracking with MRV ------- #
    # Checks if assigning a value at (row, col) violates the constraints
    def constraint_check(self, row, col, val, puzzle):
        # Check the row to see if the number exists
        if val in puzzle[row]:
            return False

        # Check the column to see if the number exists
        if any(val == puzzle[i][col] for i in range(self.puzzle_size)):
            return False

        # Check the subgrid to see if the number exists
        sub_row = (row // 3) * 3
        sub_col = (col // 3) * 3

        for r in range(sub_row, sub_row + 3):
            for c in range(sub_col, sub_col + 3):
                if puzzle[r][c] == val:
                    return False
                
        return True
    
    # Returns the possible valid values for (row, col)
    # Numbers that already exist in the same row, col, subgrid are removed
    def get_domain(self, row, col, puzzle):
        domain = set(range(1, 10))

        for i in range(self.puzzle_size):
            # Remove number from domain if it exists in the same row
            domain.discard(puzzle[row][i])
            # Remove number from domain if it exists in the same column  
            domain.discard(puzzle[i][col])  

        sub_row = (row // 3) * 3
        sub_col = (col // 3) * 3

        for r in range(sub_row, sub_row + 3):
            for c in range(sub_col, sub_col + 3):
                # Remove number from domain if it exists in the same subgrid
                domain.discard(puzzle[r][c])  

        return sorted(list(domain))

    # Iterate through each cell to find an empty cell
    # Used in backtracking to selct next cell to be assigned a value
    def search_empty_cell(self, puzzle):
        for row in range(self.puzzle_size):
            for col in range(self.puzzle_size):
                if puzzle[row][col] == 0:
                    return (row, col)
                
        return None

    # Solves the puzzle using backtracking with MRV heuristic
    # Recursively searches for a solution. Assigns values to empty cells and backtracks when solution is not valid
    def solve_puzzle(self, puzzle):
        empty_cell = self.search_empty_cell(puzzle)

        # Solution found - no empty cells left
        if not empty_cell:
            return True

        # Find the next empty cell to assign a value to
        row, col = empty_cell

        # Sort values for the current cell based on MRV heuristic
        sorted_values = self.get_domain(row, col, puzzle)

        for num in sorted_values:
            if self.constraint_check(row, col, num, puzzle):
                puzzle[row][col] = num

                if self.solve_puzzle(puzzle):
                    return True
                
                puzzle[row][col] = 0  
        return False
    
    # ------ Backtracking with MRV ------- #

    # Solves and prints the puzzles
    def solve(self, puzzle):
        print("Selected Puzzle:")
        self.print_puzzle(puzzle)
        
        print()
        print("...")
        print()

        # Uses AC-3 algorithm
        self.apply_ac3(puzzle)

        # Puzzle is solved using backtracking with MRV heuristic
        self.solve_puzzle(puzzle)

        print("Solved Puzzle:")
        self.print_puzzle(puzzle)
        return puzzle


if __name__ == "__main__":
    puzzles = [
        [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ],

        [
            [0, 9, 3, 0, 7, 4, 0, 0, 5],
            [5, 0, 0, 8, 0, 0, 0, 9, 1],
            [8, 0, 7, 1, 0, 0, 0, 4, 3],
            [0, 0, 9, 0, 0, 1, 5, 8, 6],
            [0, 0, 2, 0, 0, 5, 4, 0, 0],
            [3, 5, 8, 0, 0, 7, 0, 1, 0],
            [4, 3, 0, 0, 0, 8, 6, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [9, 8, 1, 0, 0, 2, 3, 7, 0]
        ],

        [
            [0, 7, 9, 6, 0, 5, 2, 0, 3],
            [1, 0, 0, 0, 0, 0, 0, 5, 0],
            [5, 3, 8, 2, 1, 0, 4, 7, 0],
            [7, 0, 6, 0, 0, 0, 0, 0, 4],
            [0, 0, 0, 4, 0, 0, 0, 2, 5],
            [0, 4, 5, 9, 0, 0, 0, 8, 7],
            [0, 1, 0, 0, 6, 0, 7, 4, 2],
            [0, 8, 7, 0, 4, 0, 0, 9, 0],
            [2, 5, 4, 0, 0, 0, 0, 0, 0]
        ],

        [
            [0, 4, 5, 8, 7, 0, 0, 0, 6],
            [0, 2, 6, 0, 4, 0, 0, 0, 1],
            [0, 9, 0, 2, 5, 6, 4, 0, 0],
            [9, 0, 0, 4, 0, 0, 5, 6, 0],
            [2, 0, 4, 6, 0, 0, 0, 0, 0],
            [0, 8, 0, 0, 0, 0, 3, 0, 0],
            [0, 0, 9, 1, 3, 2, 6, 8, 0],
            [1, 6, 0, 0, 0, 8, 0, 3, 4],
            [0, 0, 8, 0, 0, 4, 2, 1, 0]
        ],

        [
            [5, 0, 3, 0, 0, 4, 6, 7, 0],
            [0, 9, 0, 2, 5, 0, 8, 3, 1],
            [0, 0, 2, 6, 0, 3, 0, 0, 9],
            [0, 2, 0, 3, 7, 0, 0, 1, 5],
            [0, 0, 8, 0, 2, 0, 7, 6, 0],
            [3, 0, 0, 5, 6, 0, 0, 0, 0],
            [4, 6, 0, 0, 0, 0, 1, 0, 7],
            [2, 8, 1, 0, 4, 0, 0, 0, 0],
            [0, 0, 5, 0, 9, 0, 0, 8, 0]
        ]
    ]

    solver = SudokuSolver()

    while True:
        try:
            choice = int(input("Choose a puzzle (1~5): ".format(len(puzzles))))

            if 1 <= choice <= len(puzzles):
                solver.solve(puzzles[choice - 1])
                break
            else:
                print("Please enter a number between 1 and 5.".format(len(puzzles)))
        except ValueError:
            print("Invalid choice. Please enter a number.")