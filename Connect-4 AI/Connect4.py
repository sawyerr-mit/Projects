import pygame
import math
import sys
import os

ROWS, COLS = 6, 7
CELL = 145
WIDTH = COLS * CELL
HEIGHT = (ROWS + 1) * CELL

BLUE        = (30,  100, 200)
BLACK       = (10,   10,  10)
RED         = (220,  50,  50)
DARK_RED    = (184, 29, 29)
YELLOW      = (240, 200,  30)
DARK_YELLOW = (209, 163, 23)
WHITE       = (240, 240, 240)
GRAY        = (60,   60,  60)

EMPTY, P1, P2 = 0, 1, 2


def make_board():
    return [[EMPTY] * COLS for _ in range(ROWS)]


def drop(board, col, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            board[row][col] = player
            return row
    return -1


def undo(board, row, col):
    board[row][col] = EMPTY


def valid(board, col):
    return board[0][col] == EMPTY


def valid_moves(board):
    cols = list(range(COLS))
    return [c for c in cols if valid(board, c)]


def winner(board, row, col, player):
    for dr, dc in [(0,1),(1,0),(1,1),(1,-1)]:
        count = 1
        for sign in (1, -1):
            r, c = row + dr*sign, col + dc*sign
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
                r += dr*sign
                c += dc*sign
        if count >= 4:
            return True
    return False


def evaluate_window(a, b, c, d, player):
    score = 0
    opponent = P1 if player == P2 else P2

    pieces = [a, b, c, d]

    if pieces.count(player) == 4:
        return math.inf
    elif pieces.count(player) == 3 and pieces.count(EMPTY) == 1:
        score += 150
    elif pieces.count(player) == 2 and pieces.count(EMPTY) == 2:
        score += 15

    if pieces.count(opponent) == 3 and pieces.count(EMPTY) == 1:
        score -= 120

    return score


def evaluate(board, player):
    score = 0
    opponent = P1 if player == P2 else P2
    center = COLS // 2

    for r in range(ROWS):
        if board[r][center] == player:
            score += 10

    for r in range(ROWS):
        for c in range(COLS - 3):
            score += evaluate_window(
                board[r][c], board[r][c+1],
                board[r][c+2], board[r][c+3],
                player
            )

    for c in range(COLS):
        for r in range(ROWS - 3):
            score += evaluate_window(
                board[r][c], board[r+1][c],
                board[r+2][c], board[r+3][c],
                player
            )

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            score += evaluate_window(
                board[r][c], board[r+1][c+1],
                board[r+2][c+2], board[r+3][c+3],
                player
            )

    for r in range(ROWS - 3):
        for c in range(3, COLS):
            score += evaluate_window(
                board[r][c], board[r+1][c-1],
                board[r+2][c-2], board[r+3][c-3],
                player
            )

    return score


def order_moves(board, cols, player):
    opponent = P1 if player == P2 else P2

    winning, blocking, center, others = [], [], [], []

    for col in cols:
        row = drop(board, col, player)
        if row != -1 and winner(board, row, col, player):
            undo(board, row, col)
            winning.append(col)
            continue
        undo(board, row, col)

        row = drop(board, col, opponent)
        if row != -1 and winner(board, row, col, opponent):
            undo(board, row, col)
            blocking.append(col)
            continue
        undo(board, row, col)

        if col == COLS // 2:
            center.append(col)
        else:
            others.append(col)

    return winning + blocking + center + others


def minimax(board, depth, alpha, beta, maximizing, player):
    opponent = P1 if player == P2 else P2

    valid_cols = valid_moves(board)
    if not valid_cols:
        return 0, None

    for col in valid_cols:
        row = drop(board, col, player if maximizing else opponent)
        if row != -1:
            if winner(board, row, col, player if maximizing else opponent):
                undo(board, row, col)
                return (math.inf, col) if maximizing else (-math.inf, col)
            undo(board, row, col)

    if depth == 0:
        return evaluate(board, player), None

    valid_cols = sorted(valid_cols, key=lambda c: abs(c - COLS // 2))
    best_col = valid_cols[0]

    if maximizing:
        value = -math.inf

        for col in valid_cols:
            row = drop(board, col, player)
            if row == -1:
                continue

            score, _ = minimax(board, depth - 1, alpha, beta, False, player)
            undo(board, row, col)

            if score > value:
                value = score
                best_col = col

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return value, best_col

    else:
        value = math.inf

        for col in valid_cols:
            row = drop(board, col, opponent)
            if row == -1:
                continue

            score, _ = minimax(board, depth - 1, alpha, beta, True, player)
            undo(board, row, col)

            if score < value:
                value = score
                best_col = col

            beta = min(beta, value)
            if alpha >= beta:
                break

        return value, best_col


def draw(screen, board, font, hover_col, current_player):
    screen.fill(BLACK)

    color = RED if current_player == P1 else YELLOW
    cx = hover_col * CELL + CELL // 2
    pygame.draw.circle(screen, DARK_RED if color is RED else DARK_YELLOW, (cx, CELL // 2), CELL // 2 - 8)
    pygame.draw.circle(screen, color, (cx, CELL // 2), 0.8 * CELL // 2 - 8)

    pygame.draw.rect(screen, BLUE, (0, CELL, WIDTH, ROWS * CELL))
    for r in range(ROWS):
        for c in range(COLS):
            ring_color = BLACK
            if board[r][c] == P1:
                ring_color = DARK_RED
            elif board[r][c] == P2:
                ring_color = DARK_YELLOW
            cx = c * CELL + CELL // 2
            cy = (r + 1) * CELL + CELL // 2
            pygame.draw.circle(screen, ring_color, (cx, cy), CELL // 2 - 8)
            if ring_color is not BLACK:
                pygame.draw.circle(screen, RED if ring_color is DARK_RED else YELLOW,(cx, cy), 0.8*CELL // 2 - 8)

    pygame.display.flip()


def show_message(screen, font, text):
    screen.fill(BLACK)
    surf = font.render(text, True, WHITE)
    rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(surf, rect)
    small = pygame.font.SysFont(None, 32)
    sub = small.render("Click to play again", True, GRAY)
    screen.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))
    pygame.display.flip()


def main():
    # Run relative to this file so the sound files are found from any working directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    HUMAN = P1

    pygame.init()
    pygame.mixer.init()
    piece_played = pygame.mixer.Sound("place.wav")
    you_lose = pygame.mixer.Sound("lose.wav")
    start = pygame.mixer.Sound("new_game.mp3")
    victory = pygame.mixer.Sound("victory.mp3")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect Four")
    font = pygame.font.SysFont(None, 64)
    clock = pygame.time.Clock()

    AI = P2 if HUMAN == P1 else P1

    def new_game():
        start.play()
        return make_board(), P1, False

    board, current, game_over = new_game()
    hover_col = COLS // 2

    def do_ai_move(board, current):
        draw(screen, board, font, hover_col, current)
        _, col = minimax(board, 10, -math.inf, math.inf, True, AI)
        row = drop(board, col, AI)
        piece_played.play()

        if winner(board, row, col, AI):
            you_lose.play()
            draw(screen, board, font, hover_col, current)
            show_message(screen, font, "AI wins! You Lose :(")
            return True

        if not valid_moves(board):
            draw(screen, board, font, hover_col, current)
            show_message(screen, font, "Draw!")
            return True

        return False

    if current == AI:
        game_over = do_ai_move(board, current)
        current = HUMAN

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    board, current, game_over = new_game()
                    hover_col = COLS // 2

                    if current == AI:
                        game_over = do_ai_move(board, current)
                        current = HUMAN
                continue

            if event.type == pygame.MOUSEMOTION:
                hover_col = min(event.pos[0] // CELL, COLS - 1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // CELL
                if not valid(board, col):
                    continue

                row = drop(board, col, HUMAN)
                piece_played.play()

                if winner(board, row, col, HUMAN):
                    victory.play()
                    draw(screen, board, font, hover_col, current)
                    show_message(screen, font, "You win!")
                    game_over = True
                    continue

                if not valid_moves(board):
                    draw(screen, board, font, hover_col, current)
                    show_message(screen, font, "Draw!")
                    game_over = True
                    continue

                current = AI
                game_over = do_ai_move(board, current)
                current = HUMAN

        if not game_over:
            draw(screen, board, font, hover_col, current)

        clock.tick(60)


if __name__ == "__main__":
    main()