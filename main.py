import random
import sys
import string
from string import ascii_lowercase

PIECES_LOOKS={'K':('♔','♚'),'Q':('♕','♛'),'R':('♖','♜'),'B':('♗','♝'),'N':('♘','♞'),'P':('♙','♟'),'tile':('◻','◼')}
NOTATION_NAMES={'K':'King', 'Q':'Queen', 'R':'Rook', 'B':'Bishop', 'N':'Knight', 'P':'Pawn'}
NORMAL_BOARD={'P':list(zip([6**(x//8) for x in range(16)], [y%8 for y in range(16)])), 'N':[(0,1), (0,6), (7,1), (7,6)],
              'B':[(0,2),(0,5),(7,2),(7,5)], 'R':[(0,0),(0,7),(7,0),(7,7)],'Q':[(0,3),(7,3)], 'K':[(0,4),(7,4)]}

# blatantly stolen from StackOverflow. Thank you sixthgear for the code
def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


def notation_translator(square):
    if type(square) == str:
        square = square.lower()
        return (8-int(square[1]), ascii_lowercase.index(square[0]))
    elif type(square) == tuple:
        return ascii_lowercase[square[1]]+str(8-square[0])

class Piece:
    move_conf = ['line_mover', (0, 1), (1, 0), (0,-1),(-1,0)]

    def __init__(self,  color: bool, pos: tuple, curr_board: object): # in color, True represents white and False black
        self.color = color
        self.pos = pos
        self.curr_board = curr_board
        self.moved=0

    def probe_move(self, pos: tuple):
        place=self.curr_board.full_board[pos[0]][pos[1]]
        if place:
            if place.color == self.color:
                return 'ally'
            else:
                return 'enemy'
        else:
            return 'empty'

    def list_moves(self):
        valid_moves = []
        if self.move_conf[0]=='line_mover':
            for move in self.move_conf[1:]:
                i=1
                while i<8:
                    potential_pos=(move[0]*i+self.pos[0], move[1]*i+self.pos[1])
                    if 0<=potential_pos[0]<=7 and 0<=potential_pos[1]<=7:
                        if self.probe_move(potential_pos)=='empty':
                            valid_moves.append(potential_pos)
                        elif self.probe_move(potential_pos)=='enemy':
                            valid_moves.append(potential_pos)
                            break
                        else:
                            break
                    i+=1
        elif self.move_conf[0]=='point_mover':
            for move in self.move_conf[1:]:
                potential_pos=(move[0]+self.pos[0], move[1]+self.pos[1])
                if 0<=potential_pos[0]<=7 and 0<=potential_pos[1]<=7:
                    if self.probe_move(potential_pos)=='empty':
                        valid_moves.append(potential_pos)
                    elif self.probe_move(potential_pos)=='enemy':
                        valid_moves.append(potential_pos)
                    else:
                        continue
        return (valid_moves)


class Pawn(Piece):
    name='P'
    def __init__(self, color: bool, pos: tuple, curr_board: object):
        super().__init__(color, pos, curr_board)

    def list_moves(self):
        valid_moves = []
        ahead=(self.pos[0]+(1-(2*self.color)), self.pos[1])
        if not self.curr_board.full_board[ahead[0]][ahead[1]]:
            valid_moves.append(ahead)
            if self.moved==0:
                if not self.curr_board.full_board[ahead[0]+(1-(2*self.color))][ahead[1]]:
                    valid_moves.append((ahead[0]+(1-(2*self.color)), self.pos[1]))
        if self.pos[1]>0:
            if self.curr_board.full_board[self.pos[0]+(1-(2*self.color))][self.pos[1]-1]:
                if self.curr_board.full_board[self.pos[0]+(1-(2*self.color))][self.pos[1]-1].color!=self.color:
                    valid_moves.append((self.pos[0]+(1-(2*self.color)),self.pos[1]-1))
        if self.pos[1]<7:
            t1=self.curr_board.full_board[self.pos[0]+(1-(2*self.color))][self.pos[1]+1]
            if self.curr_board.full_board[self.pos[0]+(1-(2*self.color))][self.pos[1]+1]:
                if self.curr_board.full_board[self.pos[0]+(1-(2*self.color))][self.pos[1]+1].color!=self.color:
                    valid_moves.append((self.pos[0]+(1-(2*self.color)),self.pos[1]+1))
        return valid_moves


class King(Piece):
    name='K'
    move_conf = ['point_mover', (1,1),(1,0),(0,1),(-1,-1),(0,-1),(-1,0),(1,-1),(-1,1)]
    def __init__(self, color: bool, pos: tuple, curr_board: object):
        super().__init__(color, pos, curr_board)


class Queen(Piece):
    name='Q'
    move_conf = ['line_mover', (0, 1), (1, 0), (0,-1),(-1,0),(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def __init__(self, color: bool, pos: tuple, curr_board: object):
        super().__init__(color, pos, curr_board)


class Rook(Piece):
    name='R'
    move_conf = ['line_mover', (0, 1), (1, 0), (0,-1),(-1,0)]

    def __init__(self, color: bool, pos: tuple, curr_board: object):
        super().__init__(color, pos, curr_board)


class Bishop(Piece):
    name='B'
    move_conf = ['line_mover', (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def __init__(self, color: bool, pos: tuple, curr_board: object):
        super().__init__(color, pos, curr_board)


class Knight(Piece):
    name='N'
    move_conf = ['point_mover', (2,1),(-2,1),(2,-1),(-2,-1),(1,2),(-1,2),(1,-2),(-1,-2)]
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
        # self.full_board=Board.empty_board.copy()
        self.full_board=[[0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0]]
        if auto:
            self.make_board(conf)


    def show_board(self)->None:
        print('    ', end='')
        for numb in range(8):
            print(string.ascii_lowercase[numb], end='    ')
        print()
        for y in range(8):
            print(8-y, end=' ')
            for x in range(8):
                if self.full_board[y][x]:
                    print(PIECES_LOOKS[self.full_board[y][x].name][self.full_board[y][x].color]+'  ', end='')
                else:
                    print(PIECES_LOOKS['tile'][(x+y+1)%2]+' ', end='')
            print(8-y, end='')
            print()
        print('    ', end='')
        for numb in range(8):
            print(string.ascii_lowercase[numb], end='    ')
        print()

    def make_board(self, conf: dict):
        for piece_type in conf.keys():
            for piece in conf[piece_type]:
                self.full_board[piece[0]][piece[1]]=str_to_class(NOTATION_NAMES[piece_type])(bool(piece[0]//4), piece, self)

    def move(self, place, to):
        mover=self.full_board[place[0]][place[1]]
        self.full_board[to[0]][to[1]]=mover
        self.full_board[place[0]][place[1]]=0
        mover.pos=(to[0],to[1])
        mover.moved+=1

    def list_pieces(self, side: bool, movable=False):
        for y in range(8):
            for x in range(8):
                if self.full_board[y][x]:
                    if self.full_board[y][x].color==side:
                        if not movable:
                            yield self.full_board[y][x]
                        elif self.full_board[y][x].list_moves():
                            yield self.full_board[y][x]

    def start_of_the_turn(self):
        wKing=False
        bKing=False
        for y in range(8):
            for x in range(8):
                if self.full_board[y][x]:
                    piece=self.full_board[y][x]
                    if type(piece)==Pawn and y in [0,7]:
                        piece=Queen(piece.color, piece.pos, piece.curr_board)
                        print(f'Pawn at {notation_translator((y,x))} got promoted')
                    elif type(piece)==King:
                        if piece.color:
                            wKing=True
                        else:
                            bKing=True
        if not wKing:
            print('black won. Press enter to exit')
            input()
            exit()
        elif not bKing:
            print('white won. Press enter to exit')
            input()
            exit()


def run():
    board = Board()
    side=True
    while True:
        move_list=[]
        board.show_board()
        board.start_of_the_turn()
        if side:
            print('white to move. Your movable pieces:')
        else:
            print('black to move. Your movable pieces:')
        for i in board.list_pieces(side, movable=True):
            move_list.append(notation_translator(i.pos))
            print(i.name+notation_translator(i.pos), end=' | ')
        print(f'Choose piece to move. (example: {notation_translator((random.randint(0,8),random.randint(0,8)))})')
        while True:
            choice=input('> ')
            if choice in move_list:
                break
            else:
                print('Invalid square')
        coords=notation_translator(choice)
        move_list=board.full_board[coords[0]][coords[1]].list_moves()
        print('Available moves:')
        for move in move_list:
            print(notation_translator(move), end=' | ')
        print(f'Choose where to move. (example: {notation_translator((random.randint(0,8),random.randint(0,8)))})')
        while True:
            choice = input('> ')
            choice=notation_translator(choice)
            if choice in move_list:
                break
            else:
                print('Invalid move')
        board.move(coords, choice)
        side=not side


if __name__ == '__main__':
    run()