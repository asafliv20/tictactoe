import numpy

from settings import *

class Game:
    def __init__(self):
        # Initialize pygame and screen's settings
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(BACKGROUNDCOLOR)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.mousePos = vec() # Mouse position variable
        self.font_name = pg.font.match_font(FONTNAME)
        self.running = True  # game loop
        self.player = 1  # which player is currently playing
        self.board = numpy.zeros((NUMOFCUBES, NUMOFCUBES))  # simple visualization of the screen
        self.playing = True  # game loop
        self.gameOver = False  # game ends

    def new(self):
        self.player = 1
        self.board = numpy.zeros((NUMOFCUBES, NUMOFCUBES))
        self.screen.fill(BACKGROUNDCOLOR)

    # The update function
    def run(self):
        while self.playing:
            self.events()
            self.draw()
        self.show_start_screen()

    # Handle keyboard and mouse input events
    def events(self):
        self.canWin = False

        # Event loop, goes through keyboard and mouse input
        for event in pg.event.get():
            # Player wants to end the game
            if event.type == pg.K_ESCAPE or event.type == pg.QUIT:
                self.running = False
                sys.exit()
            # Player placing an object
            if event.type == pg.MOUSEBUTTONDOWN:
                # Get mouse's position
                self.mousePos.x = event.pos[0]
                self.mousePos.y = event.pos[1]

                # Modify mouse position to fit board's conditions
                row = int(self.mousePos.y // 200)
                column = int(self.mousePos.x // 200)

                # Check if square is available -> update board
                if self.available_square(row, column):
                    self.mark_square(row, column, self.player)
                    self.player *= -1 # Next player's turn
                    self.check_board() # Check for a winning sequence

                print(self.board)

    # Main Draw function
    def draw(self):
        self.draw_lines()
        self.draw_shapes()
        pg.display.update()

    # Checks board status
    def check_board(self):
        # Main and secondary diagonal
        self.check_main_diag()
        self.check_second_diag()

        # Goes through each combination of rows an columns
        for i in range(NUMOFCUBES):
            self.check_row(i)
            self.check_col(i)

    # Checks row in board[r][]
    def check_row(self, r):
        result = 0
        for c in range(NUMOFCUBES):
            result += self.board[r][c]

        if abs(result) == 3:
            self.draw_winner_line(20, (r*200)+100, WIDTH - 20, (r*200)+100)

    # checks column in board[][c]
    def check_col(self, c):
        result = 0
        for r in range(NUMOFCUBES):
            result += self.board[r][c]

        if abs(result) == 3:
            self.draw_winner_line((c * 200) + 100, 20, (c * 200) + 100, HEIGHT - 20)

    # Checks main diagonal
    def check_main_diag(self):
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            self.draw_winner_line(20, 20, WIDTH - 20, HEIGHT - 20)

    # Checks secondary diagonal
    def check_second_diag(self):
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            self.draw_winner_line(WIDTH - 20, 20, 20, HEIGHT - 20)

    # Checks square's availability
    def available_square(self, row, col):
        return self.board[row][col] == 0

    # Checks board's capacity
    def is_board_full(self):
        for r in range(NUMOFCUBES):
            for c in range(NUMOFCUBES):
                if self.board[r][c] == 0:
                    return False

        return True

    # Update board's placement
    def mark_square(self, row, col, player):
        self.board[row][col] = player

    # Draw game-board lines
    def draw_lines(self):
        # Lines for columns
        for i in range(NUMOFCUBES - 1):
            pg.draw.line(self.screen, LINECOLOR, [(i + 1) * 200, 0], [(i + 1) * 200, 600], LINESIZE)
        # Lines for rows
        for i in range(NUMOFCUBES - 1):
            pg.draw.line(self.screen, LINECOLOR, [0, (i + 1) * 200], [600, (i + 1) * 200], LINESIZE)

    # Draw X in a certain spot
    def draw_x(self, x, y):
        x = int(x * 200 + 100)
        y = int(y * 200 + 100)

        pg.draw.line(self.screen, XCOLOR, [x - 75, y - 75], [x + 75, y + 75], SIZEX)
        pg.draw.line(self.screen, XCOLOR, [x + 75, y - 75], [x - 75, y + 75], SIZEX)

    # Draw circle in a certain spot
    def draw_circle(self, x, y):
        x = int(x * 200 + 100)
        y = int(y * 200 + 100)

        pg.draw.circle(self.screen, CIRCLECOLOR, (x, y), CIRCLERADIUS, CIRCLESIZE)

    # Draw shapes according to the board
    def draw_shapes(self):
        for r in range(NUMOFCUBES):
            for c in range(NUMOFCUBES):
                if self.board[c][r] == 1:
                    self.draw_x(r, c)
                elif self.board[c][r] == -1:
                    self.draw_circle( r, c)

    # Draw winning line, with start and end points accordingly
    def draw_winner_line(self, startX, startY, endX, endY):
        pg.draw.line(self.screen, (255, 0, 0), (startX, startY), (endX, endY), LINESIZE+10)
        self.playing = False

    # Draw text to screen
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BACKGROUNDCOLOR)
        self.draw_text(TITLE, 48, BLACK, WIDTH / 2, HEIGHT / 4)
        self.draw_text("TIC TAC TOE", 22, BLACK, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, BLACK, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game splash/start screen
        self.screen.fill(BACKGROUNDCOLOR)
        self.draw_text(TITLE, 48, BLACK, WIDTH / 2, HEIGHT / 4)
        self.draw_text("TIC TAC TOE", 22, BLACK, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, BLACK, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    # Wait for key in opening screen
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.K_ESCAPE:
                    sys.exit()
                if event.type == pg.KEYUP:
                    waiting = False
                    self.playing = True


# Main program
g = Game()
g.show_start_screen()
while (g.running):
    g.new()
    g.run()
    g.show_go_screen()
