import numpy as np

# 定数宣言
BLACK = 1
WHITE = -1
EMPTY = 0

DIRECTIONS = np.array([
    (0, 1),   # 右 (Right)
    (1, 0),   # 下 (Down)
    (0, -1),  # 左 (Left)
    (-1, 0),  # 上 (Up)
    (1, 1),   # 右下 (Down-right)
    (1, -1),  # 左下 (Down-left)
    (-1, 1),  # 右上 (Up-right)
    (-1, -1)  # 左上 (Up-left)
])

# 8x8のボードの初期状態を作成
def create_board():
    board = np.zeros((8, 8), dtype=int)
    board[3][3], board[4][4] = WHITE, WHITE
    board[3][4], board[4][3] = BLACK, BLACK
    return board

# 指定した座標がボードの範囲内かどうかをチェック
def is_on_board(row, col):
    return 0 <= row < 8 and 0 <= col < 8

# 石を挟める座標リストを取得する
def get_stones_to_flip(board, row, col, current_color):
    opponent_color = -current_color
    stones_to_flip = []
    
    for d_row, d_col in DIRECTIONS:
        n_row, n_col = row + d_row, col + d_col
        temp_flip = []
        
        while is_on_board(n_row, n_col) and board[n_row][n_col] == opponent_color:
            temp_flip.append((n_row, n_col))
            n_row += d_row
            n_col += d_col
        
        if is_on_board(n_row, n_col) and board[n_row][n_col] == current_color and temp_flip:
            stones_to_flip.extend(temp_flip)
    
    return stones_to_flip

# 石を挟めるかどうかを確認する
def can_flip(board, row, col, current_color):
    if board[row][col] != EMPTY:
        return False
    # 挟める石があるか確認
    return len(get_stones_to_flip(board, row, col, current_color)) > 0

# 石を置いて反転させる
def place_and_flip_stones(board, row, col, current_color):
    stones_to_flip = get_stones_to_flip(board, row, col, current_color)
    
    if not stones_to_flip:
        return False
    
    board[row][col] = current_color
    # 反転させる
    for flip_row, flip_col in stones_to_flip:
        board[flip_row][flip_col] = current_color
    
    return True

# 現在のプレイヤーがボード上に石を置けるかどうかチェック
def can_place_stone(board, current_color):
    for row in range(8):
        for col in range(8):
            if can_flip(board, row, col, current_color):
                return True
    return False

# 現在のプレイヤーが石を置ける全ての有効な場所をリストとして返す
def find_valid_positions(board, current_color):
    valid_positions = []
    for row in range(8):
        for col in range(8):
            if can_flip(board, row, col, current_color):
                valid_positions.append((row, col))
    return valid_positions

# ボードを表示する
def print_board(board, valid_positions=None):
    symbols = {
        EMPTY: "□",  # 空
        BLACK: "○",  # 黒
        WHITE: "●",   # 白
        "HINT": "⊡"  # 有効な手(ヒント)
    }
    
    for row in range(8):
        row_symbols = []
        for col in range(8):
            if valid_positions and (row, col) in valid_positions:
                row_symbols.append(symbols["HINT"])
            else:
                row_symbols.append(symbols[board[row][col]])
        print(" ".join(row_symbols))

# ゲーム開始
def game_loop():
    board = create_board()
    current_color = BLACK  # ゲーム開始は黒から
    
    while True:
        # 有効な手を取得
        valid_positions = find_valid_positions(board, current_color)

        # ボードを表示
        print_board(board, valid_positions)

        # 現在のプレイヤーに有効な手がなければターンを交代
        if not can_place_stone(board, current_color):
            print(f"{'黒' if current_color == BLACK else '白'}は有効な手がありません")
            current_color = -current_color

            # 交代後のプレイヤーも有効な手がなければゲーム終了
            if not can_place_stone(board, current_color):
                print("ゲーム終了！")
                break
            continue
        
        print(f"\n{'黒' if current_color == BLACK else '白'}のターンです:")
        
        # 有効な手を表示
        valid_positions = find_valid_positions(board, current_color)
        print(f"有効な手: {', '.join(f'{row}-{col}' for row, col in valid_positions)}")
        
        try:
            row, col = map(int, input("行と列を入力してください (例: 2-1): ").split('-'))
        except ValueError:
            print("無効な入力です！")
            continue

        if is_on_board(row, col) and place_and_flip_stones(board, row, col, current_color):
            current_color = -current_color
        else:
            print("無効な手です。もう一度試してください！")

    # ゲーム終了後の結果表示
    print_board(board)
    black_count = np.sum(board == BLACK)
    white_count = np.sum(board == WHITE)
    
    # 勝者の判定
    if black_count > white_count:
        result = "勝利:黒"
    elif white_count > black_count:
        result = "勝利:白"
    else:
        result = "引き分け"

    print(f"最終スコア: 黒 {black_count}, 白 {white_count}")
    print(result)

# ゲーム開始
game_loop()
