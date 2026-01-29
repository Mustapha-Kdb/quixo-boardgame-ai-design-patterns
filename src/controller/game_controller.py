import pygame
import sys
from manager_singleton.game_manager import GameManager
from view.game_view import GameView

class GameController:
    def __init__(self, game_view: GameView):
        self.game_view = game_view
        self.gm = GameManager()

        # move_step =1 --> phase de selection par default 
        self.move_step = 1
        self.selected_cell = None
        self.possible_insertions = []

        self.winner = None  
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.game_over:
                continue

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = self.get_cell_from_mouse(x, y)
                if row is None or col is None:
                    continue

                board = self.gm.board
                current_player = self.gm.get_current_player()

                # phase de selection
                if self.move_step == 1:
                    if board.can_select(row, col, current_player.symbol):
                        self.selected_cell = (row, col)
                        self.possible_insertions = self.get_possible_insertion_cells(row, col)
                        self.move_step = 2

                # phase de mouvement
                else:
                    if (row, col) in self.possible_insertions:
                        from_r, from_c = self.selected_cell
                        to_r, to_c = (row, col)
                        symbol = current_player.symbol

                        success = board.apply_move(from_r, from_c, to_r, to_c, symbol)
                        if success:
                            winner = board.check_winner()
                            if winner:
                                self.winner = winner
                                self.game_over = True
                            else:
                                self.gm.next_player()

                        # reset vers la phase de selection
                        self.move_step = 1
                        self.selected_cell = None
                        self.possible_insertions = []

    def update(self):
        pass

    def render(self):

        # reinitialiser l’ecran
        self.game_view.clear_screen()

        # afficher le board
        self.game_view.render_board(self.gm.board)

        if not self.game_over:
            board = self.gm.board
            current_symbol = self.gm.get_current_player().symbol

            if self.move_step == 1:
                # cases sélectionnables (phase de selection)
                for r in range(board.ROWS):
                    for c in range(board.COLS):
                        if board.can_select(r, c, current_symbol):
                            self.game_view.highlight_cell(r, c, (255,165,0,60)) 
            else:
                # insertion possible (phase de mouvement)
                for (r, c) in self.possible_insertions:
                    self.game_view.highlight_cell(r, c, (255,140,0,120))
        else:
            # afficher le gagnant
            if self.winner:
                font = pygame.font.SysFont(None, 48)
                msg = f"Le gagnant est {self.winner} !"
                text_surface = font.render(msg, True, (255, 140, 0))
                rect = text_surface.get_rect(center=(
                    self.game_view.screen_width//2,
                    self.game_view.screen_height//2
                ))
                self.game_view.screen.blit(text_surface, rect)

        # update
        self.game_view.update_display()

    def get_cell_from_mouse(self, x, y):
        # convertir (x,y) en (row,col)
        cell_size = self.game_view.cell_size
        row = y // cell_size
        col = x // cell_size
        if 0 <= row < 5 and 0 <= col < 5:
            return row, col
        return None, None

    def get_possible_insertion_cells(self, row, col):

        # bords gauche, droit, haut, bas de meme ligne avec exclus de la case choisie
        board = self.gm.board
        edges = [
            (row, 0),
            (row, board.COLS-1),
            (0, col),
            (board.ROWS-1, col)
        ]
        unique_edges = list(set(edges))
        if (row, col) in unique_edges:
            unique_edges.remove((row, col))
        return unique_edges
