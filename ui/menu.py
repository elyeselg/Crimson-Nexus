import pygame
import sys
from ui.game_loop import run_game
from ui.lobby_host import lobby_host
from ui.lobby_client import lobby_client

# === CONFIG ===
WIDTH, HEIGHT = 1000, 800
BUTTON_WIDTH = 360
BUTTON_HEIGHT = 60
BUTTON_SPACING = 80

# === COULEURS ===
BG_COLOR = (25, 25, 35)
TEXT_COLOR = (240, 240, 240)
ACCENT = (255, 215, 120)
HOVER_COLOR = (70, 70, 90)

pygame.font.init()
font_title = pygame.font.SysFont("Segoe UI", 66, bold=True)
font_button = pygame.font.SysFont("Segoe UI", 30)

def quit_game():
    pygame.quit()
    sys.exit()

class ElegantButton:
    def __init__(self, text, y, callback):
        self.text = text
        self.callback = callback
        self.y = y
        self.rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.hovered = False

    def draw(self, surface):
        color = HOVER_COLOR if self.hovered else (40, 40, 60)
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, ACCENT, self.rect, width=2, border_radius=10)

        text_surface = font_button.render(self.text, True, TEXT_COLOR)
        surface.blit(text_surface, (
            self.rect.centerx - text_surface.get_width() // 2,
            self.rect.centery - text_surface.get_height() // 2
        ))

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()

def run_menu(screen):
    clock = pygame.time.Clock()
    state = "main"

    def start_vs_ai():
        pygame.mixer.music.stop()
        run_game(difficulty="easy")

    def start_lobby_host():
        pygame.mixer.music.stop()
        lobby_host(screen)

    def start_lobby_client():
        pygame.mixer.music.stop()
        lobby_client(screen)

    def switch_state(new):
        nonlocal state
        state = new

    # === BOUTONS ===
    main_buttons = [
        ElegantButton("Jouer contre l'IA", 320, start_vs_ai),
        ElegantButton("Multijoueur", 320 + BUTTON_SPACING, lambda: switch_state("mp")),
        ElegantButton("Quitter", 320 + 2 * BUTTON_SPACING, quit_game)
    ]

    mp_buttons = [
        ElegantButton("Créer un salon", 320, start_lobby_host),
        ElegantButton("Rejoindre un salon", 320 + BUTTON_SPACING, start_lobby_client),
        ElegantButton("← Retour", 320 + 2 * BUTTON_SPACING, lambda: switch_state("main"))
    ]

    while True:
        screen.fill(BG_COLOR)

        # === Titre ===
        title_surface = font_title.render("Crimson Nexus", True, ACCENT)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 140))

        # === Events ===
        events = pygame.event.get()
        mouse = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in main_buttons if state == "main" else mp_buttons:
                    btn.check_click(event.pos)

        # === Boutons ===
        buttons = main_buttons if state == "main" else mp_buttons
        for btn in buttons:
            btn.check_hover(mouse)
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)
