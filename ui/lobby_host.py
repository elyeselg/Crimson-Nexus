import pygame
import pygame_textinput
import socket
from network.network import GameServer
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

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def lobby_host(screen):
    from ui.menu import run_menu
    clock = pygame.time.Clock()
    server = GameServer()
    server.start()

    ip_address = get_local_ip()
    pseudo_input = pygame_textinput.TextInputVisualizer()
    pseudo_input.value = "Host"
    pseudo_input.cursor_color = WHITE
    pseudo_input.font_color = WHITE

    input_focused = True
    client_name = None
    start_enabled = False

    def on_receive(data):
        nonlocal client_name, start_enabled
        if isinstance(data, dict) and "pseudo" in data:
            client_name = data["pseudo"]
            start_enabled = True

    server.on_receive = on_receive

    while True:
        screen.fill(DARK)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                server.stop()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    server.stop()
                    return run_menu(screen)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                input_box = pygame.Rect(WIDTH // 2 - 60, 280, 240, 36)
                if input_box.collidepoint(event.pos):
                    input_focused = True
                else:
                    input_focused = False

                # Démarrage partie
                start_btn = pygame.Rect(WIDTH // 2 - 120, HEIGHT - 120, 240, 60)
                if start_enabled and start_btn.collidepoint(event.pos):
                    server.send({"start": True})
                    run_network_game(server, is_host=True)
                    return

                # Bouton retour
                return_btn = pygame.Rect(30, HEIGHT - 60, 190, 42)
                if return_btn.collidepoint(event.pos):
                    server.stop()
                    return run_menu(screen)

        if input_focused:
            pseudo_input.update(events)

        # === TITRE ===
        title = font_title.render("Connexion au Salon", True, GOLD)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        # === CADRE PRINCIPAL ===
        box = pygame.Rect(WIDTH // 2 - 280, 160, 560, 340)
        pygame.draw.rect(screen, (25, 25, 35), box, border_radius=14)
        pygame.draw.rect(screen, GOLD, box, 2, border_radius=14)

        # === CHAMPS ===
        label_ip = font_label.render("Adresse IP :", True, WHITE)
        ip_text = font_label.render(ip_address, True, GOLD)
        screen.blit(label_ip, (box.x + 40, box.y + 40))
        screen.blit(ip_text, (box.x + 230, box.y + 40))

        label_pseudo = font_label.render("Votre pseudo :", True, WHITE)
        screen.blit(label_pseudo, (box.x + 40, box.y + 120))

        input_rect = pygame.Rect(box.x + 230, box.y + 120, 240, 36)
        screen.blit(pseudo_input.surface, input_rect.topleft)
        pygame.draw.rect(screen, GOLD if input_focused else WHITE, input_rect, 2, border_radius=6)

        # === STATUS JOUEUR ===
        player_status = f"Joueur connecté : {client_name}" if client_name else "En attente d’un joueur..."
        status_color = GOLD if client_name else GRAY
        status_render = font_status.render(player_status, True, status_color)
        screen.blit(status_render, (box.x + 40, box.y + 200))

        # === BOUTON LANCER ===
        if start_enabled:
            btn = pygame.Rect(WIDTH // 2 - 120, HEIGHT - 120, 240, 60)
            pygame.draw.rect(screen, GOLD, btn, border_radius=12)
            pygame.draw.rect(screen, WHITE, btn, 2, border_radius=12)
            btn_text = font_label.render("Lancer la partie", True, WHITE)
            screen.blit(
                btn_text,
                (btn.x + (btn.width - btn_text.get_width()) // 2,
                 btn.y + (btn.height - btn_text.get_height()) // 2)
            )

        # === BOUTON RETOUR ===
        return_btn = pygame.Rect(30, HEIGHT - 60, 190, 42)
        pygame.draw.rect(screen, (30, 30, 40), return_btn, border_radius=8)
        pygame.draw.rect(screen, GOLD, return_btn, 2, border_radius=8)
        return_text = font_label.render("Menu principal", True, GOLD)
        screen.blit(
            return_text,
            (return_btn.x + (return_btn.width - return_text.get_width()) // 2,
             return_btn.y + (return_btn.height - return_text.get_height()) // 2)
        )

        pygame.display.flip()
        clock.tick(60)
