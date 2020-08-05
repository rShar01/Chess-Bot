import random
import chess


# returns the value of each piece
def get_piece_value(piece):
    if piece == chess.PAWN:
        return 1
    elif piece == chess.BISHOP:
        return 3
    elif piece == chess.KNIGHT:
        return 3
    elif piece == chess.ROOK:
        return 5
    elif piece == chess.QUEEN:
        return 7


class chessBot:
    # sets the bot to color it is playing
    def __init__(self, color):
        self.color = color

    # gets the location of each of the bot's pieces
    def get_piece_locations(self, curr_board: chess.Board):
        lop = curr_board.piece_map()
        own_lop = {}
        for p in lop:
            if curr_board.color_at(p) == self.color:
                own_lop[p] = lop[p]
        return own_lop

    # looks 3 moves into the future using recursion and assigns each possible move a value. Returns greatest valued move
    def find_most_value(self, curr_board, depth):
        # recurse until 5 moves in the future
        if depth == 4:
            return self.evaluate_best(curr_board)
        else:
            # generates all possible moves
            valid_moves = curr_board.legal_moves
            lom = []
            # assigns each move a value based on future possible moves
            for m in valid_moves:
                curr_board.push(m)
                fen = curr_board.board_fen()
                next_board = chess.Board(fen)
                curr_board.pop()
                lom.append(self.find_most_value(next_board, depth + 1))

        # finds move with most value
        most_value = 0
        for i in range(len(lom)):
            if lom[i] > most_value:
                most_value = lom[i]

        return most_value

    # gives a value to the move based on the next possible move is (center control, capturing pieces, checkmate, etc)
    def evaluate_best(self, curr_board):
        # gets the next possible moves
        valid_moves = curr_board.legal_moves
        most_value = 0
        lop = self.get_piece_locations(curr_board)
        for m in valid_moves:
            curr_value = 0
            # return move if it is winning (best move)
            if curr_board.is_checkmate():
                return m

            # subtracts value if the move causes you to lose a piece
            if curr_board.is_attacked_by(not self.color, m.to_square):
                curr_value = curr_value - get_piece_value(curr_board.piece_at(m.from_square).piece_type)

            # adds value of piece you can capture
            if curr_board.is_capture(m):
                piece_value = get_piece_value(curr_board.piece_at(m.from_square).piece_type)
                curr_value = piece_value

            # adds value if the move checks the king
            if curr_board.is_check():
                curr_value = curr_value + 5

            # next few if's check if the move attacks the center, adds value if it does
            if curr_board.is_attacked_by(self.color, chess.E4):
                curr_value = curr_value + 3

            if curr_board.is_attacked_by(self.color, chess.E5):
                curr_value = curr_value + 3

            if curr_board.is_attacked_by(self.color, chess.D4):
                curr_value = curr_value + 3

            if curr_board.is_attacked_by(self.color, chess.D5):
                curr_value = curr_value + 3

            if curr_board.is_attacked_by(self.color, chess.C6):
                curr_value = curr_value + 1

            if curr_board.is_attacked_by(self.color, chess.D6):
                curr_value = curr_value + 1

            if curr_board.is_attacked_by(self.color, chess.E6):
                curr_value = curr_value + 1

            if curr_board.is_attacked_by(self.color, chess.F6):
                curr_value = curr_value + 1

            if curr_board.is_attacked_by(self.color, chess.C5):
                curr_value = curr_value + 2

            if curr_board.is_attacked_by(self.color, chess.F5):
                curr_value = curr_value + 2

            if curr_board.is_attacked_by(self.color, chess.C4):
                curr_value = curr_value + 2

            if curr_board.is_attacked_by(self.color, chess.F4):
                curr_value = curr_value + 2

            if curr_board.is_attacked_by(self.color, chess.C3):
                curr_value = curr_value + 1

            if curr_board.is_attacked_by(self.color, chess.D3):
                curr_value = curr_value + 1

            if curr_board.is_attacked_by(self.color, chess.E3):
                curr_value = curr_value + 1

            if curr_board.is_attacked_by(self.color, chess.F3):
                curr_value = curr_value + 1

            # checks if the move would cause you to lose your piece, subtracts it's value if so
            for sq in lop:
                if curr_board.is_attacked_by(not self.color, sq):
                    curr_value = curr_value - get_piece_value(lop[sq].piece_type)

            # gets most possible value of each move and assigns it to that move
            if curr_value > most_value:
                most_value = curr_value

        return most_value

    # gets the move with the most value, the best move of the current legal moves
    def get_best_move(self, curr_board):
        # generates the current moves
        valid_moves = curr_board.legal_moves
        # make a dictionary of move and it's value
        lom = {}
        for m in valid_moves:
            curr_board.push(m)
            fen = curr_board.board_fen()
            next_board = chess.Board(fen)
            curr_board.pop()
            # gets the most value of that move
            best = self.find_most_value(next_board, 1)
            # assign that dictionary value to the most value
            lom[m] = best

        # display the dictionary of moves and their value
        print(lom)

        most_value = 0

        #finds move with most value
        for m in lom:
            if lom[m] >= most_value:
                best_move = m
                most_value = lom[m]

        # if all moves are bad (negative) then randomly choose one, otherwise use the best one
        if most_value > 0:
            return best_move
        else:
            print('ok yeah lets do a random') # tells user that there are no good moves so randomly choosing one
            count = random.randint(0, valid_moves.count())
            for m in valid_moves:
                if count != 0:
                    count = count - 1
                else:
                    return m


board = chess.Board()
# put moves here



# getting the bot set up with the current board
bot = chessBot(chess.WHITE)
move = bot.get_best_move(board)
# print the move
print(move)
board.push(move)
# show the move
print(board)
