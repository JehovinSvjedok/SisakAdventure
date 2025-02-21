import pygame
import random
import os
import time
from enemy import EnemyFactory, BossEnemy  # Import BossEnemy and EnemyFactory
from card import CardFactory, load_cards_from_json, AttackCard, HealCard, ShieldCard  # Import CardFactory, load_cards_from_json, AttackCard, HealCard, ShieldCard

class GameplayScreen:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.player.image = pygame.transform.scale(self.player.image, (350, 350))  # Increase player size
        self.player.rect = self.player.image.get_rect()
        self.player.rect.bottom = self.game.screen.get_height()  # Position player at the bottom
        self.player.rect.x = 100  # Position player on the left side
        self.round = 1  # Start at round 1
        self.max_rounds = 5  # Total number of rounds before boss
        self.enemy = self.create_enemy()  # Initialize first enemy
        self.player_turn = True  # Track whose turn it is
        self.action_text = ""  # Text to display the actions
        self.action_color = (255, 255, 255)  # Color for the action text
        self.initial_health = player.health  # Store the initial health of the player

        # Load background
        self.background = pygame.image.load('my-pygame-game/src/assets/game_bg.png')
        self.background = pygame.transform.scale(self.background, (self.game.screen.get_width(), self.game.screen.get_height()))

        # Load cards from JSON file
        current_dir = os.path.dirname(__file__)
        json_path = os.path.join(current_dir, '..', '..', '..', 'saved_cards.json')
        self.cards = load_cards_from_json(json_path)
        self.selected_card = None

        # Load card images
        self.card_images = []
        self.card_rects = []
        self.original_card_sizes = []
        for card in self.cards:
            try:
                card_image = pygame.image.load(card.image_path)
            except pygame.error:
                print(f"Warning: Image for {card.name} not found at {card.image_path}. Using default image.")
                card_image = pygame.image.load('my-pygame-game/src/assets/Kartice/default.png')  # Use placeholder image if not found
            card_image = pygame.transform.scale(card_image, (150, 225))  # Resize card image
            self.card_images.append(card_image)
            self.card_rects.append(card_image.get_rect())
            self.original_card_sizes.append(card_image.get_size())

    def handle_events(self):
        """Handle events for the gameplay screen."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN and self.player_turn:
                if event.key == pygame.K_e:
                    self.attack_enemy()
            elif event.type == pygame.MOUSEBUTTONDOWN and self.player_turn:
                mouse_pos = event.pos
                for i, card_rect in enumerate(self.card_rects):
                    if card_rect.collidepoint(mouse_pos):
                        self.use_card(i)
                        break
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_hover(event.pos)

    def handle_mouse_hover(self, mouse_pos):
        """Handle mouse hover over cards."""
        for i, card_rect in enumerate(self.card_rects):
            if card_rect.collidepoint(mouse_pos):
                card_image = pygame.transform.scale(self.card_images[i], (170, 255))  # Enlarge card image
                self.card_images[i] = card_image
                self.card_rects[i] = card_image.get_rect(topleft=card_rect.topleft)
            else:
                card_image = pygame.transform.scale(self.card_images[i], self.original_card_sizes[i])  # Reset card image size
                self.card_images[i] = card_image
                self.card_rects[i] = card_image.get_rect(topleft=card_rect.topleft)

    def update(self):
        """Update game logic here (e.g., check for enemy defeat)."""
        if self.enemy.health <= 0:
            if isinstance(self.enemy, BossEnemy):
                self.win_game()
            else:
                print(f"Enemy defeated! Moving to round {self.round + 1}")
                self.round += 1
                if self.round < self.max_rounds:
                    self.enemy = self.create_enemy()  # Create a new enemy for the next round
                else:
                    self.enemy = self.create_boss()  # Spawn boss in the final round

        if self.player.health <= 0:
            self.lose_game()

        if not self.player_turn:
            self.enemy_turn()

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
        shield_text = font.render(f"Shield: {self.player.shield}", True, (0, 255, 255))
        round_text = font.render(f"Round: {self.round}", True, (255, 255, 255))
        enemy_hp_text = font.render(f"Enemy HP: {self.enemy.health}", True, (255, 0, 0))

        screen.blit(hp_text, (10, 10))
        screen.blit(shield_text, (10, 50))
        screen.blit(round_text, (10, 90))
        screen.blit(enemy_hp_text, (self.game.screen.get_width() - 200, 10))

        # Draw cards
        screen_width = self.game.screen.get_width()
        total_card_width = len(self.card_images) * 150 + (len(self.card_images) - 1) * 10
        start_x = (screen_width - total_card_width) // 2
        for i, card_image in enumerate(self.card_images):
            card_rect = self.card_rects[i]
            card_rect.topleft = (start_x + i * 160, 130)
            screen.blit(card_image, card_rect)

        # Draw action text at the top
        action_text = font.render(self.action_text, True, self.action_color)
        screen.blit(action_text, (self.game.screen.get_width() // 2 - action_text.get_width() // 2, 10))

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
        enemy = EnemyFactory.create_enemy(enemy_type, 700, 300, speed=random.randint(1, 3))
        enemy.rect = enemy.image.get_rect()  # Ensure the rect is set correctly
        enemy.rect.bottom = self.game.screen.get_height()  # Position enemy at the bottom
        enemy.rect.x = self.game.screen.get_width() - 250  # Position enemy on the right side
        return enemy

    def create_boss(self):
        """Create a boss enemy for the final round."""
        boss_data = EnemyFactory.BOSS_ENEMY_DATA["boss"]
        image_path, size = boss_data
        boss = BossEnemy(700, 300, speed=1, image_path=image_path, size=size, health=100)  # Boss with custom stats
        boss.rect = boss.image.get_rect()  # Ensure the rect is set correctly
        boss.rect.bottom = self.game.screen.get_height()  # Position boss at the bottom
        boss.rect.x = self.game.screen.get_width() - 250  # Position boss on the right side
        return boss

    def attack_enemy(self):
        """Reduce enemy health when attacking."""
        damage = random.randint(5, 15)  # Random damage value
        self.enemy.health -= damage
        self.action_text = f"Player attacked! Damage: {damage}"
        self.action_color = (255, 255, 255)  # White color for player actions
        print(f"Attacked enemy! Damage: {damage}, Enemy HP: {self.enemy.health}")
        self.player_turn = False  # End player's turn
        self.wait_and_enemy_turn()

    def use_card(self, card_index):
        """Use a card from the player's hand."""
        if 0 <= card_index < len(self.cards):
            card = self.cards[card_index]
            if isinstance(card, AttackCard):
                card.use(self.enemy)
                self.action_text = f"Player used {card.name}! Damage: {card.value}"
            elif isinstance(card, HealCard):
                card.use(self.player)
                self.action_text = f"Player used {card.name}! Heal: {card.value}"
            elif isinstance(card, ShieldCard):
                card.use(self.player)
                self.action_text = f"Player used {card.name}! Shield: {card.value}"
            self.action_color = (255, 255, 255)  # White color for player actions
            print(f"Used card: {card.name}")
            self.player_turn = False  # End player's turn
            self.wait_and_enemy_turn()

    def wait_and_enemy_turn(self):
        """Wait for 2 seconds and then let the enemy take its turn."""
        self.draw(self.game.screen)  # Update the screen to show the player's action
        pygame.display.flip()
        pygame.time.wait(1000)  # Wait for 2 seconds
        self.enemy_turn()

    def enemy_turn(self):
        """Handle the enemy's turn."""
        action = random.choice(["attack", "heal"])
        if action == "attack":
            damage = random.randint(5, 15)  # Random damage value
            if self.player.shield > 0:
                if damage > self.player.shield:
                    remaining_damage = damage - self.player.shield
                    self.player.shield = 0
                    self.player.health -= remaining_damage
                else:
                    self.player.shield -= damage
                    damage = 0
            else:
                self.player.health -= damage
            self.action_text = f"Enemy attacked! Damage: {damage}"
            self.action_color = (255, 0, 0)  # Red color for enemy actions
            print(f"Enemy attacked! Damage: {damage}, Player HP: {self.player.health}")
        elif action == "heal":
            heal_amount = 5  # Fixed heal value
            self.enemy.health += heal_amount
            self.action_text = f"Enemy healed! Heal: {heal_amount}"
            self.action_color = (255, 0, 0)  # Red color for enemy actions
            print(f"Enemy healed! Heal: {heal_amount}, Enemy HP: {self.enemy.health}")
        self.player_turn = True  # End enemy's turn

    def lose_game(self):
        """Handles the loss condition (when player's health reaches 0)."""
        # Display loss message
        font = pygame.font.Font(None, 60)
        lose_text = font.render("You Lose!", True, (255, 0, 0))
        self.game.screen.blit(lose_text, (self.game.screen.get_width() // 2 - 100, self.game.screen.get_height() // 2))
        pygame.display.flip()

        pygame.time.wait(2000)  # Wait for 2 seconds to show the loss message

        # Reset player's health to initial value
        self.player.health = self.initial_health

        # After losing, switch back to the starting area screen
        from screens.starting_area_screen import StartingAreaScreen
        self.game.change_screen(StartingAreaScreen(self.game, self.game.selected_player))  # Switch back to StartingAreaScreen

    def run(self):
        """Main loop for gameplay."""
        while self.game.running:
            self.handle_events()
            self.update()
            self.draw(self.game.screen)