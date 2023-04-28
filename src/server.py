import Pyro5.api

from player import Player


ULTRA_VIOLET = (92, 96, 153)
ARGENTINIAN_BLUE = (71, 179, 255)

PLAYERS: list[Player] = [
    {'id': 1, 'symbol': 'X', 'active': False, 'color': ULTRA_VIOLET},
    {'id': 2, 'symbol': 'O', 'active': False, 'color': ARGENTINIAN_BLUE},
]
CURRENT_PLAYER: Player = PLAYERS[0]
WINNER = None

BOARD_SIZE: int = 3
EMPTY_POSITION: str = ''
BOARD: list[list[str]] = [[EMPTY_POSITION for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


@Pyro5.api.expose
class TicTacToeServer(object):

    def __init__(self) -> None:
        self.players: list[Player] = PLAYERS
        self.current_player: Player = CURRENT_PLAYER
        self.winner = WINNER

        self.board_size: int = BOARD_SIZE
        self.board: list[list[str]] = BOARD

    def get_players(self) -> list[Player]:
        return self.players

    def get_current_player(self) -> Player:
        return self.current_player

    def get_winner(self):
        return self.winner

    def get_board(self) -> list[list[str]]:
        return self.board

    def is_position_empty(self, x: int, y: int) -> bool:
        return self.board[x][y] == EMPTY_POSITION

    def add_player(self) -> Player | None:
        for player in self.players:
            if not player['active']:
                player['active'] = True
                print(f"Player {player['id']} has joined the game.")
                return player

        return None

    def remove_player(self, player: Player) -> None:
        self.players.remove(player)
        print(f"Player {player['id']} has left the game.")

    def make_move(self, x: int, y: int):
        if self.winner is None and self.is_position_empty(x, y):
            self.board[x][y] = self.current_player['symbol']
            winner = self.check_for_winner()
            print('winner:', winner)
            if winner is not None:
                self.winner = winner
                print(f'Player {self.winner} wins!')
            else:
                self.switch_player()

    def check_for_winner(self):
        for i in range(self.board_size):
            # rows
            if not self.is_position_empty(i, 0) and self.board[i][0] == self.board[i][1] == self.board[i][2]:
                return self.board[i][0]
            # columnns
            if not self.is_position_empty(0, i) and self.board[0][i] == self.board[1][i] == self.board[2][i]:
                return self.board[0][i]

        # main dioganol
        if not self.is_position_empty(0, 0) and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return self.board[0][0]
        # reverse dioganol
        if not self.is_position_empty(0, 2) and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return self.board[0][2]

        if all(all(row) for row in self.board):
            return 'Tie'

        return None

    def switch_player(self) -> None:
        self.current_player = self.players[2] if self.current_player == self.players[1] else self.players[1]


def start_server() -> None:
    daemon = Pyro5.server.Daemon()
    # ns = Pyro5.api.locate_ns()
    uri = daemon.register(TicTacToeServer)
    # ns.register("game.server", uri)
    print(f'URI: {uri}\nReady. Waiting for players...')
    daemon.requestLoop()


if __name__ == '__main__':
    try:
        start_server()
    except (KeyboardInterrupt, EOFError):
        print('Goodbye! :)')
exit()
