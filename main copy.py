import numpy as np

# 8x8のボードの初期状態を作成（0:空、1:黒、-1:白）
def create_board():
    board = np.zeros((8, 8), dtype=int)
    board[3][3], board[4][4] = -1, -1  # 白
    board[3][4], board[4][3] = 1, 1    # 黒
    return board

# ボードを表示する
def print_board(board):
    print("\n".join(" ".join(["□" if cell == 0 else "●" if cell == 1 else "○" for cell in row]) for row in board))

# 方向ベクトル
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

# 指定した座標がボードの範囲内かどうかをチェック
def is_on_board(x, y):
    return 0 <= x < 8 and 0 <= y < 8

# 石を挟めるかどうかを確認する
def can_flip(board, x, y, color):
    if board[x][y] != 0:
        return False
    
    opponent = -color
    valid = False
    
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        stones_to_flip = []
        while is_on_board(nx, ny) and board[nx][ny] == opponent:
            stones_to_flip.append((nx, ny))
            nx += dx
            ny += dy
        if is_on_board(nx, ny) and board[nx][ny] == color and len(stones_to_flip) > 0:
            valid = True
            break
    return valid

# 石を置いて反転させる
def make_move(board, x, y, color):
    if not can_flip(board, x, y, color):
        return False
    
    opponent = -color
    board[x][y] = color
    
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        stones_to_flip = []
        while is_on_board(nx, ny) and board[nx][ny] == opponent:
            stones_to_flip.append((nx, ny))
            nx += dx
            ny += dy
        if is_on_board(nx, ny) and board[nx][ny] == color:
            for flip_x, flip_y in stones_to_flip:
                board[flip_x][flip_y] = color
    return True

# ゲームループ
def game_loop():
    board = create_board()
    current_color = 1  # 1:黒、-1:白

    while True:
        print_board(board)
        if not any(can_flip(board, x, y, current_color) for x in range(8) for y in range(8)):
            print("No valid moves for", "Black" if current_color == 1 else "White")
            current_color = -current_color
            if not any(can_flip(board, x, y, current_color) for x in range(8) for y in range(8)):
                print("Game Over!")
                break
            continue

        print(f"\n{'Black' if current_color == 1 else 'White'}'s turn:")
        try:
            x, y = map(int, input("Enter row and column (0-7, space-separated): ").split())
        except ValueError:
            print("Invalid input!")
            continue

        if is_on_board(x, y) and make_move(board, x, y, current_color):
            current_color = -current_color
        else:
            print("Invalid move, try again!")

    print_board(board)
    black_count = np.sum(board == 1)
    white_count = np.sum(board == -1)
    print(f"Final Score: Black {black_count}, White {white_count}")
    print("Winner:", "Black" if black_count > white_count else "White" if white_count > black_count else "Draw")

# ゲーム開始
game_loop()
