# Import necessary libraries
import numpy as np  # Import NumPy for array manipulation
import pygame  # Import Pygame for creating the game interface
import sys  # Import sys for system-related functionalities
import math  # Import math for mathematical calculations

# Define color constants for the game
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Define the number of rows and columns on the game board
ROW_COUNT = 6
COLUMN_COUNT = 7

# Define a function to create the game board
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))  # Create a 2D NumPy array filled with zeros
    return board

# Define a function to place a player's piece on the board
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Define a function to check if a column is a valid move
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

# Define a function to find the next available row in a column
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Define a function to print the game board
def print_board(board):
    print(np.flip(board, 0))  # Print the board with rows flipped for visual display

# Define a function to check for a winning move
def winning_move(board, piece):
    # Check horizontal locations for a win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations for a win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals for a win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals for a win
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

# Define a function to draw the game board
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

# Create the initial game board
board = create_board()

# Print the empty game board
print_board(board)

# Initialize game-related variables
game_over = False
turn = 0

# Initialize Pygame
pygame.init()

# Define constants for the game board and pieces
SQUARESIZE = 100  # Size of each cell in the game board
width = COLUMN_COUNT * SQUARESIZE  # Width of the game window
height = (ROW_COUNT + 1) * SQUARESIZE  # Height of the game window
size = (width, height)  # Size of the game window
RADIUS = int(SQUARESIZE / 2 - 5)  # Radius of player's pieces

# Create the Pygame screen
screen = pygame.display.set_mode(size)

# Draw the initial game board
draw_board(board)
pygame.display.update()

# Initialize the font for displaying messages
myfont = pygame.font.SysFont("monospace", 75)

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            # Update the piece's position based on mouse movement
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handle player's move when the mouse is clicked
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            col = int(math.floor(posx / SQUARESIZE))

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1 if turn == 0 else 2)

                if winning_move(board, 1 if turn == 0 else 2):
                    label = myfont.render("Player 1 wins!!" if turn == 0 else "Player 2 wins!!", 1, RED if turn == 0 else YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2  # Toggle between Player 1 and Player 2

            if game_over:
                pygame.time.wait(3000)
