import pygame

WIDTH, HEIGHT = 1000, 800
SQUARE_SIZE = 800 // 8

# Couleurs modernes
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
HIGHLIGHT_BORDER = (0, 255, 255)
HIGHLIGHT_DOT = (0, 200, 0)
PANEL_BG = (35, 35, 35)
TEXT_COLOR = (255, 255, 255)
SUBTLE_WHITE = (220, 220, 220)

PIECE_IMAGES = {}

def load_images():
    types = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
    colors = ['white', 'black']
    for color in colors:
        for piece in types:
            name = f"{color}_{piece}"
            path = f"assets/pieces/{name}.png"
            image = pygame.image.load(path)
            PIECE_IMAGES[name] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

def draw_board(screen):
    for row in range(8):
        for col in range(8):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, board):
    for row in range(8):
        for col in range(8):
            piece = board.board[row][col]
            if piece:
                name = f"{piece.color}_{piece.__class__.__name__.lower()}"
                image = PIECE_IMAGES.get(name)
                if image:
                    screen.blit(image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def highlight_squares(screen, selected_pos, legal_moves):
    # --- Case sélectionnée (bord cyan) ---
    if selected_pos:
        row, col = selected_pos
        pygame.draw.rect(
            screen, HIGHLIGHT_BORDER,
            (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            width=4
        )

    # --- Cases de destination (effet vert translucide) ---
    overlay = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    overlay.fill((0, 200, 0, 80))  # vert translucide

    for move in legal_moves:
        end_row, end_col = move.end_pos
        screen.blit(overlay, (end_col * SQUARE_SIZE, end_row * SQUARE_SIZE))


def format_move(move):
    def to_alg(pos):
        row, col = pos
        return f"{chr(col + 97)}{8 - row}"
    return f"{to_alg(move.start_pos)} → {to_alg(move.end_pos)}"

def draw_move_history(screen, move_history):
    pygame.draw.rect(screen, PANEL_BG, (800, 0, 200, HEIGHT))
    font = pygame.font.SysFont("consolas", 20)
    title = font.render("Historique", True, TEXT_COLOR)
    screen.blit(title, (810, 20))

    move_pairs = [move_history[i:i+2] for i in range(0, len(move_history), 2)]
    y = 60
    for idx, pair in enumerate(move_pairs):
        text = f"{idx + 1}. " + "  ".join(format_move(m) for m in pair)
        rendered = font.render(text, True, SUBTLE_WHITE)
        screen.blit(rendered, (810, y))
        y += 28

def draw_captured(screen, move_history):
    # Suppression de l'affichage des pièces capturées
    return [], [], 0, 0

def show_check_popup(screen):
    rect = pygame.Rect(WIDTH // 2 - 100, 20, 200, 40)
    pygame.draw.rect(screen, (250, 250, 250), rect, border_radius=10)
    pygame.draw.rect(screen, (255, 0, 0), rect, width=3, border_radius=10)
    font = pygame.font.SysFont("segoeui", 24)
    text = font.render("Échec !", True, (255, 0, 0))
    screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

def show_end_screen(screen, message, winner, *_):
    pygame.draw.rect(screen, (20, 20, 20), (180, 240, 640, 300), border_radius=16)
    pygame.draw.rect(screen, (255, 255, 255), (180, 240, 640, 300), width=3, border_radius=16)

    font_title = pygame.font.SysFont("georgia", 50, bold=True)
    font_info = pygame.font.SysFont("segoeui", 26)

    y = 270

    if "échec et mat" in message.lower():
        main_message = "Échec et Mat !"
        color_message = (255, 80, 80)
    elif "pat" in message.lower() or "match nul" in message.lower():
        main_message = "Match nul"
        color_message = (100, 200, 255)
    else:
        main_message = "Fin de Partie"
        color_message = (255, 255, 255)

    screen.blit(font_title.render(main_message, True, color_message), (WIDTH // 2 - 160, y))
    y += 60

    if winner != "Aucun":
        winner_text = f"🎉 Gagnant : {winner}"
    else:
        winner_text = "Aucun gagnant"

    screen.blit(font_info.render(winner_text, True, TEXT_COLOR), (WIDTH // 2 - 150, y))
    y += 60

    button_replay = pygame.Rect(WIDTH // 2 - 160, y, 140, 40)
    button_menu = pygame.Rect(WIDTH // 2 + 20, y, 160, 40)

    pygame.draw.rect(screen, HIGHLIGHT_BORDER, button_replay, border_radius=8)
    pygame.draw.rect(screen, HIGHLIGHT_BORDER, button_menu, border_radius=8)

    font_btn = pygame.font.SysFont("segoeui", 24)
    screen.blit(font_btn.render("Rejouer", True, TEXT_COLOR), (button_replay.x + 20, button_replay.y + 8))
    screen.blit(font_btn.render("Retour Menu", True, TEXT_COLOR), (button_menu.x + 15, button_menu.y + 8))

    return button_replay, button_menu
