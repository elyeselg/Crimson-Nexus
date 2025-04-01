import pygame
import threading
from core.board import Board
from core.move import Move
from ai.base_ai import get_random_move
from network.network import GameServer, GameClient

WIDTH, HEIGHT = 1000, 800
SQUARE_SIZE = 800 // 8
PIECE_IMAGES = {}

WHITE = (245, 245, 245)
GRAY = (160, 160, 160)
GREEN = (50, 200, 50)
HIGHLIGHT = (0, 150, 255)
BLACK = (30, 30, 30)

PIECE_SYMBOLS = {
    "Pawn": "♙", "Rook": "♖", "Knight": "♘",
    "Bishop": "♗", "Queen": "♕", "King": "♔"
}


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
    y = 20
    screen.fill((240, 240, 240), (800, 0, 200, HEIGHT))
    screen.blit(font.render("Historique", True, BLACK), (x, y))
    y += 30
    for i, move in enumerate(move_history):
        move_text = format_move(move)
        text = font.render(f"{(i // 2) + 1}. {move_text}", True, BLACK)
        screen.blit(text, (x, y))
        y += 25


def draw_captured(screen, move_history):
    font = pygame.font.SysFont("segoeui", 22)
    white_taken = []
    black_taken = []
    white_score = 0
    black_score = 0

    for move in move_history:
        if move.piece_captured:
            name = move.piece_captured.__class__.__name__
            symbol = PIECE_SYMBOLS.get(name, "?")
            value = {"Pawn": 1, "Knight": 3, "Bishop": 3, "Rook": 5, "Queen": 9}.get(name, 0)

            if move.piece_captured.color == "white":
                white_taken.append(symbol)
                black_score += value
            else:
                black_taken.append(symbol)
                white_score += value

    y_offset = 540
    screen.blit(font.render("Blancs perdus:", True, BLACK), (810, y_offset))
    screen.blit(font.render(" ".join(white_taken), True, BLACK), (810, y_offset + 30))
    screen.blit(font.render(f"Score Noir: {black_score}", True, BLACK), (810, y_offset + 55))

    screen.blit(font.render("Noirs perdus:", True, BLACK), (810, y_offset + 100))
    screen.blit(font.render(" ".join(black_taken), True, BLACK), (810, y_offset + 130))
    screen.blit(font.render(f"Score Blanc: {white_score}", True, BLACK), (810, y_offset + 155))

    return white_taken, black_taken, white_score, black_score


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

    font_title = pygame.font.SysFont("segoeui", 42)
    font_info = pygame.font.SysFont("segoeui", 26)

    y = 260
    screen.blit(font_title.render("Fin de la partie", True, (255, 255, 255)), (WIDTH // 2 - 150, y))
    y += 50
    screen.blit(font_info.render(f"{message}", True, (255, 255, 255)), (WIDTH // 2 - 200, y))
    y += 40
    screen.blit(font_info.render(f"Gagnant : {winner}", True, (200, 255, 200)), (WIDTH // 2 - 200, y))
    y += 40
    screen.blit(font_info.render(f"Score Blanc : {white_score}  |  Score Noir : {black_score}", True, (255, 255, 255)), (WIDTH // 2 - 200, y))
    y += 40
    screen.blit(font_info.render(f"Pièces capturées par les Blancs : {''.join(black_taken)}", True, (255, 255, 255)), (WIDTH // 2 - 200, y))
    y += 30
    screen.blit(font_info.render(f"Pièces capturées par les Noirs : {''.join(white_taken)}", True, (255, 255, 255)), (WIDTH // 2 - 200, y))

    # Bouton rejouer
    pygame.draw.rect(screen, (70, 70, 70), (WIDTH // 2 - 170, y + 50, 150, 40), border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 2 - 170, y + 50, 150, 40), width=2, border_radius=10)
    screen.blit(font_info.render("Rejouer", True, (255, 255, 255)), (WIDTH // 2 - 140, y + 58))

    # Bouton retour menu
    pygame.draw.rect(screen, (70, 70, 70), (WIDTH // 2 + 20, y + 50, 170, 40), border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 2 + 20, y + 50, 170, 40), width=2, border_radius=10)
    screen.blit(font_info.render("Retour au menu", True, (255, 255, 255)), (WIDTH // 2 + 30, y + 58))


def run_game(difficulty="easy", network=None, is_host=False):
    from ui.menu import run_menu
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Crimson Nexus – Partie")
    clock = pygame.time.Clock()

    def reset_game():
        return Board(), None, None, [], False, "", None, False, None

    board, selected_piece, selected_pos, legal_moves, game_over, message, winner, ai_thinking, ai_move = reset_game()

    load_images()

    def receive_move(move):
        board.move_piece(move)

    if difficulty == "online":
        network.on_receive = receive_move

    running = True

    def ai_logic():
        nonlocal ai_move, ai_thinking
        ai_move = get_random_move(board)
        ai_thinking = False

    while running:
        clock.tick(60)

        if not game_over and difficulty == "easy" and board.turn == "black":
            if not ai_thinking and ai_move is None:
                ai_thinking = True
                threading.Thread(target=ai_logic).start()
            elif ai_move:
                board.move_piece(ai_move)
                ai_move = None
                selected_piece = None
                selected_pos = None
                legal_moves = []

        draw_board(screen)
        highlight_squares(screen, selected_pos, legal_moves)
        draw_pieces(screen, board)
        draw_move_history(screen, board.move_history)
        white_taken, black_taken, white_score, black_score = draw_captured(screen, board.move_history)

        if not game_over and board.is_in_check(board.turn):
            show_check_popup(screen)

        if not game_over:
            if board.is_checkmate(board.turn):
                winner = "Blancs" if board.turn == "black" else "Noirs"
                message = f"{winner} gagnent par échec et mat"
                game_over = True
            elif board.is_stalemate(board.turn):
                message = "Match nul par pat"
                winner = "Aucun"
                game_over = True

        if game_over:
            show_end_screen(screen, message, winner, white_taken, black_taken, white_score, black_score)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif game_over and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if WIDTH // 2 - 170 <= x <= WIDTH // 2 - 20 and HEIGHT - 90 <= y <= HEIGHT - 50:
                    board, selected_piece, selected_pos, legal_moves, game_over, message, winner, ai_thinking, ai_move = reset_game()
                elif WIDTH // 2 + 20 <= x <= WIDTH // 2 + 190 and HEIGHT - 90 <= y <= HEIGHT - 50:
                    return run_menu()

            elif not game_over and event.type == pygame.MOUSEBUTTONDOWN and not ai_thinking:
                x, y = pygame.mouse.get_pos()
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE
                if col >= 8:
                    continue
                clicked_pos = (row, col)
                clicked_piece = board.get_piece(clicked_pos)

                if selected_piece:
                    move_made = False
                    for move in legal_moves:
                        if move.end_pos == clicked_pos:
                            board.move_piece(move)
                            if difficulty == "online" and network:
                                network.send(move)
                            move_made = True
                            break

                    selected_piece = None
                    selected_pos = None
                    legal_moves = []

                    if not move_made and clicked_piece and clicked_piece.color == board.turn:
                        selected_piece = clicked_piece
                        selected_pos = clicked_pos
                        legal_moves = board.get_valid_moves(selected_piece)
                else:
                    if clicked_piece and clicked_piece.color == board.turn:
                        selected_piece = clicked_piece
                        selected_pos = clicked_pos
                        legal_moves = board.get_valid_moves(selected_piece)

    pygame.quit()
