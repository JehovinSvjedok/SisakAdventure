def load_image(file_path):
    """Load an image from the specified file path."""
    try:
        image = pygame.image.load(file_path)
        return image
    except pygame.error as e:
        print(f"Unable to load image at {file_path}: {e}")
        return None

def load_sound(file_path):
    """Load a sound from the specified file path."""
    try:
        sound = pygame.mixer.Sound(file_path)
        return sound
    except pygame.error as e:
        print(f"Unable to load sound at {file_path}: {e}")
        return None

def draw_text(surface, text, font, color, position):
    """Draw text on the given surface at the specified position."""
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

def reset_game_state():
    """Reset the game state to its initial values."""
    return {
        'player': None,
        'deck': [],
        'current_screen': 'start',
        'score': 0,
    }