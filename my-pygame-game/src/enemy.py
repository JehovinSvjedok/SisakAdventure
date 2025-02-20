import pygame
import random

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


# Boss Enemy Class
class BossEnemy(Enemy):
    def __init__(self, x, y, speed, image_path, size, health):
        super().__init__(x, y, speed, image_path, size, health)
        self.is_boss = True  # Mark this enemy as a boss

    def update(self):
        # Special boss behavior (e.g., different movement, attack, etc.)
        pass


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
    # Mapping normal enemy types to their respective parameters
    NORMAL_ENEMY_DATA = {
        1: ("my-pygame-game/src/assets/goblin_koplje.png", (200, 270)),
        2: ("my-pygame-game/src/assets/goblin.png", (200, 270)),
        3: ("my-pygame-game/src/assets/mali_skeleton.png", (200, 270))
    }

    # Mapping boss enemy types to their respective parameters
    BOSS_ENEMY_DATA = {
        "boss": ("my-pygame-game/src/assets/skeleton_dragon.png", (400, 400))  # Add boss asset and size
    }

    @staticmethod
    def create_enemy(enemy_type, x, y, speed):
        if enemy_type in EnemyFactory.NORMAL_ENEMY_DATA:
            image_path, size = EnemyFactory.NORMAL_ENEMY_DATA[enemy_type]
            return Enemy(x, y, speed, image_path, size, health=10)  # Normal enemies
        elif enemy_type in EnemyFactory.BOSS_ENEMY_DATA:
            image_path, size = EnemyFactory.BOSS_ENEMY_DATA[enemy_type]
            return BossEnemy(x, y, speed, image_path, size, health=50)  # Boss has more health
        else:
            raise ValueError("Unknown enemy type")