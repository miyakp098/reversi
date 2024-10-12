import random
import numpy as np
from abc import ABC, abstractmethod


BLACK = 1
WHITE = -1
EMPTY = 0
HUMAN_PLAYER_NAME = "HumanPlayer"
EASY_AI_PLAYER_NAME = "EasyAIPlayer"
HARD_AI_PLAYER_NAME = "HardAIPlayer"
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
        """現在のプレイヤーが置ける有効な手を全て見つける。

        Args:
            current_color (int): 現在のプレイヤーの色。

        Returns:
            list: 有効な手の座標リスト。
        """
        valid_positions = []
        for row in range(8):
            for col in range(8):
                if self.can_flip(row, col, current_color):
                    valid_positions.append((row, col))
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
        stones_to_flip = self.get_stones_to_flip(row, col, current_color)

        if not stones_to_flip:
            return False

        self.board[row][col] = current_color
        for flip_row, flip_col in stones_to_flip:
            self.board[flip_row][flip_col] = current_color

        return True
    
    
    def can_flip(self, row, col, current_color):
        """指定した位置で石を挟むことができるか確認する。

        Args:
            row (int): 行のインデックス。
            col (int): 列のインデックス。
            current_color (int): 現在のプレイヤーの色。

        Returns:
            bool: 石を挟むことができればTrue、そうでなければFalse。
        """
        if self.board[row][col] != EMPTY:
            return False
        return len(self.get_stones_to_flip(row, col, current_color)) > 0
    
    def get_stones_to_flip(self, row, col, current_color):
        """指定した位置で挟むことができる石のリストを取得。

        Args:
            row (int): 行のインデックス。
            col (int): 列のインデックス。
            current_color (int): 現在のプレイヤーの色。

        Returns:
            list: 挟むことができる石の座標リスト。
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

        return stones_to_flip
    
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
                
                
class AIPlayer(Player):
    """AIプレイヤーを表すクラス。"""

    # 8x8の優先度マトリクス（数字が大きいほど優先度が高い）
    priority_matrix = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    def get_valid_positions(self, board):
        """AIプレイヤーの手を取得する。

        Args:
            board (Board): ゲームボード。

        Returns:
            tuple: AIが選択した座標 (row, col)。
        """
        valid_positions = board.find_valid_positions(self.color)

        if not valid_positions:
            return None, None

        # 優先度が最も高い位置を選ぶためのリストを用意
        best_positions = []
        highest_priority = -1

        # 各位置の優先度を確認して、同じ優先度の手をリストに追加
        for position in valid_positions:
            row, col = position
            priority = self.priority_matrix[row][col]
            if priority > highest_priority:
                highest_priority = priority
                best_positions = [position]  # 新しい最高優先度が見つかったらリストをリセット
            elif priority == highest_priority:
                best_positions.append(position)  # 同じ優先度ならリストに追加

        # 複数の最高優先度の手からランダムに選ぶ
        best_position = random.choice(best_positions)

        # 選択された手をボードに反映
        board.place_and_flip_stones(best_position[0], best_position[1], self.color)
        print(f"{self.name} (AI) は {COLUMN_LABELS[best_position[1]]}-{best_position[0]} に石を置きました。")
        return best_position
    

class EasyAIPlayer(AIPlayer):
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


class HardAIPlayer(AIPlayer):
    """より高度な手を選ぶ難しいAIプレイヤー。"""
    
    priority_matrix = [
        [9, 1, 5, 5, 5, 5, 1, 9],
        [1, 0, 3, 3, 3, 3, 0, 1],
        [5, 3, 4, 4, 4, 4, 3, 5],
        [5, 3, 4, 4, 4, 4, 3, 5],
        [5, 3, 4, 4, 4, 4, 3, 5],
        [5, 3, 4, 4, 4, 4, 3, 5],
        [1, 0, 3, 3, 3, 3, 0, 1],
        [9, 1, 5, 5, 5, 5, 1, 9]
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
        game_mode = input("ゲームモードを選んでください:\n1: 人間同士\n2: 人間対AI\n3: AI対AI\n選択肢の番号を入力してください: ").strip()

        if game_mode == '1':
            self.setup_human_vs_human()
        elif game_mode == '2':
            self.setup_human_vs_ai()
        elif game_mode == '3':
            self.setup_ai_vs_ai()
        else:
            print("無効な選択です。デフォルトでAI対AIのモードになります。")
            self.setup_ai_vs_ai()

    def setup_human_vs_human(self):
        """人間同士のプレイヤーを設定する。"""
        player_name_black = f"{HUMAN_PLAYER_NAME}1"
        player_name_white = f"{HUMAN_PLAYER_NAME}2"
        self.players = [
            HumanPlayer(player_name_black, BLACK),
            HumanPlayer(player_name_white, WHITE)
        ]

    def setup_human_vs_ai(self):
        """人間対AIのプレイヤーを設定する。"""
        player_name_black = "HumanPlayer"
        ai_level = input("AIレベルを選んでください: \n1: Easy AI\n2: Hard AI\n選択肢の番号を入力してください: ").strip()

        if ai_level == '1':
            player_name_white = EASY_AI_PLAYER_NAME
            self.players = [
                HumanPlayer(player_name_black, BLACK),
                EasyAIPlayer(player_name_white, WHITE)
            ]
        elif ai_level == '2':
            player_name_white = HARD_AI_PLAYER_NAME
            self.players = [
                HumanPlayer(player_name_black, BLACK),
                HardAIPlayer(player_name_white, WHITE)
            ]
        else:
            print("無効な選択です。デフォルトでEasy AIが選ばれます。")
            self.setup_human_vs_ai()

    def setup_ai_vs_ai(self):
        """AI同士のプレイヤーを設定する。"""
        ai_level = input(f"AIレベルを選んでください: \n1: Easy AI\n2: Hard AI\n選択肢の番号を入力してください: ").strip()

        if ai_level == '1':
            player_name_black = f"{EASY_AI_PLAYER_NAME}1"
            player_name_white = f"{EASY_AI_PLAYER_NAME}2"
            self.players = [
                EasyAIPlayer(player_name_black, BLACK),
                EasyAIPlayer(player_name_white, WHITE)
            ]
        elif ai_level == '2':
            player_name_black = HARD_AI_PLAYER_NAME
            player_name_white = EASY_AI_PLAYER_NAME
            self.players = [
                HardAIPlayer(player_name_black, BLACK),
                EasyAIPlayer(player_name_white, WHITE)
            ]
        else:
            print("無効な選択です。デフォルトでHard AI同士が選ばれます。")
            player_name_black = f"{HARD_AI_PLAYER_NAME}2"
            player_name_white = f"{HARD_AI_PLAYER_NAME}2"
            self.players = [
                HardAIPlayer(player_name_black, BLACK),
                HardAIPlayer(player_name_white, WHITE)
            ]            

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

        print(f"最終スコア: {player_name_black} {black_count}個, {player_name_white} {white_count}個")
        print(result)


if __name__ == "__main__":
    Game().play()
