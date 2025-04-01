import pygame
import sys
from ui.game_loop import run_game
from network.network import GameServer, GameClient
import pygame_textinput

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

# === INIT ===
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crimson Nexus – Menu")
font_title = pygame.font.SysFont("segoeui", 64, bold=True)
font_button = pygame.font.SysFont("segoeui", 28)
clock = pygame.time.Clock()

# === MUSIQUE ===
pygame.mixer.init()
try:
    pygame.mixer.music.load("assets/music/menu_theme.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except Exception as e:
    print("🎵 Erreur de chargement de la musique :", e)

# === UTIL ===
def load_icon(path, size=(40, 40)):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(img, size)

def quit_game():
    pygame.quit()
    sys.exit()

# === BOUTON ICONIQUE ===
class IconButton:
    def __init__(self, text, icon_path, y, callback, color=HIGHLIGHT):
        self.text = text
        self.icon = load_icon(icon_path)
        self.callback = callback
        self.color = color
        self.base_color = color
        self.hover_color = tuple(min(c + 40, 255) for c in color)
        self.hovered = False
        self.rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, y, BUTTON_WIDTH, BUTTON_HEIGHT)

    def draw(self, surface):
        bg = self.hover_color if self.hovered else self.base_color
        pygame.draw.rect(surface, bg, self.rect, border_radius=BUTTON_RADIUS)
        surface.blit(self.icon, (self.rect.x + 15, self.rect.y + 15))
        text_surface = font_button.render(self.text, True, WHITE)
        surface.blit(text_surface, (self.rect.x + 70, self.rect.y + (BUTTON_HEIGHT - text_surface.get_height()) // 2))

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()

# === MENU PRINCIPAL ===
def run_menu():
    state = "main"
    server = None
    client = None
    ip_input = pygame_textinput.TextInputVisualizer()
    ip_input.value = "127.0.0.1"

    def start_vs_ai():
        run_game(difficulty="easy")  # difficulté unique maintenant

    def start_host():
        nonlocal server
        server = GameServer()
        server.start()
        run_game(difficulty="online", network=server, is_host=True)

    def start_client(ip):
        nonlocal client
        client = GameClient(ip)
        client.connect()
        run_game(difficulty="online", network=client)

    mp_buttons = [
        IconButton("Créer un salon", "assets/icons/multiplayer.png", 300, start_host, HIGHLIGHT),
        IconButton("Rejoindre un salon", "assets/icons/multiplayer.png", 390, lambda: start_client(ip_input.value), SOFT_BLUE),
        IconButton("← Retour", "assets/icons/back.png", 490, lambda: switch_state("main"), GRAY)
    ]

    def switch_state(new_state):
        nonlocal state
        state = new_state

    main_buttons = [
        IconButton("Jouer contre l'IA", "assets/icons/ai.png", 300, start_vs_ai),
        IconButton("Multijoueur", "assets/icons/multiplayer.png", 390, lambda: switch_state("mp")),
        IconButton("Quitter", "assets/icons/quit.png", 480, quit_game)
    ]

    running = True
    while running:
        screen.fill(DARK)
        for y in range(HEIGHT):
            pygame.draw.line(screen, (25 + y // 20, 30 + y // 15, 40 + y // 10), (0, y), (WIDTH, y))

        title = font_title.render("Crimson Nexus", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))

        buttons = main_buttons if state == "main" else mp_buttons

        mouse = pygame.mouse.get_pos()
        for btn in buttons:
            btn.check_hover(mouse)
            btn.draw(screen)

        if state == "mp":
            ip_input.update(pygame.event.get())
            ip_label = font_button.render("IP du serveur :", True, WHITE)
            screen.blit(ip_label, (WIDTH // 2 - 160, 240))
            screen.blit(ip_input.surface, (WIDTH // 2, 240))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    btn.check_click(event.pos)

        pygame.display.flip()
        clock.tick(60)
