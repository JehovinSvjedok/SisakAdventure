import pygame
from player import Player
from screens.starting_area_screen import StartingAreaScreen

class ChoosePlayerScreen:
    def __init__(self, game):
        self.game = game
        self.players = [
            Player("Lule", health=80, image_path='my-pygame-game/src/assets/player1.png'),
            Player("Toni", health=120, image_path='my-pygame-game/src/assets/player2.png'),
            Player("Lovro", health=100, image_path='my-pygame-game/src/assets/player3.png')
        ]
        self.selected_player = None
        self.font = pygame.font.Font(None, 30)  # Smaller font for player text
        self.image_size = (200, 280)  # New size for player images

        # Load the background image
        self.background_image = pygame.image.load('my-pygame-game/src/assets/main_bg.png')
        self.background_image = pygame.transform.scale(self.background_image, (1200, 800))  # Scale to match screen size

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.select_player(0)
                elif event.key == pygame.K_2:
                    self.select_player(1)
                elif event.key == pygame.K_3:
                    self.select_player(2)

    def select_player(self, index):
        self.selected_player = self.players[index]
        self.game.selected_player = self.selected_player  # Store in Game class
        print(f"Selected Player: {self.selected_player.name}, Health: {self.selected_player.health}")
        self.game.change_screen(StartingAreaScreen(self.game, self.selected_player))  # Pass the selected player

    def update(self):
        pass  # No animations yet

    def draw(self, screen):
        # Draw the background
        screen.blit(self.background_image, (0, 0))

        title_text = self.font.render("Choose Your Player", True, (255, 255, 255))
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 20))

        # Calculate positioning for players
        spacing = 100  # Space between characters
        total_width = len(self.players) * self.image_size[0] + (len(self.players) - 1) * spacing
        start_x = (screen.get_width() - total_width) // 2  # Center horizontally
        start_y = 200  # Starting Y position for player images

        for index, player in enumerate(self.players):
            player_image = player.get_image()
            player_image = pygame.transform.scale(player_image, self.image_size)  # Scale to new size
            image_x = start_x + index * (self.image_size[0] + spacing)  # Calculate X position
            screen.blit(player_image, (image_x, start_y))  # Draw player image

            # Render text below each image
            text = self.font.render(f"{player.name} - Health: {player.health} (Press {index + 1})", True, (255, 255, 255))
            text_x = image_x + (self.image_size[0] - text.get_width()) // 2  # Center text below the image
            screen.blit(text, (text_x, start_y + self.image_size[1] + 5))  # Draw text below image
