import random
import numpy as np
from abc import ABC, abstractmethod


BLACK = 1
WHITE = -1
EMPTY = 0
HUMAN_PLAYER_NAME = "HumanPlayer"
POSITION_PRIORITY_EASY_CPU_NAME = "EasyPosCPU"
POSITION_PRIORITY_HARD_CPU_NAME = "HardPosCPU"
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
    """ゲームボードを管理するクラス。

    Attributes:
        board (np.ndarray): ボードの状態を表す2次元配列。
    """

    def __init__(self):
        """ボードを初期化し、初期状態を設定する。"""
        self.board = self.create_board()

    def create_board(self):
        """初期のボード状態を作成。

        Returns:
            np.ndarray: 初期状態のボード。
        """
        board = np.zeros((8, 8), dtype=int)
        board[3][3], board[4][4] = WHITE, WHITE
        board[3][4], board[4][3] = BLACK, BLACK
        return board
    
    def print_board(self, valid_positions=None):
        """ボードの状態を表示する。

        Args:
            valid_positions (list, optional): 有効な手の座標リスト。デフォルトはNone。
        """
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
        
    def find_valid_positions(self, current_color):
        """現在のプレイヤーが置ける有効な手を全て見つけ、ひっくり返せる石の数も格納する。

        Args:
            current_color (int): 現在のプレイヤーの色。

        Returns:
            dict: 有効な手の座標とひっくり返せる石の数の辞書。
        """
        valid_positions = {}
        for row in range(8):
            for col in range(8):
                flip_count = self.get_flip_count(row, col, current_color)
                if flip_count > 0:
                    valid_positions[(row, col)] = flip_count
        return valid_positions


    def place_and_flip_stones(self, row, col, current_color):
        """指定した位置に石を置き、挟む石を反転させる。

        Args:
            row (int): 行のインデックス。
            col (int): 列のインデックス。
            current_color (int): 現在のプレイヤーの色。

        Returns:
            bool: 石を置いて反転できた場合はTrue、できなかった場合はFalse。
        """
        stones_to_flip, _ = self.get_stones_to_flip(row, col, current_color)

        if not stones_to_flip:
            return False

        self.board[row][col] = current_color
        for flip_row, flip_col in stones_to_flip:
            self.board[flip_row][flip_col] = current_color

        return True
    
    
    def get_flip_count(self, row, col, current_color):
        """指定した位置で石を挟むことができるか確認し、ひっくり返せる石の数を返す。

        Args:
            row (int): 行のインデックス。
            col (int): 列のインデックス。
            current_color (int): 現在のプレイヤーの色。

        Returns:
            int: ひっくり返せる石の数。挟めない場合は0を返す。
        """
        if self.board[row][col] != EMPTY:
            return 0

        _, flip_count = self.get_stones_to_flip(row, col, current_color)
        return flip_count  # ひっくり返せる石の数を返す
    
    def get_stones_to_flip(self, row, col, current_color):
        """指定した位置で挟むことができる石のリストとその数を取得。

        Args:
            row (int): 行のインデックス。
            col (int): 列のインデックス。
            current_color (int): 現在のプレイヤーの色。

        Returns:
            list: 挟むことができる石の座標リスト。
            int: ひっくり返せる石の数。
        """
        opponent_color = -current_color
        stones_to_flip = []

        for d_row, d_col in DIRECTIONS:
            n_row, n_col = row + d_row, col + d_col
            temp_flip = []

            # 相手の石が連続する限り、石をリストに追加
            while self.is_on_board(n_row, n_col) and self.board[n_row][n_col] == opponent_color:
                temp_flip.append((n_row, n_col))
                n_row += d_row
                n_col += d_col

            # 相手の石の後に自分の石があれば、それまでの石を全て反転リストに追加
            if self.is_on_board(n_row, n_col) and self.board[n_row][n_col] == current_color and temp_flip:
                stones_to_flip.extend(temp_flip)

        return stones_to_flip, len(stones_to_flip)
    
    def is_on_board(self, row, col):
        """指定した座標がボードの範囲内かどうかをチェック。

        Args:
            row (int): 行のインデックス。
            col (int): 列のインデックス。

        Returns:
            bool: 座標がボード内であればTrue、そうでなければFalse。
        """
        return 0 <= row < 8 and 0 <= col < 8

