import pygame

WIDTH, HEIGHT = 1000, 800
SQUARE_SIZE = 800 // 8

WHITE = (245, 245, 245)
GRAY = (160, 160, 160)
GREEN = (50, 200, 50)
HIGHLIGHT = (0, 150, 255)
BLACK = (30, 30, 30)

PIECE_SYMBOLS = {
    "Pawn": "♙", "Rook": "♖", "Knight": "♘",
    "Bishop": "♗", "Queen": "♕", "King": "♔"
}

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
    colors = [WHITE, GRAY]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
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
    if selected_pos:
        row, col = selected_pos
        pygame.draw.rect(screen, HIGHLIGHT, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)
    for move in legal_moves:
        end_row, end_col = move.end_pos
        center = (end_col * SQUARE_SIZE + SQUARE_SIZE // 2, end_row * SQUARE_SIZE + SQUARE_SIZE // 2)
        pygame.draw.circle(screen, GREEN, center, 10)

def format_move(move):
    def to_alg(pos):
        row, col = pos
        return f"{chr(col + 97)}{8 - row}"
    return f"{to_alg(move.start_pos)} → {to_alg(move.end_pos)}"

def draw_move_history(screen, move_history):
    font = pygame.font.SysFont("segoeui", 22)
    x = 810
    y = 30
    screen.fill((240, 240, 240), (800, 0, 200, HEIGHT))
    
    title = font.render("Historique", True, BLACK)
    screen.blit(title, (x + (200 - title.get_width()) // 2 - 10, 10))

    move_pairs = [move_history[i:i+2] for i in range(0, len(move_history), 2)]
    for idx, pair in enumerate(move_pairs):
        text = f"{idx + 1}. "
        for move in pair:
            text += format_move(move) + "  "
        rendered = font.render(text.strip(), True, BLACK)
        screen.blit(rendered, (x + 10, y))
        y += 30

def draw_captured(screen, move_history):
    white_taken = []
    black_taken = []

    for move in move_history:
        if move.piece_captured:
            name = move.piece_captured.__class__.__name__
            symbol = PIECE_SYMBOLS.get(name, "?")
            if move.piece_captured.color == "white":
                white_taken.append(symbol)
            else:
                black_taken.append(symbol)

    return white_taken, black_taken, 0, 0  # scores supprimés car inutiles

def show_check_popup(screen):
    rect = pygame.Rect(WIDTH // 2 - 100, 20, 200, 40)
    pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=10)
    pygame.draw.rect(screen, (255, 0, 0), rect, width=3, border_radius=10)
    font = pygame.font.SysFont("segoeui", 24)
    text = font.render("Échec !", True, (255, 0, 0))
    screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

def show_end_screen(screen, message, winner, white_taken, black_taken, white_score, black_score):
    pygame.draw.rect(screen, (30, 30, 30), (180, 240, 640, 360), border_radius=16)
    pygame.draw.rect(screen, (255, 255, 255), (180, 240, 640, 360), width=3, border_radius=16)

    font_title = pygame.font.SysFont("segoeui", 48)
    font_info = pygame.font.SysFont("segoeui", 28)

    y = 270

    # --- Détection spéciale Mat ou Pat ---
    if "échec et mat" in message.lower():
        main_message = "Échec et Mat !"
        color_message = (255, 80, 80)
    elif "pat" in message.lower() or "match nul" in message.lower():
        main_message = "Pat !"
        color_message = (80, 180, 255)
    else:
        main_message = "Fin de Partie"
        color_message = (255, 255, 255)

    # --- Affichage principal ---
    screen.blit(font_title.render(main_message, True, color_message), (WIDTH // 2 - font_title.size(main_message)[0] // 2, y))
    y += 60

    # --- Gagnant ---
    if winner != "Aucun":
        winner_text = f"Gagnant : {winner}"
        screen.blit(font_info.render(winner_text, True, (200, 255, 200)), (WIDTH // 2 - font_info.size(winner_text)[0] // 2, y))
        y += 40
    else:
        draw = "Match nul"
        screen.blit(font_info.render(draw, True, (200, 200, 200)), (WIDTH // 2 - font_info.size(draw)[0] // 2, y))
        y += 40

    # --- Scores capturés ---
    screen.blit(font_info.render(f"Score Blanc : {white_score}   |   Score Noir : {black_score}", True, (255, 255, 255)), (WIDTH // 2 - 200, y))
    y += 40

    # --- Pièces capturées ---
    screen.blit(font_info.render(f"Capturées par Blancs : {''.join(black_taken)}", True, (255, 255, 255)), (WIDTH // 2 - 200, y))
    y += 30
    screen.blit(font_info.render(f"Capturées par Noirs : {''.join(white_taken)}", True, (255, 255, 255)), (WIDTH // 2 - 200, y))
    y += 30

    # --- Boutons ---
    button_replay = pygame.Rect(WIDTH // 2 - 170, y + 50, 150, 40)
    button_menu = pygame.Rect(WIDTH // 2 + 20, y + 50, 170, 40)

    pygame.draw.rect(screen, (70, 70, 70), button_replay, border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), button_replay, width=2, border_radius=10)
    pygame.draw.rect(screen, (70, 70, 70), button_menu, border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), button_menu, width=2, border_radius=10)

    font_btn = pygame.font.SysFont("segoeui", 26)
    screen.blit(font_btn.render("Rejouer", True, (255, 255, 255)), (button_replay.x + 25, button_replay.y + 5))
    screen.blit(font_btn.render("Retour Menu", True, (255, 255, 255)), (button_menu.x + 15, button_menu.y + 5))

    return button_replay, button_menu

