import pygame
import sys
import pygame_textinput
from ui.game_loop import run_game
from ui.lobby_host import lobby_host
from ui.lobby_client import lobby_client



# === CONFIG ===
WIDTH, HEIGHT = 1000, 800
BUTTON_WIDTH, BUTTON_HEIGHT = 320, 70
BUTTON_RADIUS = 14

# === COULEURS ===
WHITE = (255, 255, 255)
DARK = (25, 25, 25)
HIGHLIGHT = (0, 120, 240)
SOFT_BLUE = (100, 160, 255)
GRAY = (180, 180, 180)

pygame.font.init()
font_title = pygame.font.SysFont("segoeui", 64, bold=True)
font_button = pygame.font.SysFont("segoeui", 28)

def quit_game():
    pygame.quit()
    sys.exit()

def load_icon(path, size=(40, 40)):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(img, size)

class IconButton:
    def __init__(self, text, icon_path, y, callback, color=HIGHLIGHT):
        self.text = text
        self.icon = load_icon(icon_path)
        self.callback = callback
        self.color = color
        self.hover_color = tuple(min(c + 40, 255) for c in color)
        self.hovered = False
        self.rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, y, BUTTON_WIDTH, BUTTON_HEIGHT)

    def draw(self, surface):
        bg = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, bg, self.rect, border_radius=BUTTON_RADIUS)
        surface.blit(self.icon, (self.rect.x + 15, self.rect.y + 15))
        text_surface = font_button.render(self.text, True, WHITE)
        surface.blit(text_surface, (self.rect.x + 70, self.rect.y + (BUTTON_HEIGHT - text_surface.get_height()) // 2))

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

    main_buttons = [
        IconButton("Jouer contre l'IA", "assets/icons/ai.png", 300, start_vs_ai),
        IconButton("Multijoueur", "assets/icons/multiplayer.png", 390, lambda: switch_state("mp")),
        IconButton("Quitter", "assets/icons/quit.png", 480, quit_game)
    ]

    mp_buttons = [
        IconButton("Créer un salon", "assets/icons/multiplayer.png", 300, start_lobby_host, HIGHLIGHT),
        IconButton("Rejoindre un salon", "assets/icons/multiplayer.png", 390, start_lobby_client, SOFT_BLUE),
        IconButton("← Retour", "assets/icons/back.png", 490, lambda: switch_state("main"), GRAY)
    ]

    while True:
        screen.fill(DARK)
        for y in range(HEIGHT):
            pygame.draw.line(screen, (25 + y // 20, 30 + y // 15, 40 + y // 10), (0, y), (WIDTH, y))

        title = font_title.render("Crimson Nexus", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))

        events = pygame.event.get()
        mouse = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in main_buttons if state == "main" else mp_buttons:
                    btn.check_click(event.pos)

        buttons = main_buttons if state == "main" else mp_buttons
        for btn in buttons:
            btn.check_hover(mouse)
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)
