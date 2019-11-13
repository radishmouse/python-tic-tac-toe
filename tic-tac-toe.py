EMPTY = ' '
PLAYER_X = 'X'
PLAYER_Y = 'Y'

def is_board_valid(board):
    has_enough_rows = len(board) == 3
    has_correct_row_length = True
    for row in board:
        if len(row) != 3:
            has_correct_row_length = False
    return has_enough_rows and has_correct_row_length

def is_location_free(board, location):
    # y = location[0]
    # x = location[1]
    # clever trick:
    y, x = location
    return board[y][x] == EMPTY

def is_location_valid(board, location):
    y, x = location

    # y tells us which row.
    # that row number should be between -1 and the length of the board
    y_is_valid = y >= 0 and y < len(board)

    # x tells us which column in a single row
    x_is_valid = True
    if x < 0:
        x_is_valid = False
    else:
        for row in board:
            if x >= len(row):
                x_is_valid = False
                
    return y_is_valid and x_is_valid

def move(board, location, player):
    if not is_board_valid(board):
        raise Exception('The board is the wrong size, buddy')    
    elif not is_location_valid(board, location):
        raise Exception(f'The location {location} is outside the board')
    elif not is_location_free(board, location):
        raise Exception(f'The location {location} is already taken')

    y, x = location
    board[y][x] = player
    return board

def get_move_location():
    y = int(input("what row? "))
    x = int(input("what column? "))

    return (y, x)

def print_board(board):
    for row in board:
        print(row)

def winning_row(row):
    is_all_same = True
    first = row[0]
    for item in row:
        if item == EMPTY or item != first:
            is_all_same = False

    return (is_all_same, first)

def get_column(board, column_number):
    column = []
    for row in board:
        column.append(row[column_number])
    return column

def generate_diagonals(board, other=False):
    diag = []
    if other:
        y_range = range(len(board) - 1, -1, -1)
    else:
        y_range = range(len(board))
        
    for y in y_range:
        for x in range(len(board)):
            diag.append((y, x))
    return diag[::4]

def get_diagonal(board, coordinate_list):
    diag = []
    for y, x in coordinate_list:
        diag.append(board[y][x])
    return diag
    
def has_winner(board):
    # search all rows
    for row in board:
        found_winner, whom = winning_row(row)
        if found_winner:
            # print('found winning row', row)
            return whom

    # Get a row, just to get a column count
    a_row = board[0]
    # Loop through the column numbers
    for i in range(len(a_row)):
        column_as_row = get_column(board, i)

        # Search the column using our existing function
        found_winner, whom = winning_row(column_as_row)
        if found_winner:
            # print('found winning column', column_as_row)
            return whom

    # Check both diagonals
    diag_coords_1 = generate_diagonals(board, True)
    diag_as_row = get_diagonal(board, diag_coords_1)
    found_winner, whom = winning_row(diag_as_row)
    if found_winner:
        # print('found winning diagonal', diag_as_row)
        return whom
    
    diag_coords_2 = generate_diagonals(board, False)
    diag_as_row = get_diagonal(board, diag_coords_2)
    found_winner, whom = winning_row(diag_as_row)
    if found_winner:
        # print('found winning diagonal', diag_as_row)
        return whom
        
    # If we don't find a winner, return "nothing""
    return None

def main():
    # Setup
    board = [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],        
    ]

    player = PLAYER_X    
    is_player_x_turn = True
    still_playing = True
    
    # Main game loop
    while still_playing:
        print_board(board)
        
        if is_player_x_turn:
            player = PLAYER_X
        else:
            player = PLAYER_Y            
        
        try:
            print(f'Ready to play player {player}')
            location = get_move_location()
            board = move(board, location, player)

            # Flip the turn
            is_player_x_turn = not is_player_x_turn
        except Exception as error:
            print()
            print()            
            print(error)
            print(f'Try again player {player}!')
            print()
            print()
        winner = has_winner(board)
        if winner:
            print(f'Yay! Player {winner} won!')
            still_playing = False
    

    # Testing for invalid location
    # move(board, (-1, 3), PLAYER_X)

main()
