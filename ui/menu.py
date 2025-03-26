import pygame
import sys
from ui.game_loop import run_game
from network.network import GameServer, GameClient
import pygame_textinput

# === Couleurs ===
WHITE = (255, 255, 255)
SOFT_GRAY = (245, 245, 245)
DARK_TEXT = (50, 50, 50)
ACCENT = (0, 122, 255)
ACCENT_HOVER = (0, 102, 210)
GREEN = (70, 200, 70)
ORANGE = (240, 160, 60)
RED = (220, 70, 70)

WIDTH, HEIGHT = 800, 800
BUTTON_WIDTH = 280
BUTTON_HEIGHT = 60
BUTTON_RADIUS = 12

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crimson Nexus – Menu")
font_title = pygame.font.SysFont("segoeui", 58, bold=False)
font_button = pygame.font.SysFont("segoeui", 28)

clock = pygame.time.Clock()


class Button:
    def __init__(self, text, x, y, callback, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.callback = callback
        self.color = color
        self.hover_color = hover_color
        self.hovered = False
        self.alpha = 0
        self.visible = False

    def draw(self, surface):
        if not self.visible:
            return

        shadow_rect = self.rect.copy()
        shadow_rect.move_ip(2, 2)
        pygame.draw.rect(surface, (180, 180, 180), shadow_rect, border_radius=BUTTON_RADIUS)

        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=BUTTON_RADIUS)

        text_surf = font_button.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        if not self.visible:
            return
        self.hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        if self.visible and self.rect.collidepoint(mouse_pos):
            self.callback()

    def animate_in(self, speed=10):
        if self.alpha < 255:
            self.alpha += speed
            if self.alpha > 255:
                self.alpha = 255


def quit_game():
    pygame.quit()
    sys.exit()


def run_menu():
    state = "main"
    server = None
    client = None

    ip_input = pygame_textinput.TextInputVisualizer()
    ip_input.value = "127.0.0.1"

    def switch_to_ia():
        nonlocal state
        state = "ia_choice"
        for btn in ia_buttons:
            btn.visible = True
            btn.alpha = 0

    def switch_to_multiplayer():
        nonlocal state
        state = "multiplayer"
        for btn in multiplayer_buttons:
            btn.visible = True
            btn.alpha = 0
        ip_input.value = "127.0.0.1"

    def switch_to_main():
        nonlocal state
        state = "main"
        for btn in ia_buttons + multiplayer_buttons:
            btn.visible = False

    def start_host():
        nonlocal server
        server = GameServer()
        server.start()
        print("🟢 Serveur lancé. En attente de connexion...")
        run_game(difficulty="online", network=server, is_host=True)

    def start_client(ip):
        nonlocal client
        client = GameClient(host=ip)
        client.connect()
        print(f"🔵 Client connecté à {ip}")
        run_game(difficulty="online", network=client, is_host=False)

    # === Boutons ===
    main_buttons = [
        Button("Jouer contre l'IA", WIDTH // 2 - BUTTON_WIDTH // 2, 300, switch_to_ia, (40, 120, 240), (30, 100, 220)),
        Button("Multijoueur", WIDTH // 2 - BUTTON_WIDTH // 2, 380, switch_to_multiplayer, (80, 80, 80), (100, 100, 100)),
        Button("Quitter", WIDTH // 2 - BUTTON_WIDTH // 2, 460, quit_game, (200, 60, 60), (240, 80, 80)),
    ]

    ia_buttons = [
        Button("Facile", WIDTH // 2 - BUTTON_WIDTH // 2, 320, lambda: run_game("easy"), GREEN, (50, 255, 50)),
        Button("Normal", WIDTH // 2 - BUTTON_WIDTH // 2, 400, lambda: run_game("normal"), ORANGE, (255, 180, 80)),
        Button("Difficile", WIDTH // 2 - BUTTON_WIDTH // 2, 480, lambda: run_game("hard"), RED, (255, 90, 90)),
        Button("← Retour", WIDTH // 2 - BUTTON_WIDTH // 2, 560, switch_to_main, ACCENT, ACCENT_HOVER),
    ]

    multiplayer_buttons = [
        Button("Créer un salon (hôte)", WIDTH // 2 - BUTTON_WIDTH // 2, 320, start_host, ACCENT, ACCENT_HOVER),
        Button("Rejoindre un salon", WIDTH // 2 - BUTTON_WIDTH // 2, 400, lambda: start_client(ip_input.value), ACCENT, ACCENT_HOVER),
        Button("← Retour", WIDTH // 2 - BUTTON_WIDTH // 2, 480, switch_to_main, ACCENT, ACCENT_HOVER),
    ]

    for btn in main_buttons:
        btn.visible = True

    running = True
    while running:
        screen.fill(SOFT_GRAY)
        mouse_pos = pygame.mouse.get_pos()

        title = font_title.render("Crimson Nexus", True, DARK_TEXT)
        title_rect = title.get_rect(center=(WIDTH // 2, 150))
        screen.blit(title, title_rect)

        if state == "ia_choice":
            buttons = ia_buttons
        elif state == "multiplayer":
            buttons = multiplayer_buttons
        else:
            buttons = main_buttons

        for button in buttons:
            button.check_hover(mouse_pos)
            button.animate_in(speed=12)
            button.draw(screen)

        if state == "multiplayer":
            ip_input.update(pygame.event.get())
            ip_label = font_button.render("Adresse IP :", True, DARK_TEXT)
            screen.blit(ip_label, (WIDTH // 2 - BUTTON_WIDTH // 2, 260))
            screen.blit(ip_input.surface, (WIDTH // 2 - BUTTON_WIDTH // 2 + 150, 260))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.check_click(mouse_pos)

        pygame.display.flip()
        clock.tick(60)
