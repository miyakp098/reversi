# 定数宣言
BLACK = 1
WHITE = -1
EMPTY = 0

DIRECTIONS = [
    (0, 1),   # 右 (Right)
    (1, 0),   # 下 (Down)
    (0, -1),  # 左 (Left)
    (-1, 0),  # 上 (Up)
    (1, 1),   # 右下 (Down-right)
    (1, -1),  # 左下 (Down-left)
    (-1, 1),  # 右上 (Up-right)
    (-1, -1)  # 左上 (Up-left)
]

# 8x8のボードの初期状態を作成
def create_board():
    board = [[EMPTY] * 8 for _ in range(8)]
    board[3][3], board[4][4] = WHITE, WHITE
    board[3][4], board[4][3] = BLACK, BLACK
    return board

# ボードを表示する
def print_board(board):
    symbols = {
        EMPTY: "□",  # 空
        BLACK: "○",  # 黒
        WHITE: "●"   # 白
    }
    
    for row in board:
        row_symbols = [symbols[cell] for cell in row]
        print(" ".join(row_symbols))

# 指定した座標がボードの範囲内かどうかをチェック
def is_on_board(x, y):
    return 0 <= x < 8 and 0 <= y < 8

# 石を挟めるかどうかを確認する
def can_flip(board, x, y, current_color):
    if board[x][y] != EMPTY:
        return False
    
    opponent_color = -current_color
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        stones_to_flip = []
        while is_on_board(nx, ny) and board[nx][ny] == opponent_color:
            stones_to_flip.append((nx, ny))
            nx += dx
            ny += dy
        if is_on_board(nx, ny) and board[nx][ny] == current_color and stones_to_flip:
            return True
    return False

# 石を置いて反転させる
def make_move(board, x, y, current_color):
    if not can_flip(board, x, y, current_color):
        return False
    
    opponent_color = -current_color
    board[x][y] = current_color
    
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        stones_to_flip = []
        while is_on_board(nx, ny) and board[nx][ny] == opponent_color:
            stones_to_flip.append((nx, ny))
            nx += dx
            ny += dy
        if is_on_board(nx, ny) and board[nx][ny] == current_color:
            for flip_x, flip_y in stones_to_flip:
                board[flip_x][flip_y] = current_color
    return True

def has_valid_moves(board, current_color):
    return any(can_flip(board, x, y, current_color) for x in range(8) for y in range(8))

def get_valid_moves(board, current_color):
    return [(x, y) for x in range(8) for y in range(8) if can_flip(board, x, y, current_color)]

# ゲーム開始
def game_loop():
    board = create_board()
    current_color = BLACK  # ゲーム開始は黒から
    
    while True:
        print_board(board)

        # 現在のプレイヤーに有効な手がなければターンを交代
        if not has_valid_moves(board, current_color):
            print(f"{'黒' if current_color == BLACK else '白'}は有効な手がありません")
            current_color = -current_color

            # 交代後のプレイヤーも有効な手がなければゲーム終了
            if not has_valid_moves(board, current_color):
                print("ゲーム終了！")
                break
            continue
        
        print(f"\n{'黒' if current_color == BLACK else '白'}のターンです:")
        
        # 有効な手を表示
        valid_moves = get_valid_moves(board, current_color)
        print(f"有効な手: {', '.join(f'{x}-{y}' for x, y in valid_moves)}")
        
        try:
            x, y = map(int, input("行と列を入力してください (例: 2-1): ").split('-'))
        except ValueError:
            print("無効な入力です！")
            continue

        if is_on_board(x, y) and make_move(board, x, y, current_color):
            current_color = -current_color
        else:
            print("無効な手です。もう一度試してください！")

    # ゲーム終了後の結果表示
    print_board(board)
    black_count = sum(row.count(BLACK) for row in board)
    white_count = sum(row.count(WHITE) for row in board)
    print(f"最終スコア: 黒 {black_count}, 白 {white_count}")
    print("勝利:", "黒" if black_count > white_count else "白" if white_count > black_count else "引き分け")

# ゲーム開始
game_loop()
