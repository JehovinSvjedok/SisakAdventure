import pygame
from screens.start_screen import StartScreen
from screens.choose_player_screen import ChoosePlayerScreen
from screens.tavern_screen import TavernScreen
from screens.gameplay_screen import GameplayScreen
from screens.starting_area_screen import StartingAreaScreen

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("My Pygame Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.selected_player = None  # Track selected player
        self.current_screen = StartScreen(self)

    def change_screen(self, new_screen):
        """Switch to a new screen."""
        self.current_screen = new_screen

    def run(self):
        """Main game loop."""
        while self.running:
            self.current_screen.handle_events()
            self.current_screen.update()
            self.current_screen.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()