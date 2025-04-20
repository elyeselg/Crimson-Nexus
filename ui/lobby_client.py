import pygame
import pygame_textinput
from network.network import GameClient
from ui.network_game_loop import run_network_game

# === CONFIG ===
WIDTH, HEIGHT = 1000, 800
DARK = (15, 15, 25)
GOLD = (220, 190, 80)
WHITE = (240, 240, 240)
GRAY = (100, 100, 100)

pygame.font.init()
font_title = pygame.font.SysFont("Georgia", 54, bold=True)
font_label = pygame.font.SysFont("Georgia", 26)
font_status = pygame.font.SysFont("Georgia", 22)

def lobby_client(screen):
    from ui.menu import run_menu
    clock = pygame.time.Clock()

    ip_input = pygame_textinput.TextInputVisualizer()
    pseudo_input = pygame_textinput.TextInputVisualizer()

    ip_input.value = "127.0.0.1"
    pseudo_input.value = "Client"

    for input_box in [ip_input, pseudo_input]:
        input_box.cursor_color = WHITE
        input_box.font_color = WHITE

    input_focus = "ip"
    client = None
    host_name = None
    connected = False
    game_started = False

    def try_connect():
        nonlocal client, connected
        try:
            client = GameClient(ip_input.value)
            client.connect()
            client.on_receive = on_receive
            client.send({"pseudo": pseudo_input.value})
            connected = True
        except Exception as e:
            print("❌ Connexion échouée :", e)

    def on_receive(data):
        nonlocal game_started, host_name
        if isinstance(data, dict):
            if "start" in data:
                game_started = True
            elif "pseudo" in data:
                host_name = data["pseudo"]

    while True:
        screen.fill(DARK)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                if client:
                    client.stop()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not connected:
                    try_connect()
                elif event.key == pygame.K_ESCAPE:
                    return run_menu(screen)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ip_rect.collidepoint(event.pos):
                    input_focus = "ip"
                elif pseudo_rect.collidepoint(event.pos):
                    input_focus = "pseudo"
                elif btn_return.collidepoint(event.pos):
                    return run_menu(screen)

        if input_focus == "ip":
            ip_input.update(events)
        elif input_focus == "pseudo":
            pseudo_input.update(events)

        # === UI ===
        title = font_title.render("Connexion au Salon", True, GOLD)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        # --- Cadre principal ---
        box = pygame.Rect(WIDTH // 2 - 280, 160, 560, 340)
        pygame.draw.rect(screen, (25, 25, 35), box, border_radius=14)
        pygame.draw.rect(screen, GOLD, box, 2, border_radius=14)

        # --- Champs texte ---
        label_ip = font_label.render("Adresse IP :", True, WHITE)
        label_pseudo = font_label.render("Votre pseudo :", True, WHITE)

        ip_rect = pygame.Rect(box.x + 230, box.y + 40, 240, 36)
        pseudo_rect = pygame.Rect(box.x + 230, box.y + 120, 240, 36)

        screen.blit(label_ip, (box.x + 40, box.y + 40))
        screen.blit(ip_input.surface, ip_rect.topleft)
        pygame.draw.rect(screen, GOLD if input_focus == "ip" else WHITE, ip_rect, 2, border_radius=6)

        screen.blit(label_pseudo, (box.x + 40, box.y + 120))
        screen.blit(pseudo_input.surface, pseudo_rect.topleft)
        pygame.draw.rect(screen, GOLD if input_focus == "pseudo" else WHITE, pseudo_rect, 2, border_radius=6)

        # --- Statut de connexion ---
        status = f"Hôte : {host_name}" if host_name else "En attente de l’hôte..."
        status_color = GOLD if host_name else GRAY
        status_render = font_status.render(status, True, status_color)
        screen.blit(status_render, (box.x + 40, box.y + 200))

        if not connected:
            hint = font_status.render("Entrée pour se connecter", True, GRAY)
            screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, box.y + 270))

        # --- Bouton retour ---
        btn_return = pygame.Rect(30, HEIGHT - 60, 190, 42)
        pygame.draw.rect(screen, (30, 30, 40), btn_return, border_radius=8)
        pygame.draw.rect(screen, GOLD, btn_return, 2, border_radius=8)
        text_retour = font_label.render("Menu principal", True, GOLD)
        screen.blit(
            text_retour,
            (btn_return.x + (btn_return.width - text_retour.get_width()) // 2,
             btn_return.y + (btn_return.height - text_retour.get_height()) // 2)
        )

        if game_started:
            run_network_game(client, is_host=False)
            return

        pygame.display.flip()
        clock.tick(60)
