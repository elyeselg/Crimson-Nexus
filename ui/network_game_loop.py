import pygame
from core.board import Board
from core.move import Move
from ui.draw import (
    load_images, draw_board, draw_pieces, highlight_squares,
    draw_move_history, draw_captured,
    show_check_popup, show_end_screen
)

WIDTH, HEIGHT = 1000, 800
SQUARE_SIZE = 800 // 8

def run_network_game(network, is_host=False):
    import ui.menu

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Crimson Nexus – Partie en ligne")
    clock = pygame.time.Clock()

    board = Board()
    selected_piece = None
    selected_pos = None
    legal_moves = []
    game_over = False
    message = ""
    winner = None
    button_replay = None
    button_menu = None

    load_images()

    my_color = "white" if is_host else "black"
    waiting_for_opponent = not is_host

    def receive_move(move):
        nonlocal waiting_for_opponent, selected_piece, selected_pos, legal_moves
        board.move_piece(move)
        waiting_for_opponent = False
        selected_piece = None
        selected_pos = None
        legal_moves = []

    def is_insufficient_material(board):
        pieces = [p for row in board.board for p in row if p]
        if len(pieces) == 2:
            return True  # Roi contre Roi
        if len(pieces) == 3:
            types = [p.__class__.__name__ for p in pieces]
            if "Bishop" in types or "Knight" in types:
                return True  # Roi contre Roi + (Fou ou Cavalier)
        if len(pieces) == 4:
            types = [p.__class__.__name__ for p in pieces]
            if types.count("Bishop") == 2:
                bishops = [p for p in pieces if p.__class__.__name__ == "Bishop"]
                colors = [(b.pos[0] + b.pos[1]) % 2 for b in bishops]
                if colors[0] == colors[1]:
                    return True  # Deux fous sur même couleur
        return False

    network.on_receive = receive_move

    running = True
    while running:
        clock.tick(60)

        # --- AFFICHAGE ---
        draw_board(screen)
        highlight_squares(screen, selected_pos, legal_moves)
        draw_pieces(screen, board)
        draw_move_history(screen, board.move_history)
        white_taken, black_taken, white_score, black_score = draw_captured(screen, board.move_history)

        if not game_over and board.is_in_check(board.turn):
            show_check_popup(screen)

        # --- DETECTION FIN DE PARTIE ---
        if not game_over:
            if board.is_checkmate(board.turn):
                winner = "Blancs" if board.turn == "black" else "Noirs"
                message = f"{winner} gagnent par échec et mat"
                game_over = True
            elif board.is_stalemate(board.turn):
                winner = "Aucun"
                message = "Match nul par pat"
                game_over = True
            elif is_insufficient_material(board):
                winner = "Aucun"
                message = "Match nul par matériel insuffisant"
                game_over = True

        # --- AFFICHER ECRAN DE FIN ---
        if game_over and button_replay is None and button_menu is None:
            button_replay, button_menu = show_end_screen(screen, message, winner, white_taken, black_taken, white_score, black_score)
            pygame.display.update()

            # 🔥 Bloquer ici jusqu'à clic
            waiting_click = True
            while waiting_click:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        if button_replay and button_replay.collidepoint(x, y):
                            return run_network_game(network, is_host)
                        elif button_menu and button_menu.collidepoint(x, y):
                            return ui.menu.run_menu(screen)

                pygame.display.flip()

        pygame.display.flip()

        # --- GESTION DES EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif not game_over and not waiting_for_opponent and event.type == pygame.MOUSEBUTTONDOWN:
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
                            network.send(move)
                            waiting_for_opponent = True
                            move_made = True
                            break

                    selected_piece = None
                    selected_pos = None
                    legal_moves = []

                    if not move_made and clicked_piece and clicked_piece.color == my_color:
                        selected_piece = clicked_piece
                        selected_pos = clicked_pos
                        legal_moves = board.get_valid_moves(selected_piece)
                else:
                    if clicked_piece and clicked_piece.color == my_color:
                        selected_piece = clicked_piece
                        selected_pos = clicked_pos
                        legal_moves = board.get_valid_moves(selected_piece)

    pygame.quit()
