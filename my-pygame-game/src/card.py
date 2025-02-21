import json
import os
from abc import ABC, abstractmethod

# Base Card Class
class Card(ABC):
    def __init__(self, name, value, image_path):
        self.name = name
        self.value = value
        self.image_path = image_path

    @abstractmethod
    def use(self, target):
        pass

    def __str__(self):
        return f"{self.name} ({self.value})"

# Card Types
class AttackCard(Card):
    def use(self, target):
        target.health -= self.value
        print(f"{self.name} used on {target}. Damage: {self.value}")

class HealCard(Card):
    def use(self, target):
        target.health += self.value
        print(f"{self.name} used on {target}. Heal: {self.value}")

class ShieldCard(Card):
    def use(self, target):
        target.shield += self.value
        print(f"{self.name} used on {target}. Shield: {self.value}")

# Factory Class
class CardFactory:
    _card_types = {}

    @classmethod
    def register_card(cls, card_type, card_class):
        cls._card_types[card_type] = card_class

    @classmethod
    def create_card(cls, card_type, name, value, image_path="default.png"):
        if card_type not in cls._card_types:
            raise ValueError(f"Card type '{card_type}' is not registered.")
        # Ensure the image path is relative to the assets/Kartice directory
        if not image_path.startswith('my-pygame-game/src/assets/Kartice'):
            image_path = os.path.join('my-pygame-game/src/assets/Kartice', image_path)
        return cls._card_types[card_type](name, value, image_path)

# Register card types
CardFactory.register_card("attack", AttackCard)
CardFactory.register_card("heal", HealCard)
CardFactory.register_card("shield", ShieldCard)

# Function to load cards from JSON file
def load_cards_from_json(file_path):
    with open(file_path, 'r') as file:
        card_data = json.load(file)
    cards = []
    for card_info in card_data:
        card_type = card_info['type']
        name = card_info['name']
        value = card_info['value']
        image_path = card_info.get('image_path', 'default.png')  # Provide a placeholder image path if missing
        card = CardFactory.create_card(card_type, name, value, image_path)
        cards.append(card)
    return cards

# Function to get predefined cards
def get_predefined_cards():
    return [
        CardFactory.create_card("attack", "Fireball", 5, "fireball.png"),
        CardFactory.create_card("heal", "Health Potion", 3, "health_potion.png"),
        CardFactory.create_card("shield", "Wooden Shield", 2, "wooden_shield.png"),
        CardFactory.create_card("shield", "Iron Shield", 4, "iron_shield.png"),
        CardFactory.create_card("attack", "Sword", 6, "sword.png"),
        CardFactory.create_card("attack", "Spear", 4, "spear.png"),
        CardFactory.create_card("attack", "Rock", 1, "rock.png"),
        CardFactory.create_card("heal", "Kebab", 2, "kebab.png")
    ]

# Example Usage (for debugging)
if __name__ == "__main__":
    # Use a relative path to the saved_cards.json file
    current_dir = os.path.dirname(__file__)
    json_path = os.path.join(current_dir, '..', '..', 'saved_cards.json')
    cards = load_cards_from_json(json_path)
    for card in cards:
        print(card)

