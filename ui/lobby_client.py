import pygame
import pygame_textinput
from network.network import GameClient
from ui.network_game_loop import run_network_game

WIDTH, HEIGHT = 1000, 800
WHITE = (255, 255, 255)
DARK = (25, 25, 25)
BLUE = (100, 160, 255)
GRAY = (180, 180, 180)

pygame.font.init()
font_title = pygame.font.SysFont("segoeui", 54, bold=True)
font_text = pygame.font.SysFont("segoeui", 28)

def lobby_client(screen):
    clock = pygame.time.Clock()
    ip_input = pygame_textinput.TextInputVisualizer()
    pseudo_input = pygame_textinput.TextInputVisualizer()
    ip_input.value = "127.0.0.1"
    pseudo_input.value = "Client"

    client = None
    host_name = None
    game_started = False
    connected = False

    def try_connect():
        nonlocal client, connected
        try:
            client = GameClient(ip_input.value)
            client.connect()
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

    running = True
    while running:
        screen.fill(DARK)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and not connected:
                try_connect()
                if client:
                    client.on_receive = on_receive

        ip_input.update(events)
        pseudo_input.update(events)

        # --- AFFICHAGE ---
        title = font_title.render("Lobby – Client", True, WHITE)
        ip_label = font_text.render("IP du serveur :", True, WHITE)
        pseudo_label = font_text.render("Ton pseudo :", True, WHITE)
        status = font_text.render(
            f"Hôte : {host_name or 'En attente...'}", True, BLUE if host_name else GRAY
        )
        help_text = font_text.render("Appuie sur Entrée pour te connecter", True, GRAY)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
        screen.blit(ip_label, (WIDTH // 2 - 150, 180))
        screen.blit(ip_input.surface, (WIDTH // 2, 180))
        screen.blit(pseudo_label, (WIDTH // 2 - 150, 250))
        screen.blit(pseudo_input.surface, (WIDTH // 2, 250))
        screen.blit(status, (WIDTH // 2 - 150, 330))
        if not connected:
            screen.blit(help_text, (WIDTH // 2 - help_text.get_width() // 2, 400))

        if game_started:
            run_network_game(client, is_host=False)
            return

        pygame.display.flip()
        clock.tick(60)
