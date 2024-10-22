import tkinter as tk
from tkinter import messagebox
from sense_hat import SenseHat
from time import sleep

#Sense HAT initialization
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
# cursor = [[x1,y1], [x2,y1], [x1, y2], [x2,y2]]
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
	# Look for row match
	if board[0][0] == board[3][0] == board[6][0] !=' ':
		return board[0][0]

	if board[0][3] == board[3][3] == board[6][3] !=' ':
		return board[0][3]
	
	if board[0][6] == board[3][6] == board[6][6] !=' ':
		return board[0][6]

	# Look for column match
	if board[0][0] == board[0][3] == board[0][6] !=' ':
		return board[0][0]

	if board[3][0] == board[3][3] == board[3][6] !=' ':
		return board[3][0]
	
	if board[6][0] == board[6][3] == board[6][6] !=' ':
		return board[6][0]
	
	# Look for diagonal match
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

# Move the cursor based on joystick input (all coordinates move 3 steps/pixels because they can't be on grid)
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
		

# Main game loop for joystick
def game_loop():
	global current_player
	global cursor
	sense.clear()
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

class TicTacToe:
	def __init__(self, root):
		self.root = root
		self.root.title("Tic-Tac-Toe")
		self.current_player = "X"  # X starts the game
		self.board = [" " for _ in range(9)]  # A list to store board values
		self.buttons = []

		# Create buttons for the game grid
		for i in range(9):
			button = tk.Button(self.root, text=" ", font=("Arial", 20), height=3, width=6,
							   command=lambda i=i: self.make_move(i))
			button.grid(row=i // 3, column=i % 3)
			self.buttons.append(button)

	def make_move(self, index):
		if self.board[index] == " " and not self.check_winner():
			self.board[index] = self.current_player
			self.buttons[index].config(text=self.current_player)

			if self.check_winner():
				messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
				self.reset_board()
			elif " " not in self.board:
				messagebox.showinfo("Game Over", "It's a tie!")
				self.reset_board()
			else:
				self.current_player = "O" if self.current_player == "X" else "X"

	def check_winner(self):
		# Define all possible winning combinations
		winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
								(0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
								(0, 4, 8), (2, 4, 6)]              # Diagonal
		for combo in winning_combinations:
			if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != " ":
				return True
		return False

	def reset_board(self):
		self.board = [" " for _ in range(9)]
		for button in self.buttons:
			button.config(text=" ")
		self.current_player = "X"  # X starts again

def GUI_version():
	# Create the main window
	root = tk.Tk()
	game = TicTacToe(root)
	root.mainloop()
				
def Joystick_version():
	# Start the game
	sense.clear()
	game_loop()
	
def main():
	while True:
		user_input = input("Welcome to Tic-Tac-Toe!\n For GUI version, type 'G', for Joystick version, type 'J'!\n Or type 'exit' to quit:")
		if user_input.lower() == 'exit':
			print("Exiting the program.")
			break
		elif user_input.lower() == 'g':
			GUI_version()
		elif user_input.lower() == 'j':
			Joystick_version()

if __name__ == "__main__":
	main()
