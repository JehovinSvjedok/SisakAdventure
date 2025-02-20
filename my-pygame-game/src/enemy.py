import pygame

class Enemy:
    def __init__(self, x, y, speed, image_path, size, health=10):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = self.load_image(image_path, size)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = health

    def load_image(self, path, size):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)

    def update(self):
        pass  # No movement for enemies

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0  # Return whether the enemy is slain

# Example Enemy Types with specific attributes
class EnemyType1(Enemy):
    def update(self):
        # Implement movement or behavior for EnemyType1
        pass

class EnemyType2(Enemy):
    def update(self):
        # Implement movement or behavior for EnemyType2
        pass

class EnemyType3(Enemy):
    def update(self):
        # Implement movement or behavior for EnemyType3
        pass

class EnemyType4(Enemy):
    def update(self):
        # Implement movement or behavior for EnemyType4
        pass

class EnemyFactory:
    # Mapping enemy types to their respective parameters
    ENEMY_DATA = {
        1: ("my-pygame-game/src/assets/goblin_koplje.png", (200, 270)),
        2: ("my-pygame-game/src/assets/goblin.png", (200, 270)),
        3: ("my-pygame-game/src/assets/mali_skeleton.png", (200, 270)),
        4: ("my-pygame-game/src/assets/skeleton_dragon.png", (300, 300)),
    }

    @staticmethod
    def create_enemy(enemy_type, x, y, speed):
        if enemy_type in EnemyFactory.ENEMY_DATA:
            image_path, size = EnemyFactory.ENEMY_DATA[enemy_type]
            return Enemy(x, y, speed, image_path, size, health=10)  # Set default health to 10
        else:
            raise ValueError("Unknown enemy type")
