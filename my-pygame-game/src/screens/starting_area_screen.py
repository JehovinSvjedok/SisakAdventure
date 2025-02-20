import pygame
from screens.tavern_screen import TavernScreen
from screens.gameplay_screen import GameplayScreen

class StartingAreaScreen:
    def __init__(self, game, player):
        self.game = game
        self.screen = game.screen
        self.player = player  

        # Load assets
        self.background = pygame.image.load('my-pygame-game/src/assets/main_bg.png')  
        self.tavern_image = pygame.image.load('my-pygame-game/src/assets/kuca.png')
        self.portal_image = pygame.image.load('my-pygame-game/src/assets/portal.png')

        # Resize tavern and portal images
        self.tavern_image = pygame.transform.scale(self.tavern_image, (500, 500))  
        self.portal_image = pygame.transform.scale(self.portal_image, (360, 480))  

        # Player setup
        self.original_player_image = self.player.get_image()
        self.original_player_image = pygame.transform.scale(self.original_player_image, (200, 240))
        self.player_image = self.original_player_image  
        self.player_rect = self.player_image.get_rect(center=(600, 625))  

        # Direction tracking
        self.facing_right = True

        # Tavern & Portal positions
        self.tavern_rect = self.tavern_image.get_rect(center=(200, 600))  
        self.portal_rect = self.portal_image.get_rect(center=(1000, 600))  

        # Interaction flags
        self.near_tavern = False
        self.near_portal = False  # New flag for the portal

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if self.near_tavern:
                        print("Entering Tavern...")
                        self.game.change_screen(TavernScreen(self.game))
                    if self.near_portal:
                        print("Entering Portal... Starting Combat!")
                        self.game.change_screen(GameplayScreen(self.game, self.player))

    def update(self):
        keys = pygame.key.get_pressed()  
        speed = 5  

        if keys[pygame.K_a]:  
            self.player_rect.x -= speed
            if self.facing_right:  
                self.player_image = pygame.transform.flip(self.original_player_image, True, False)
                self.facing_right = False

        if keys[pygame.K_d]:  
            self.player_rect.x += speed
            if not self.facing_right:  
                self.player_image = self.original_player_image
                self.facing_right = True

        # Prevent player from moving off the screen
        self.player_rect.left = max(0, self.player_rect.left)
        self.player_rect.right = min(self.game.screen.get_width(), self.player_rect.right)

        # Check interactions
        self.near_tavern = self.player_rect.colliderect(self.tavern_rect)
        self.near_portal = self.player_rect.colliderect(self.portal_rect)  # Check portal collision

    def draw(self, screen):
        screen.blit(self.background, (0, 0))  
        screen.blit(self.tavern_image, self.tavern_rect)
        screen.blit(self.portal_image, self.portal_rect)
        screen.blit(self.player_image, self.player_rect)  

        font = pygame.font.Font(None, 36)

        # Show interaction text
        if self.near_tavern:
            text = font.render("Press E to enter the Tavern", True, (255, 255, 255))
            screen.blit(text, (self.tavern_rect.centerx - text.get_width() // 2, self.tavern_rect.top - 40))

        if self.near_portal:
            text = font.render("Press E to enter the Portal", True, (255, 255, 255))
            screen.blit(text, (self.portal_rect.centerx - text.get_width() // 2, self.portal_rect.top - 40))