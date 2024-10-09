from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

color1 = [100, 0, 0]  # Red
color2 = [0, 0, 100]  # Blue
cursor_color = [0, 255, 0] # Green for cursor
    
B = [0, 0, 0]  #Black
W = [100, 100, 100] #White

board_outline = [
    B, B, W, B, B, W, B, B,
    B, B, W, B, B, W, B, B,
    W, W, W, W, W, W, W, W,
    B, B, W, B, B, W, B, B,
    B, B, W, B, B, W, B, B,
    W, W, W, W, W, W, W, W,
    B, B, W, B, B, W, B, B,
    B, B, W, B, B, W, B, B
    ]


# Initialize board as empty
board = [[' ' for _ in range(8)] for _ in range(8)]

# Current cursor position starting at the middle
#cursor = [[x1,y1], [x2,y1], [x1, y2], [x2,y2]]
cursor = [[3, 3], [4, 3], [3, 4], [4, 4]]
current_player = 'pl1'

# Draw the Tic-Tac-Toe board on the LED matrix
def draw_board():
    global marked
    # Clear the matrix first
    sense.clear()
    
    sense.set_pixels(board_outline)
    
    for x in range(8):
        for y in range(8): 
            if board[x][y] == 'pl1':
                sense.set_pixel(x, y, color1)
            elif board[x][y] == 'pl2':
                sense.set_pixel(x, y, color2)
    
    # Highlight the current cursor position
        player_color = color1 if current_player== 'pl1' else color2
        sense.set_pixel(cursor[0][0], cursor[0][1], cursor_color)
        sense.set_pixel(cursor[3][0], cursor[3][1], cursor_color)
        sense.set_pixel(cursor[1][0], cursor[1][1], player_color)
        sense.set_pixel(cursor[2][0], cursor[2][1], player_color)

# Check if a player has won
def check_winner():
    for row in board:
        if row[0] == row[3] == row[6] != ' ':
            return row[0]
    
    for col in board:
        if col[0] == col[3] == col[6] != ' ':
            return col[0]
    
    if board[0][0] == board[3][3] == board[6][6] != ' ':
        return board[0][0]
    
    if board[1][6] == board[4][3] == board[7][0] != ' ':
        return board[1][6]
    
    return None

# Check if the board is full (draw)
def check_draw():
    for i in range(0, 7, 3):
        for j in range (0, 7, 3):
            if board[i][j] == ' ':
                return False
    return True

# Move the cursor based on joystick input
def move_cursor(direction):
    if direction == 'up' and cursor[0][1] > 2:  #y1,y2 --
        for i in cursor:
            i[1] -= 3
    elif direction == 'down' and cursor[2][1] < 5:  #y1,y2++
        for i in cursor:
            i[1] += 3
    elif direction == 'left' and cursor[0][0] > 2: #x1,x2 --
        for i in cursor:
            i[0] -= 3
    elif direction == 'right' and cursor[1][0] < 5:    #x1,x2 ++
        for i in cursor:
            i[0] += 3

# Place the current player's mark on the board
def place_mark():
    global current_player
    global cursor
    for i in cursor:
        x=i[0]
        y=i[1]
        if board[x][y] == ' ':  # Only place mark if the cell is empty
            board[x][y] = current_player
        elif board[x][y] != ' ':
            sense.clear()
            sense.show_message("not empty!", text_colour=[255, 255, 0])
            return
    if current_player == 'pl1':
            current_player = 'pl2'
            sense.clear()
            sense.show_letter("2", text_colour=color2)
            sleep(1)
            
    else:
            current_player = 'pl1'
            sense.clear()
            sense.show_letter("1", text_colour=color1)
            sleep(1)
        

# Main game loop
def game_loop():
    global current_player
    global cursor
    sense.clear()
    sense.show_message("Welcome to Tic-Tac-Toe!", text_colour=[255, 255, 0])
    sense.show_letter("1", text_colour=color1)
    sleep(1)
    while True:
        draw_board()
        sleep(0.1)
        
        for event in sense.stick.get_events():
            if event.action == 'pressed':
                if event.direction in ['up', 'down', 'left', 'right']:
                    move_cursor(event.direction)
                elif event.direction == 'middle':
                    place_mark()

                # Check for a winner after placing the mark
                winner = check_winner()
                if winner:
                    sense.show_message(f"{winner} wins!", text_colour=color1 if winner == 'pl1' else color2)
                    return
                
                # Check for a draw
                if check_draw():
                    sense.show_message("Draw!", text_colour=[255, 255, 0])
                    return
                

# Start the game
sense.clear()
game_loop()
