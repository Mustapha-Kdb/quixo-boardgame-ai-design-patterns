import pygame
from manager_singleton.game_manager import GameManager
from view.game_view import GameView
from controller.game_controller import GameController

def main():
    pygame.init()
    clock = pygame.time.Clock()

    # créer la Vue 
    view = GameView()
    screen = view.init_display()

    # créer le Controller
    controller = GameController(view)

    # boucle de jeu
    while True:
        # le controlleur gere les evenements
        controller.handle_events()

        # update 
        controller.update()

        # on demande à la Vue d’afficher tout
        controller.render()

        clock.tick(30)


if __name__ == "__main__":
    main()
