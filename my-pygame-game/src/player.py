import pygame

class Player:
    def __init__(self, name, health, image_path):
        """
        Initialize a player with name and health, and load an image.

        Args:
            name (str): The name of the player.
            health (int): The health points of the player.
            image_path (str): Path to the player's image file.
        """
        self.name = name
        self.health = health
        self.image = pygame.image.load(image_path)  # Load player image
        self.image = pygame.transform.scale(self.image, (50, 50))  # Adjust size as needed
        self.rect = self.image.get_rect()

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            print("Player is dead")
            return True  # Player is dead
        return False

    def heal(self, amount):
        self.health += amount
        print(f"Player healed by {amount}. Current health: {self.health}")

    def is_alive(self):
        return self.health > 0

    def get_image(self):
        return self.image

    def absorb_damage(self, amount):
        # Implement shield logic here
        pass
