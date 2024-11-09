import sys
import string
from xmlrpc.client import PARSE_ERROR

PIECES_LOOKS={'K':('♔','♚'),'Q':('♕','♛'),'R':('♖','♜'),'B':('♗','♝'),'N':('♘','♞'),'P':('♙','♟'),'tile':('◻','◼')}
NOTATION_NAMES={'K':'King', 'Q':'Queen', 'R':'Rook', 'B':'Bishop', 'N':'Knight', 'P':'Pawn'}
NORMAL_BOARD={'P':list(zip([6**(x//8) for x in range(16)], [y%8 for y in range(16)])), 'N':[(0,2), (0,5), (7,2), (7,5)],
              'B':[(0,1),(0,6),(7,1),(7,6)], 'R':[(0,0),(0,7),(7,0),(7,7)],'Q':[(0,3),(7,3)], 'K':[(0,4),(7,4)]}

# blatantly stolen from StackOverflow. Thank you sixthgear for the code
def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


class Piece:
    def __init__(self,  color: bool, pos: tuple, curr_board: object): # in color, True represents white and False black
        self.color = color
        self.pos = pos
        self.curr_board = curr_board

    def valid_move(self, pos: tuple):
        piece=self.curr_board.full_board[pos[0]][pos[1]]
        if piece:
            if piece.color == self.color:
                return False
            else:
                return True
        else:
            return True



class Pawn(Piece):
    name='P'
    def __init__(self, color: bool, pos: tuple, curr_board: object):
        super().__init__(color, pos, curr_board)


class King(Piece):
    name='K'
    def __init__(self, color: bool, pos: tuple, curr_board: object):
        super().__init__(color, pos, curr_board)


class Queen(Piece):
    name='Q'
    def __init__(self, color: bool, pos: tuple, curr_board: object):
        super().__init__(color, pos, curr_board)


class Rook(Piece):
    name='R'
    def __init__(self, color: bool, pos: tuple, curr_board: object):
        super().__init__(color, pos, curr_board)


class Bishop(Piece):
    name='B'
    def __init__(self, color: bool, pos: tuple, curr_board: object):
        super().__init__(color, pos, curr_board)


class Knight(Piece):
    name='N'
    def __init__(self, color: bool, pos: tuple, curr_board: object):
        super().__init__(color, pos, curr_board)


class Board:

    empty_board=[[0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0]]

    def __init__(self, auto=True, conf=NORMAL_BOARD):
        self.full_board=self.empty_board
        if auto:
            self.make_board(conf)

    # I had to browse utf-8 encoding for this sleek chessboard design but I think I got it
    def show_board(self)->None:
        showed=self.full_board
        for y in range(8):
            for x in range(8):
                if showed[y][x]:
                    showed[y][x]=PIECES_LOOKS[showed[y][x].name][showed[y][x].color]+'  '
                else:
                    showed[y][x]=PIECES_LOOKS['tile'][(x+y+1)%2]+' '
        i=1
        print('   ', end='')
        for numb in range(8):
            print(string.ascii_lowercase[numb], end='    ')
        print()
        for y in showed:
            print(i, end=' ')
            i+=1
            for x in y:
                print(x, end='')
            print()


    def make_board(self, conf: dict):
        for piece_type in conf.keys():
            for piece in conf[piece_type]:
                self.full_board[piece[0]][piece[1]]=str_to_class(NOTATION_NAMES[piece_type])(bool(piece[0]//4), piece, self)


if __name__ == '__main__':
    board=Board()
    board.show_board()
    piece=board.full_board[0][0]
    print(piece)
    # print(board.full_board[0][0].valid_move((2,0),))