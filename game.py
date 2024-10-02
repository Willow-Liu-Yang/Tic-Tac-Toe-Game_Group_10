
def print_board(board):
    """Prints the current state of the game board."""
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board):
    """Checks if there is a winner on the board."""
    # Check rows for a win
    for row in board:
        if row.count(row[0]) == 3 and row[0] != ' ':
            return True
    
    # Check columns for a win
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return True
    
    # Check diagonals for a win
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return True
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return True
    
    return False

def is_full(board):
    """Checks if the board is full (tie situation)."""
    return all(cell != ' ' for row in board for cell in row)

def tic_tac_toe():
    """Main function to run the Tic-Tac-Toe game."""
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'

    while True:
        print_board(board)
        try:
            row = int(input(f"Player {current_player}, enter row (0-2): "))
            col = int(input(f"Player {current_player}, enter col (0-2): "))
            
            if row < 0 or row > 2 or col < 0 or col > 2:
                print("Invalid input! Please enter values between 0 and 2.")
                continue

            if board[row][col] == ' ':
                board[row][col] = current_player
                if check_winner(board):
                    print_board(board)
                    print(f"Player {current_player} wins!")
                    break
                if is_full(board):
                    print_board(board)
                    print("It's a tie!")
                    break
                current_player = 'O' if current_player == 'X' else 'X'
            else:
                print("Cell already taken! Try again.")
        except ValueError:
            print("Invalid input! Please enter numbers only.")
        except IndexError:
            print("Invalid input! Row and column must be between 0 and 2.")

if __name__ == "__main__":
    tic_tac_toe()
