import pygame
from core.board import Board
from core.move import Move

from ai.base_ai import get_random_move
from ai.minimax import get_minimax_move
from ai.evaluator import get_best_move_alphabeta
from network.network import GameServer, GameClient

# === Constantes ===
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8
PIECE_IMAGES = {}

# === Couleurs ===
WHITE = (245, 245, 245)
GRAY = (160, 160, 160)
GREEN = (50, 200, 50)
HIGHLIGHT = (0, 150, 255)

# === Chargement des images de pièces ===
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


def run_game(difficulty="easy", network=None, is_host=False):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Crimson Nexus – Partie en cours")
    clock = pygame.time.Clock()

    board = Board()
    selected_piece = None
    selected_pos = None
    legal_moves = []

    load_images()

    def receive_move(move):
        board.move_piece(move)

    if difficulty == "online":
        if is_host:
            network.on_receive = receive_move
        else:
            network.on_receive = receive_move

    running = True
    while running:
        clock.tick(60)

        # === IA (noir)
        if difficulty in ["easy", "normal", "hard"] and board.turn == "black":
            if difficulty == "easy":
                move = get_random_move(board)
            elif difficulty == "normal":
                move = get_minimax_move(board, depth=2)
            elif difficulty == "hard":
                move = get_best_move_alphabeta(board, depth=3)
            else:
                move = None

            if move:
                board.move_piece(move)
                selected_piece = None
                selected_pos = None
                legal_moves = []

        draw_board(screen)
        highlight_squares(screen, selected_pos, legal_moves)
        draw_pieces(screen, board)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE
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
                        legal_moves = selected_piece.get_legal_moves(board)

                else:
                    if clicked_piece and clicked_piece.color == board.turn:
                        selected_piece = clicked_piece
                        selected_pos = clicked_pos
                        legal_moves = selected_piece.get_legal_moves(board)

    pygame.quit()