class Player(ABC):
    """プレイヤーの抽象クラス。"""

    def __init__(self, name, color):
        """プレイヤーの名前と色を初期化する。

        Args:
            name (str): プレイヤー名。
            color (int): プレイヤーの色。
        """
        self.name = name
        self.color = color

    @abstractmethod
    def get_valid_positions(self, board):
        """プレイヤーの手を取得する。

        Args:
            board (Board): ゲームボード。

        Returns:
            tuple: プレイヤーの選択した座標 (row, col)。
        """
        pass


class HumanPlayer(Player):
    """人間プレイヤーを表すクラス。"""

    def get_valid_positions(self, board):
        """人間プレイヤーからの手を取得する。

        Args:
            board (Board): ゲームボード。

        Returns:
            tuple: プレイヤーの選択した座標 (row, col)。
        """
        valid_positions = board.find_valid_positions(self.color)
        board.print_board(valid_positions)

        if not valid_positions:
            return None, None

        print(f"\n{self.name}のターンです:")
        valid_positions_str = [f"{COLUMN_LABELS[col]}-{row}" for row, col in valid_positions]
        print(f"有効な手: {', '.join(valid_positions_str)}")

        while True:
            try:
                user_input = input("列と行を入力してください (例: A-2): ")
                col_char, row = user_input.split('-')
                col = COLUMN_LABELS.index(col_char.upper())
                row = int(row)

                if board.is_on_board(row, col) and board.place_and_flip_stones(row, col, self.color):
                    return row, col
                else:
                    print("無効な手です。もう一度試してください！")
            except (ValueError, IndexError):
                print("無効な入力です！もう一度試してください。")
                
                
class CPUPlayer(Player):
    """CPUプレイヤーを表すクラス。"""

    # 8x8の優先度マトリクス（数字が大きいほど優先度が高い）
    priority_matrix = np.zeros((8, 8), dtype=int)

    def select_best_position(self, valid_positions):
        """最も優先度の高い手を選ぶ。

        Args:
            valid_positions (list of tuple): 有効な手のリスト

        Returns:
            tuple: 最も優先度の高い手
        """
        best_positions = []
        highest_priority = -1

        for position in valid_positions:
            row, col = position
            priority = self.priority_matrix[row][col]
            if priority > highest_priority:
                highest_priority = priority
                best_positions = [position]
            elif priority == highest_priority:
                best_positions.append(position)

        return random.choice(best_positions)

    def get_valid_positions(self, board):
        """CPUプレイヤーの手を取得する。

        Args:
            board (Board): ゲームボード。

        Returns:
            tuple: CPUが選択した座標 (row, col)。
        """
        valid_positions = board.find_valid_positions(self.color)

        if not valid_positions:
            return None, None

        best_position = self.select_best_position(valid_positions)
        board.place_and_flip_stones(best_position[0], best_position[1], self.color)
        print(f"{self.name} (CPU) は {COLUMN_LABELS[best_position[1]]}-{best_position[0]} に石を置きました。")
        return best_position


class PositionPriorityEasyCPU(CPUPlayer):
    priority_matrix = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]


class PositionPriorityHardCPU(CPUPlayer):
    priority_matrix = [
        [9, 4, 5, 5, 5, 5, 4, 9],
        [4, 0, 3, 3, 3, 3, 0, 4],
        [5, 3, 4, 4, 4, 4, 3, 5],
        [5, 3, 4, 4, 4, 4, 3, 5],
        [5, 3, 4, 4, 4, 4, 3, 5],
        [5, 3, 4, 4, 4, 4, 3, 5],
        [4, 0, 3, 3, 3, 3, 0, 4],
        [9, 4, 5, 5, 5, 5, 4, 9]
    ]


