class Board:

    ROWS = 5
    COLS = 5

    # init
    def __init__(self):
        
        self.grid = [[' ' for _ in range(self.COLS)] for _ in range(self.ROWS)]

    def reset_board(self):
        self.grid = [[' ' for _ in range(self.COLS)] for _ in range(self.ROWS)]

    def is_on_edge(self, row, col):
        return (
            row == 0 
            or row == self.ROWS - 1
            or col == 0
            or col == self.COLS - 1
        )

    # selection possible si case sur bord + case vide ou deja au symbole du joueur
    def can_select(self, row, col, symbol):

        if not self.is_on_edge(row, col):
            return False
        return (self.grid[row][col] == ' ' or self.grid[row][col] == symbol)

    def apply_move(self, from_row, from_col, to_row, to_col, symbol):

        # marquer la case d’origine au symbole
        self.grid[from_row][from_col] = symbol

        # verif qu’on est dans la même ligne ou colonne
        if from_row != to_row and from_col != to_col:
            print("Mouvement invalide (pas la même ligne ou colonne).")
            return False

        # sauvegarder le pion
        saved_cube = self.grid[from_row][from_col]
        # vider la case source
        self.grid[from_row][from_col] = ' '

        # décalage des cases
        if from_row == to_row:
            # décal horizontal
            row = from_row
            if to_col < from_col:
                # droite -> gauche
                for c in range(from_col - 1, to_col - 1, -1):
                    self.grid[row][c+1] = self.grid[row][c]
                self.grid[row][to_col] = saved_cube
            else:
                # gauche -> droite
                for c in range(from_col + 1, to_col + 1):
                    self.grid[row][c-1] = self.grid[row][c]
                self.grid[row][to_col] = saved_cube
        else:
            # décal vertical
            col = from_col
            if to_row < from_row:
                # bas -> haut
                for r in range(from_row - 1, to_row - 1, -1):
                    self.grid[r+1][col] = self.grid[r][col]
                self.grid[to_row][col] = saved_cube
            else:
                # haut -> bas
                for r in range(from_row + 1, to_row + 1):
                    self.grid[r-1][col] = self.grid[r][col]
                self.grid[to_row][col] = saved_cube

        return True

    def check_winner(self):

        lines = []

        # rows
        for r in range(self.ROWS):
            lines.append(self.grid[r])
        # cols
        for c in range(self.COLS):
            col_vals = [self.grid[r][c] for r in range(self.ROWS)]
            lines.append(col_vals)
        # diags
        diag1 = [self.grid[i][i] for i in range(self.ROWS)]
        diag2 = [self.grid[i][self.ROWS - 1 - i] for i in range(self.ROWS)]
        lines.append(diag1)
        lines.append(diag2)

        for line in lines:
            if line.count('X') == 5:
                return 'X'
            if line.count('O') == 5:
                return 'O'
        return None
