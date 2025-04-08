import pygame
import pygame_textinput
import socket
from network.network import GameServer
from ui.network_game_loop import run_network_game

WIDTH, HEIGHT = 1000, 800
WHITE = (255, 255, 255)
DARK = (25, 25, 25)
BLUE = (100, 160, 255)
GRAY = (180, 180, 180)

pygame.font.init()
font_title = pygame.font.SysFont("segoeui", 54, bold=True)
font_text = pygame.font.SysFont("segoeui", 28)

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
    clock = pygame.time.Clock()
    server = GameServer()
    server.start()

    ip_address = get_local_ip()
    pseudo_input = pygame_textinput.TextInputVisualizer()
    pseudo_input.value = "Host"

    client_name = None
    start_enabled = False

    def on_receive(data):
        nonlocal client_name, start_enabled
        if isinstance(data, dict) and "pseudo" in data:
            client_name = data["pseudo"]
            start_enabled = True

    server.on_receive = on_receive

    running = True
    while running:
        screen.fill(DARK)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and start_enabled:
                x, y = event.pos
                if WIDTH // 2 - 100 <= x <= WIDTH // 2 + 100 and HEIGHT - 120 <= y <= HEIGHT - 70:
                    # Envoie un signal de démarrage au client
                    server.send({"start": True})
                    run_network_game(server, is_host=True)
                    return

        pseudo_input.update(events)

        # Textes
        title = font_title.render("Lobby – Hôte", True, WHITE)
        ip_label = font_text.render(f"Ton IP : {ip_address}", True, WHITE)
        pseudo_label = font_text.render("Ton pseudo :", True, WHITE)
        client_label = font_text.render(
            f"Joueur connecté : {client_name or 'En attente...'}", True, BLUE if client_name else GRAY
        )

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
        screen.blit(ip_label, (WIDTH // 2 - 150, 180))
        screen.blit(pseudo_label, (WIDTH // 2 - 150, 250))
        screen.blit(pseudo_input.surface, (WIDTH // 2, 250))
        screen.blit(client_label, (WIDTH // 2 - 150, 330))

        if start_enabled:
            pygame.draw.rect(screen, BLUE, (WIDTH // 2 - 100, HEIGHT - 120, 200, 50), border_radius=10)
            start_text = font_text.render("Lancer la partie", True, WHITE)
            screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT - 110))

        pygame.display.flip()
        clock.tick(60)
