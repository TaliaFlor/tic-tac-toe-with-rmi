import Pyro5.api
import pygame

from player import Player

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PRUSSIAN_BLUE = (4, 42, 74)
PISTACHIO = (150, 204, 143)


# BIG_FONT = pygame.font.Font('freesansbold.ttf', 64)
# SMALL_FONT = pygame.font.Font('freesansbold.ttf', 32)


class Game:
    def __init__(self, server: Pyro5.api.Proxy, player: Player) -> None:
        pygame.init()

        self.width = 600
        self.height = 550

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tic Tac Toe")

        icon = pygame.image.load("img/tictactoe.png")
        pygame.display.set_icon(icon)

        self.board_size = 3
        self.cell_size = self.width // self.board_size

        self.server = server
        self.player = player

    # def draw_screen(self, status_msg: str, info_msg: str) -> None:
    #     self.screen.fill(WHITE)
    #
    #     # vertical lines
    #     self._draw_line((250 - 2, 150), (250 - 2, 450))
    #     self._draw_line((350 - 2, 150), (350 - 2, 450))
    #     # horizontal lines
    #     self._draw_line((150, 250 - 2), (450, 250 - 2))
    #     self._draw_line((150, 350 - 2), (450, 350 - 2))
    #
    #     # write texts
    #     title = BIG_FONT.render("TIC TAC TOE", True, PRUSSIAN_BLUE)
    #     self.screen.blit(title, (110, 0))
    #
    #     subtitle = SMALL_FONT.render(status_msg, True, self.player['color'])
    #     self.screen.blit(subtitle, (150, 70))
    #
    #     info = SMALL_FONT.render(info_msg, True, PISTACHIO)
    #     self.screen.blit(info, (100, 480))
    #
    # def _draw_line(self, start_pos: tuple[int, int], end_pos: tuple[int, int]):
    #     pygame.draw.line(self.screen, BLACK, start_pos, end_pos, 4)

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.server.remove_player(self.player)
                    pygame.quit()
                    return

                if event.type != pygame.MOUSEBUTTONDOWN:
                    continue
                print(event)
                if len(self.server.get_players()) < 2:
                    continue

                print(self.server.get_current_player())
                print(self.player)
                if self.server.get_current_player()['id'] != self.player['id']:
                    continue

                print('after if')

                x, y = event.pos[0] // self.cell_size, event.pos[1] // self.cell_size
                self.server.make_move(x, y)

            # Draw the board
            self.screen.fill(WHITE)
            board = self.server.get_board()
            for x in range(self.board_size):
                for y in range(self.board_size):
                    rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, BLACK, rect, 1)
                    if not self.server.is_position_empty(x, y):
                        text = pygame.font.SysFont(None, 60).render(board[x][y], True, BLACK)
                        text_rect = text.get_rect(center=rect.center)
                        self.screen.blit(text, text_rect)

            # Update the display
            pygame.display.update()

            # Check for winner or tie
            if self.server.get_winner() is not None:
                pygame.time.wait(1000)
                if self.server.get_winner() == 'Tie':
                    print("It's a tie!")
                else:
                    print(f"Player {self.server.get_winner()} wins!")
                self.server.remove_player()
                pygame.quit()
                return


def start_client() -> None:
    uri = input("What is the URI of the server? ").strip()
    server = Pyro5.api.Proxy(uri)
    # server = Pyro5.api.Proxy('PYRONAME:game.server')

    # Connect to the server and join the game
    player: Player = server.add_player()
    if player is None:
        print('Game is full.')
        exit()

    # Start the game loop
    print('Connected to the game server.')
    print(f'You are player {player["id"]}.')

    game = Game(server, player)
    game.run()


if __name__ == '__main__':
    try:
        start_client()
    except (KeyboardInterrupt, EOFError):
        print('Goodbye! :)')
exit()
