import pygame
import random
from enemy import EnemyFactory, BossEnemy  # Import BossEnemy and EnemyFactory

class GameplayScreen:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.round = 1  # Start at round 1
        self.max_rounds = 5  # Total number of rounds before boss
        self.enemy = self.create_enemy()  # Initialize first enemy

        # Load background
        self.background = pygame.image.load('my-pygame-game/src/assets/game_bg.png')
        self.background = pygame.transform.scale(self.background, (self.game.screen.get_width(), self.game.screen.get_height()))

    def handle_events(self):
        """Handle events for the gameplay screen."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.attack_enemy()

    def update(self):
        """Update game logic here (e.g., check for enemy defeat)."""
        if self.enemy.health <= 0:
            if isinstance(self.enemy, BossEnemy):
                self.win_game()
                self.game.running = False  # Stop the game loop
            else:
                print(f"Enemy defeated! Moving to round {self.round + 1}")
                self.round += 1
                if self.round < self.max_rounds:
                    self.enemy = self.create_enemy()  # Create a new enemy for the next round
                else:
                    self.enemy = self.create_boss()  # Spawn boss in the final round

    def draw(self, screen):
        """Draw gameplay elements on the screen."""
        screen.blit(self.background, (0, 0))  # Draw the background

        # Draw player
        screen.blit(self.player.image, self.player.rect)

        # Draw enemy
        self.enemy.draw(screen)  # Use the enemy's draw method

        # Draw HP and round tracker
        font = pygame.font.Font(None, 36)
        hp_text = font.render(f"HP: {self.player.health}", True, (255, 255, 255))
        round_text = font.render(f"Round: {self.round}", True, (255, 255, 255))
        enemy_hp_text = font.render(f"Enemy HP: {self.enemy.health}", True, (255, 0, 0))

        screen.blit(hp_text, (10, 10))
        screen.blit(round_text, (10, 50))
        screen.blit(enemy_hp_text, (self.game.screen.get_width() - 200, 10))

        pygame.display.flip()

    def win_game(self):
        """Handles the win condition (after defeating the final boss)."""
        # Display victory message
        font = pygame.font.Font(None, 60)
        win_text = font.render("You Win!", True, (0, 255, 0))
        self.game.screen.blit(win_text, (self.game.screen.get_width() // 2 - 100, self.game.screen.get_height() // 2))
        pygame.display.flip()

        pygame.time.wait(2000)  # Wait for 2 seconds to show the victory message
        
        # After winning, switch back to the starting area screen
        
        from screens.starting_area_screen import StartingAreaScreen
        self.game.change_screen(StartingAreaScreen(self.game, self.game.selected_player))  # Switch back to StartingAreaScreen

    def create_enemy(self):
        """Randomly create a normal enemy."""
        enemy_type = random.randint(1, 3)  # Random enemy type
        return EnemyFactory.create_enemy(enemy_type, 700, 300, speed=random.randint(1, 3))

    def create_boss(self):
        """Create a boss enemy for the final round."""
        boss_data = EnemyFactory.BOSS_ENEMY_DATA["boss"]
        image_path, size = boss_data
        return BossEnemy(700, 300, speed=1, image_path=image_path, size=size, health=100)  # Boss with custom stats

    def attack_enemy(self):
        """Reduce enemy health when attacking."""
        damage = random.randint(5, 15)  # Random damage value
        self.enemy.health -= damage
        print(f"Attacked enemy! Damage: {damage}, Enemy HP: {self.enemy.health}")

    def run(self):
        """Main loop for gameplay."""
        while self.game.running:
            self.handle_events()
            self.update()
            self.draw(self.game.screen)
