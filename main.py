import numpy as np

BLACK = 1
WHITE = -1
EMPTY = 0
PLAYER_NAME_BLACK = "Player1(黒)"
PLAYER_NAME_WHITE = "Player2(白)"
COLUMN_LABELS = ["A", "B", "C", "D", "E", "F", "G", "H"]

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

class Board:
    def __init__(self):
        self.board = self.create_board()  # ボードの初期化

    # 初期のボード状態を作成
    def create_board(self):
        board = np.zeros((8, 8), dtype=int)
        board[3][3], board[4][4] = WHITE, WHITE
        board[3][4], board[4][3] = BLACK, BLACK
        return board

    
    # 指定した座標がボードの範囲内かどうかをチェック
    def is_on_board(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    # 石を挟める座標リストを取得する
    def get_stones_to_flip(self, row, col, current_color):
        opponent_color = -current_color
        stones_to_flip = []

        for d_row, d_col in DIRECTIONS:
            n_row, n_col = row + d_row, col + d_col
            temp_flip = []

            while self.is_on_board(n_row, n_col) and self.board[n_row][n_col] == opponent_color:
                temp_flip.append((n_row, n_col))
                n_row += d_row
                n_col += d_col

            if self.is_on_board(n_row, n_col) and self.board[n_row][n_col] == current_color and temp_flip:
                stones_to_flip.extend(temp_flip)

        return stones_to_flip

    # 石を置いて反転させる
    def place_and_flip_stones(self, row, col, current_color):
        stones_to_flip = self.get_stones_to_flip(row, col, current_color)

        if not stones_to_flip:
            return False

        self.board[row][col] = current_color
        for flip_row, flip_col in stones_to_flip:
            self.board[flip_row][flip_col] = current_color

        return True

    # 現在のプレイヤーがボード上に石を置けるかどうかチェック
    def find_valid_positions(self, current_color):
        valid_positions = []
        for row in range(8):
            for col in range(8):
                if self.can_flip(row, col, current_color):
                    valid_positions.append((row, col))
        return valid_positions

    # 石を挟めるかどうかを確認する
    def can_flip(self, row, col, current_color):
        if self.board[row][col] != EMPTY:
            return False
        return len(self.get_stones_to_flip(row, col, current_color)) > 0

    # ボードを表示する
    def print_board(self, valid_positions=None):
        symbols = {
            EMPTY: "□",  # 空
            BLACK: "○",  # 黒
            WHITE: "●",  # 白
            "HINT": "⊡"  # 有効な手(ヒント)
        }

        for row in range(8):
            row_symbols = []
            for col in range(8):
                if valid_positions and (row, col) in valid_positions:
                    row_symbols.append(symbols["HINT"])
                else:
                    row_symbols.append(symbols[self.board[row][col]])
            print(" ".join(row_symbols) + f" {row}")

        print(" ".join(COLUMN_LABELS))


class Player:
    def __init__(self, name, color):
        self.name = name  # プレイヤー名
        self.color = color  # プレイヤーの色

    # 現在のプレイヤーの有効な手を取得
    def get_valid_moves(self, board):
        return board.find_valid_positions(self.color)


class Game:
    def __init__(self):
        self.board = Board()  # ボードの作成
        self.players = [
            Player(PLAYER_NAME_BLACK, BLACK),
            Player(PLAYER_NAME_WHITE, WHITE)
        ]
        self.current_player_index = 0  # 最初のプレイヤー

    # ターンを交代する
    def switch_turn(self):
        self.current_player_index = 1 - self.current_player_index

    # ゲームのメインループ
    def play(self):
        while True:
            current_player = self.players[self.current_player_index]
            valid_positions = current_player.get_valid_moves(self.board)
            self.board.print_board(valid_positions)

            if not valid_positions:
                print(f"{current_player.name}は有効な手がありません。")
                self.switch_turn()
                if not self.players[1 - self.current_player_index].get_valid_moves(self.board):
                    print("ゲーム終了！")
                    break
                continue

            print(f"\n{current_player.name}のターンです:")
            valid_positions_str = [f"{COLUMN_LABELS[col]}-{row}" for row, col in valid_positions]
            print(f"有効な手: {', '.join(valid_positions_str)}")

            try:
                user_input = input("列と行を入力してください (例: A-2): ")
                col_char, row = user_input.split('-')
                col = COLUMN_LABELS.index(col_char.upper())
                row = int(row)
            except (ValueError, IndexError):
                print("無効な入力です！")
                continue

            if self.board.is_on_board(row, col) and self.board.place_and_flip_stones(row, col, current_player.color):
                self.switch_turn()
            else:
                print("無効な手です。もう一度試してください！")

        # 結果の表示
        self.board.print_board()
        black_count = np.sum(self.board.board == BLACK)
        white_count = np.sum(self.board.board == WHITE)

        if black_count > white_count:
            result = f"勝利: {PLAYER_NAME_BLACK}"
        elif white_count > black_count:
            result = f"勝利: {PLAYER_NAME_WHITE}"
        else:
            result = "引き分け"

        print(f"最終スコア: {PLAYER_NAME_BLACK} {black_count}, {PLAYER_NAME_WHITE} {white_count}")
        print(result)


if __name__ == "__main__":
    game = Game()  # ゲームを開始
    game.play()
