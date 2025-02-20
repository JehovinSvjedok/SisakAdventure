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

        self.selected_card_index = None
        self.selected_tavern_card_index = None

        # Load card images
        self.card_images = self.load_card_images()

        # Card display settings
        self.card_width = 150
        self.card_height = 200
        self.card_spacing = 130

        # Calculate centered positions
        self.start_x_player = (1200 - (4 * self.card_spacing)) // 2
        self.card_y_player = 500

        self.start_x_tavern = (1200 - (len(self.all_cards) * self.card_spacing)) // 2
        self.card_y_tavern = 250

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
        if self.selected_card_index is not None and self.selected_tavern_card_index is not None:
            self.player_cards[self.selected_card_index], self.all_cards[self.selected_tavern_card_index] = (
                self.all_cards[self.selected_tavern_card_index], self.player_cards[self.selected_card_index]
            )
            self.selected_card_index = None
            self.selected_tavern_card_index = None  # Reset selection

    def handle_events(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Check if a player card is clicked
                    for i in range(len(self.player_cards)):
                        card_x = self.start_x_player + i * self.card_spacing
                        if card_x <= mouse_x <= card_x + self.card_width and \
                                self.card_y_player <= mouse_y <= self.card_y_player + self.card_height:
                            self.selected_card_index = i

                    # Check if a tavern card is clicked
                    for i in range(len(self.all_cards)):
                        card_x = self.start_x_tavern + i * self.card_spacing
                        if card_x <= mouse_x <= card_x + self.card_width and \
                                self.card_y_tavern <= mouse_y <= self.card_y_tavern + self.card_height:
                            self.selected_tavern_card_index = i

                    # Swap if both selections are made
                    if self.selected_card_index is not None and self.selected_tavern_card_index is not None:
                        self.swap_card()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
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

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Draw Player Cards (Bottom Row - Centered)
        for i, card in enumerate(self.player_cards):
            card_x = self.start_x_player + i * self.card_spacing

            # Check if mouse is hovering over this card
            is_hovered = card_x <= mouse_x <= card_x + self.card_width and \
                         self.card_y_player <= mouse_y <= self.card_y_player + self.card_height

            # Resize for hover effect
            size_offset = 10 if is_hovered else 0
            hover_width = self.card_width + size_offset
            hover_height = self.card_height + size_offset
            hover_x = card_x - size_offset // 2
            hover_y = self.card_y_player - size_offset // 2

            if self.card_images.get(card.name):
                scaled_image = pygame.transform.scale(self.card_images[card.name], (hover_width, hover_height))
                screen.blit(scaled_image, (hover_x, hover_y))

        # Draw Tavern Cards (Top Row - Centered)
        for i, card in enumerate(self.all_cards):
            card_x = self.start_x_tavern + i * self.card_spacing

            # Check if mouse is hovering over this card
            is_hovered = card_x <= mouse_x <= card_x + self.card_width and \
                         self.card_y_tavern <= mouse_y <= self.card_y_tavern + self.card_height

            # Resize for hover effect
            size_offset = 10 if is_hovered else 0
            hover_width = self.card_width + size_offset
            hover_height = self.card_height + size_offset
            hover_x = card_x - size_offset // 2
            hover_y = self.card_y_tavern - size_offset // 2

            if self.card_images.get(card.name):
                scaled_image = pygame.transform.scale(self.card_images[card.name], (hover_width, hover_height))
                screen.blit(scaled_image, (hover_x, hover_y))

        # Instructions at the bottom
        info_text = self.info_font.render("Click on a player card, then a tavern card to swap | E: Exit", True, (255, 255, 255))
        screen.blit(info_text, ((1200 - info_text.get_width()) // 2, 750))
