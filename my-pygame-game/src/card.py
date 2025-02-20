from abc import ABC, abstractmethod

# Base Card Class
class Card(ABC):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    @abstractmethod
    def use(self, target):
        """Each card must define its own effect."""
        pass

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name} (Value: {self.value})"

# Card Types
class AttackCard(Card):
    def use(self, target):
        target.take_damage(self.value)

class HealCard(Card):
    def use(self, target):
        target.heal(self.value)

class ShieldCard(Card):
    def use(self, target):
        target.absorb_damage(self.value)

# Factory Class
class CardFactory:
    _card_types = {}

    @staticmethod
    def register_card(card_type, card_class):
        """Registers a new card type."""
        CardFactory._card_types[card_type] = card_class

    @staticmethod
    def create_card(card_type, name, value):
        """Creates a card of the given type."""
        if card_type in CardFactory._card_types:
            return CardFactory._card_types[card_type](name, value)
        else:
            raise ValueError(f"Unknown card type: {card_type}")

# Register card types
CardFactory.register_card("attack", AttackCard)
CardFactory.register_card("heal", HealCard)
CardFactory.register_card("shield", ShieldCard)

# Function to get predefined cards
def get_predefined_cards():
    return [
        CardFactory.create_card("attack", "Fireball", 5),
        CardFactory.create_card("heal", "Health Potion", 3),
        CardFactory.create_card("shield", "Wooden Shield", 2),
        CardFactory.create_card("shield", "Iron Shield", 4),
        CardFactory.create_card("attack", "Sword", 6),
        CardFactory.create_card("attack", "Spear", 4),
        CardFactory.create_card("attack", "Rock", 1),
        CardFactory.create_card("heal", "Kebab", 2)
    ]

# Example Usage (for debugging)
if __name__ == "__main__":
    cards = get_predefined_cards()
    for card in cards:
        print(card)
