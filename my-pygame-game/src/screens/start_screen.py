import pygame

class StartScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 74)
        self.title = self.font.render("My Game", True, (255, 255, 255))
        self.start_text = pygame.font.Font(None, 50).render("Press Enter to Start", True, (255, 255, 255))
        self.background = pygame.image.load("my-pygame-game/src/assets/main_bg.png")  # Ensure this file exists!

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                from screens.choose_player_screen import ChoosePlayerScreen
                self.game.change_screen(ChoosePlayerScreen(self.game))  # Switch screen

    def update(self):
        pass  # No animations yet, but can be used later

    def draw(self, screen):
        screen.blit(self.background, (0, 0))  # Draw the background
        screen.blit(self.title, (screen.get_width() // 2 - self.title.get_width() // 2, 100))
        screen.blit(self.start_text, (screen.get_width() // 2 - self.start_text.get_width() // 2, 300))
