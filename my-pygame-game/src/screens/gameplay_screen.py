import pygame
import random
from enemy import EnemyFactory  # Import Enemy Factory

class GameplayScreen:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.stage = 1  # Start at stage 1
        self.enemy = self.create_enemy()  # Initialize first enemy

        # Load background
        self.background = pygame.image.load('my-pygame-game/src/assets/game_bg.png')
        self.background = pygame.transform.scale(self.background, (self.game.screen.get_width(), self.game.screen.get_height()))

    def handle_events(self):
        """Handle events for the gameplay screen."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            # Add more event handling as needed

    def update(self):
        """Update game logic here (e.g., check for enemy defeat)."""
        if self.enemy.health <= 0:
            print(f"Enemy defeated! Moving to stage {self.stage + 1}")
            self.stage += 1
            self.enemy = self.create_enemy()  # Create a new enemy for the next stage

    def draw(self, screen):
        """Draw gameplay elements on the screen."""
        screen.blit(self.background, (0, 0))  # Draw the background

        # Draw player
        screen.blit(self.player.image, self.player.rect)

        # Draw enemy
        self.enemy.draw(screen)  # Use the enemy's draw method

        # Draw HP and stage tracker
        font = pygame.font.Font(None, 36)
        hp_text = font.render(f"HP: {self.player.health}", True, (255, 255, 255))
        stage_text = font.render(f"Stage: {self.stage}", True, (255, 255, 255))
        screen.blit(hp_text, (10, 10))
        screen.blit(stage_text, (10, 50))

        pygame.display.flip()

    def create_enemy(self):
        """Randomly create a new enemy for the next stage."""
        enemy_type = random.randint(1, 4)  # Random enemy type
        return EnemyFactory.create_enemy(enemy_type, 700, 300, speed=0)

    def run(self):
        """Main loop for gameplay."""
        while self.game.running:
            self.handle_events()
            self.update()
            self.draw(self.game.screen)