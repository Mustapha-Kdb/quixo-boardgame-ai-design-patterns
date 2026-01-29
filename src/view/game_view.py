import pygame

class GameView:

    def __init__(self, screen_width=500, screen_height=500):
        self.screen_width = screen_width
        self.screen_height = screen_height
        # taille des cases
        self.cell_size = 100  


        self.background_color = (255, 140, 0)
        self.line_color = (0, 0, 0)

        self.screen = None

    def init_display(self):

        # initialisation de la fenêtre
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Quixo")
        return self.screen

    def clear_screen(self):

        if self.screen:
            self.screen.fill((255, 255, 255))

    # afficher le board
    def render_board(self, board):

        if not self.screen:
            return

        rows = board.ROWS
        cols = board.COLS

        for r in range(rows):
            for c in range(cols):
                rect = (c*self.cell_size, r*self.cell_size, self.cell_size, self.cell_size)
                # dessiner bordure
                pygame.draw.rect(self.screen, self.line_color, rect, width=2)

                # dessiner la case si la case n’est pas vide
                symbol = board.grid[r][c]
                if symbol != ' ':
                    color = (0, 0, 0) if symbol == 'X' else (255, 0, 0)
                    font = pygame.font.SysFont(None, 72)
                    text_surface = font.render(symbol, True, color)
                    text_rect = text_surface.get_rect(
                        center=(c*self.cell_size + self.cell_size//2,
                                r*self.cell_size + self.cell_size//2))
                    self.screen.blit(text_surface, text_rect)

    def highlight_cell(self, row, col, rgba):

        if not self.screen:
            return
        highlight_surf = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
        highlight_surf.fill(rgba)
        self.screen.blit(highlight_surf, (col*self.cell_size, row*self.cell_size))

    def update_display(self):
        pygame.display.flip()