class Game:
    """オセロゲームを管理するクラス。"""

    def __init__(self):
        """ゲームを初期化し、ボードとプレイヤーを作成する。"""
        self.board = Board()
        self.current_player_color = BLACK  # 最初のプレイヤーの色

        self.set_players()

    def set_players(self):
        """プレイヤーの設定を行う。"""
        while True:
            game_mode = input("ゲームモードを選んでください:\n1: 人間対人間\n2: 人間対CPU\n3: CPU対CPU\n選択肢の番号を入力してください: ").strip()

            if game_mode == '1':
                self.setup_human_vs_human()
                break
            elif game_mode == '2':
                self.setup_human_vs_cpu()
                break
            elif game_mode == '3':
                self.setup_cpu_vs_cpu()
                break
            else:
                print("無効な選択です。もう一度選んでください。")

    def setup_human_vs_human(self):
        """人間同士のプレイヤーを設定する。"""
        player_name_black = f"{HUMAN_PLAYER_NAME}1"
        player_name_white = f"{HUMAN_PLAYER_NAME}2"
        self.players = [
            HumanPlayer(player_name_black, BLACK),
            HumanPlayer(player_name_white, WHITE)
        ]

    def setup_human_vs_cpu(self):
        """人間対CPUのプレイヤーを設定する。"""
        player_name_black = HUMAN_PLAYER_NAME
        player_name_white, cpu_class = self.select_cpu_player()
        
        # 選択したCPUレベルに応じてプレイヤーを設定
        self.players = [
            HumanPlayer(player_name_black, BLACK),
            cpu_class(player_name_white, WHITE)
        ]
        
    def setup_cpu_vs_cpu(self):
        """CPU同士のプレイヤーを設定する。"""
        # 黒と白のCPUプレイヤーをそれぞれ選択
        print("黒のCPUを選択します。")
        player_name_black, cpu_class_black = self.select_cpu_player()

        print("白のCPUを選択します。")
        player_name_white, cpu_class_white = self.select_cpu_player()
        
        # 選択したCPUレベルに応じてプレイヤーを設定
        self.players = [
            cpu_class_black(player_name_black, BLACK),
            cpu_class_white(player_name_white, WHITE)
        ]

    
    def select_cpu_player(self):
        """CPUプレイヤーのレベルとクラスを選択する。
        
        Returns:
            tuple: (player_name_white, cpu_class)
        """
        while True:
            # CPUレベルの選択を促す
            cpu_level = input(
                f"CPUレベルを選んでください:\n"
                f"1: {POSITION_PRIORITY_EASY_CPU_NAME}\n"
                f"2: {POSITION_PRIORITY_HARD_CPU_NAME}\n"
                f"選択肢の番号を入力してください: "
            ).strip()

            # CPUレベルに応じてクラスと名前を決定
            if cpu_level == '1':
                return POSITION_PRIORITY_EASY_CPU_NAME, PositionPriorityEasyCPU
            elif cpu_level == '2':
                return POSITION_PRIORITY_HARD_CPU_NAME, PositionPriorityHardCPU
            else:
                print("無効な選択です。もう一度選んでください。")

    def switch_turn(self):
        """ターンを交代する。"""
        self.current_player_color = WHITE if self.current_player_color == BLACK else BLACK

    def get_current_player(self):
        """現在のプレイヤーを取得する。

        Returns:
            Player: 現在のプレイヤー。
        """
        return next(player for player in self.players if player.color == self.current_player_color)

    def play(self):
        """ゲームのメインループを実行する。"""
        while True:
            current_player = self.get_current_player()

            if current_player.get_valid_positions(self.board) == (None, None):
                print(f"{current_player.name}は有効な手がありません。")
                self.switch_turn()
                if self.get_current_player().get_valid_positions(self.board) == (None, None):
                    print("ゲーム終了！")
                    break
                continue

            self.switch_turn()

        self.show_result()

    def show_result(self):
        """ゲーム結果を表示する。"""
        self.board.print_board()
        black_count = np.sum(self.board.board == BLACK)
        white_count = np.sum(self.board.board == WHITE)

        # プレイヤーの名前を取得
        player_name_black = self.players[0].name
        player_name_white = self.players[1].name

        if black_count > white_count:
            result = f"勝利: {player_name_black}"
        elif white_count > black_count:
            result = f"勝利: {player_name_white}"
        else:
            result = "引き分け"

        print(f"最終スコア: 黒: {player_name_black} {black_count}個, 白: {player_name_white} {white_count}個")
        print(result)


if __name__ == "__main__":
    Game().play()
