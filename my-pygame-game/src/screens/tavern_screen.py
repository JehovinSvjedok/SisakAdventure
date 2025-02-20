import json
import pygame
from card import CardFactory, get_predefined_cards

class TavernScreen:
    SAVE_FILE = "saved_cards.json"

    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 40)  # Font for title
        self.info_font = pygame.font.Font(None, 30)  # Font for instructions

        # Load background
        self.background = pygame.image.load("my-pygame-game/src/assets/tavern.jpg")
        self.background = pygame.transform.scale(self.background, (1200, 800))

        # Load cards
        self.player_cards = self.load_saved_cards()
        self.all_cards = get_predefined_cards()

        self.selected_card_index = 0
        self.selected_tavern_card_index = 0

        # Load card images
        self.card_images = self.load_card_images()

    def load_card_images(self):
        """Loads images for all predefined cards."""
        images = {}
        for card in self.all_cards:
            image_path = f"my-pygame-game/src/assets/Kartice/{card.name.lower().replace(' ', '_')}.png"
            try:
                images[card.name] = pygame.image.load(image_path)
                images[card.name] = pygame.transform.scale(images[card.name], (150, 200))  # Resize cards
            except pygame.error:
                print(f"Warning: Image for {card.name} not found at {image_path}")
                images[card.name] = None  # Use a placeholder if missing
        return images

    def load_saved_cards(self):
        try:
            with open(self.SAVE_FILE, "r") as file:
                card_data = json.load(file)
                return [CardFactory.create_card(c["type"], c["name"], c["value"]) for c in card_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return get_predefined_cards()[:4]

    def save_cards(self):
        with open(self.SAVE_FILE, "w") as file:
            json.dump(
                [{"type": card.__class__.__name__.replace("Card", "").lower(), "name": card.name, "value": card.value}
                 for card in self.player_cards],
                file
            )

    def swap_card(self):
        """Swaps selected player card with a tavern card."""
        self.player_cards[self.selected_card_index], self.all_cards[self.selected_tavern_card_index] = (
            self.all_cards[self.selected_tavern_card_index], self.player_cards[self.selected_card_index]
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_card_index = (self.selected_card_index - 1) % 4
                elif event.key == pygame.K_DOWN:
                    self.selected_card_index = (self.selected_card_index + 1) % 4
                elif event.key == pygame.K_LEFT:
                    self.selected_tavern_card_index = (self.selected_tavern_card_index - 1) % len(self.all_cards)
                elif event.key == pygame.K_RIGHT:
                    self.selected_tavern_card_index = (self.selected_tavern_card_index + 1) % len(self.all_cards)
                elif event.key == pygame.K_RETURN:
                    self.swap_card()
                elif event.key == pygame.K_e:
                    self.return_to_game()

    def update(self):
        """Prevent crashes by ensuring update exists."""
        pass

    def return_to_game(self):
        """Exit Tavern and return to the game while saving cards."""
        self.save_cards()
        from screens.starting_area_screen import StartingAreaScreen
        self.game.change_screen(StartingAreaScreen(self.game, self.game.selected_player))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))  # Draw Tavern Background

        # Draw "Edit Your Deck" at the top center
        title_text = self.font.render("Edit Your Deck", True, (255, 255, 255))
        screen.blit(title_text, ((1200 - title_text.get_width()) // 2, 30))

        # Centering player cards
        screen_width = 1200
        card_width = 150
        card_height = 200
        card_spacing = 130  # Space between cards

        # Center player cards horizontally
        total_card_width = 4 * card_spacing
        start_x_player = (screen_width - total_card_width) // 2

        card_y_player = 500  # Player's cards row
        card_y_tavern = 250  # Tavern's cards row

        # Draw Player Cards (Bottom Row - Centered)
        for i, card in enumerate(self.player_cards):
            card_x = start_x_player + i * card_spacing
            if self.card_images.get(card.name):
                screen.blit(self.card_images[card.name], (card_x, card_y_player))
            if i == self.selected_card_index:  # Highlight selected card
                pygame.draw.rect(screen, (255, 255, 0), (card_x, card_y_player, card_width, card_height), 5)

        # Center tavern cards horizontally
        total_tavern_card_width = len(self.all_cards) * card_spacing
        start_x_tavern = (screen_width - total_tavern_card_width) // 2

        # Draw Tavern Cards (Top Row - Centered)
        for i, card in enumerate(self.all_cards):
            card_x = start_x_tavern + i * card_spacing  # Start drawing from the centered position
            if self.card_images.get(card.name):
                screen.blit(self.card_images[card.name], (card_x, card_y_tavern))
            if i == self.selected_tavern_card_index:
                pygame.draw.rect(screen, (0, 255, 255), (card_x, card_y_tavern, card_width, card_height), 5)

        # Instructions at the bottom
        info_text = self.info_font.render("UP/DOWN: Select your card | LEFT/RIGHT: Browse Tavern | ENTER: Swap | E: Exit", True, (255, 255, 255))
        screen.blit(info_text, ((screen_width - info_text.get_width()) // 2, 750))
