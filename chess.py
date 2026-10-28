import pieces as p

''' moves list (rows 8 to 1)
        default check from top left to bottom right
        pawn
            (8 + 6*12 + 8) + 4 * (2 + 6*3 + 2) + (3 + 6*4 + 3) = 206

        rook 
            64*14 = 896

        knight
            2 * (2*2 + 2*3 + 4*4) + 2 * (2*3 + 2*4 + 4*6) + 4 * (2*4 + 2*6 + 4*8) = 336

        bishop
        check by diagonals, from position outward
            2 * (8*7) + 2 * (2*7 + 6*9) + 2 * (2*7 + 2*9 + 4*11) + 2 * (2*7 + 2*9 + 2*11 + 2*13) = 560

        queen
            64*14 + 2 * (8*7) + 2 * (2*7 + 6*9) + 2 * (2*7 + 2*9 + 4*11) + 2 * (2*7 + 2*9 + 2*11 + 2*13) = 1456

        king
            2 * (2*3 + 6*5) + 6 * (2*5 + 6*8) = 420

        castles
            2
        
        total 3876
'''

class Chess:
    def __init__(self):
        self.board0 = [0] * 64
        self.board1 = [0] * 64   # board for white point of view and board for black point of view
        self.player = 1
        self.moves = [
            # pawn
            [
                [[0] * 8] + [[0] * 12 for i in range(6)] + [[0] * 8],
                *([[[0] * 2] + [[0] * 3 for i in range(6)] + [[0] * 2] for j in range(4)]), 
                [[0] * 3] + [[0] * 4 for i in range(6)] + [[0] * 3]
            ],
            # rook
            [
                    *([[0] * 14 for i in range(8)] for j in range(8))
            ],
            # knight
            [
                    [[0] * 2] + [[0] * 3] + [[0] * 4 for i in range(4)] + [[0] * 3] + [[0] * 2],
                    [[0] * 3] + [[0] * 4] + [[0] * 6 for i in range(4)] + [[0] * 4] + [[0] * 3],
                    *([[[0] * 4] + [[0] * 6] + [[0] * 8 for i in range(4)] + [[0] * 6] + [[0] * 4] for j in range(4)]),
                    [[0] * 3] + [[0] * 4] + [[0] * 6 for i in range(4)] + [[0] * 4] + [[0] * 3],
                    [[0] * 2] + [[0] * 3] + [[0] * 4 for i in range(4)] + [[0] * 3] + [[0] * 2],
            ],
            # bishop
            [
                    [[0] * 7 for i in range(8)], 
                    [[0] * 7] + [[0] * 9 for i in range(6)] + [[0] * 7],
                    [[0] * 7] + [[0] * 9] + [[0] * 11 for i in range(4)] + [[0] * 9] + [[0] * 7],
                    *([[[0] * 7] + [[0] * 9] + [[0] * 11] + [[0] * 13 for i in range(2)] + [[0] * 11] + [[0] * 9] + [[0] * 7] for j in range(2)]),           
                    [[0] * 7] + [[0] * 9] + [[0] * 11 for i in range(4)] + [[0] * 9] + [[0] * 7],   
                    [[0] * 7] + [[0] * 9 for i in range(6)] + [[0] * 7],
                    [[0] * 7 for i in range(8)]   
            ],
            # queen
            [
                [*([[0] * 14 for i in range(8)] for j in range(8))],
                [[[0] * 7 for i in range(8)], 
                [[0] * 7] + [[0] * 9 for i in range(6)] + [[0] * 7],
                [[0] * 7] + [[0] * 9] + [[0] * 11 for i in range(4)] + [[0] * 9] + [[0] * 7],
                *([[[0] * 7] + [[0] * 9] + [[0] * 11] + [[0] * 13 for i in range(2)] + [[0] * 11] + [[0] * 9] + [[0] * 7] for j in range(2)]),           
                [[0] * 7] + [[0] * 9] + [[0] * 11 for i in range(4)] + [[0] * 9] + [[0] * 7],   
                [[0] * 7] + [[0] * 9 for i in range(6)] + [[0] * 7],
                [[0] * 7 for i in range(8)]]
            ],
            # king
            [
                    [[0] * 3] + [[0] * 5 for i in range(6)] + [[0] * 3],
                    *([[[0] * 5] + [[0] * 8 for i in range(6)] + [[0] * 5] for j in range(6)]),
                    [[0] * 3] + [[0] * 5 for i in range(6)] + [[0] * 3],
            ],
            # castles
            [0, 0]
        ]

    def initialization(self):
        pieces = []

        # pjesaci
        for i in range(8):
            pawn = p.Pawn(1, i, -1)
            pieces.append(pawn)
            self.board0[8 + i] = pawn.side * pawn.abs
            self.board1[55 - i] = -1 * pawn.side * pawn.abs

            pawn = p.Pawn(7, i, 1)
            pieces.append(pawn)
            self.board0[48 + i] = pawn.side * pawn.abs
            self.board1[15 - i] = -1 * pawn.side * pawn.abs

        # kule
        for i in [0, 7]:
            rook = p.Rook(0, i, -1)
            pieces.append(rook)
            self.board0[i] = rook.side * rook.abs
            self.board1[63 - i] = -1 * rook.side * rook.abs

            rook = p.Rook(7, i, 1)
            pieces.append(rook)
            self.board0[56 + i] = rook.side * rook.abs
            self.board1[7 - i] = -1 * rook.side * rook.abs

        # konji
        for i in [1, 6]:
            knight = p.Knight(0, i, -1)
            pieces.append(knight)
            self.board0[i] = knight.side * knight.abs
            self.board1[63 - i] = -1 * knight.side * knight.abs

            knight = p.Knight(7, i, 1)
            pieces.append(knight)
            self.board0[56 + i] = knight.side * knight.abs
            self.board1[7 - i] = -1 * knight.side * knight.abs      

        # lovci
        for i in [2, 5]:
            bishop = p.Bishop(0, i, -1)
            pieces.append(bishop)
            self.board0[i] = bishop.side * bishop.abs
            self.board1[63 - i] = -1 * bishop.side * bishop.abs

            bishop = p.Bishop(7, i, 1)
            pieces.append(bishop)
            self.board0[56 + i] = bishop.side * bishop.abs
            self.board1[7 - i] = -1 * bishop.side * bishop.abs

        # kraljice
        queen = p.Queen(0, 3, -1)
        pieces.append(queen)
        self.board0[3] = queen.side * queen.abs
        self.board1[59] = -1 * queen.side * queen.abs

        queen = p.Queen(7, 3, 1)
        pieces.append(queen)
        self.board0[59] = queen.side * queen.abs
        self.board1[3] = -1 * queen.side * queen.abs

        # kralj
        king = p.King(0, 4, -1)
        pieces.append(king)
        self.board0[4] = king.side * king.abs
        self.board1[60] = -1 * king.side * king.abs

        king = p.King(7, 4, 1)
        pieces.append(king)
        self.board0[60] = king.side * king.abs
        self.board1[4] = -1 * king.side * king.abs

        for piece in pieces:
            if piece.side == -1:
                piece.valid_positions(self.board1)
            else:
                piece.valid_positions(self.board0)
            piece.calc_attacking()

    def position_print(self):
        print('    ', end='')
        for i in range(ord('a'), ord('i')):
            print(chr(i), end='  ')
        print('')
        for i in range(8):
            print(i+1, end=' ')
            for j in range(8):
                if self.board0[8 * i + j] < 0:
                    print(' ' + str(self.board0[8 * i + j]), end='')
                else:
                    print('  ' + str(self.board0[8 * i + j]), end='')
            print('')
    
    def valid_moves(self):
        # -1 -> valid position, invalid move
        # 0 -> invalid position
        # 1 -> valid move

        valid = self.moves.copy()
        valid[0][0] = valid[0][1].copy()

        for piece in self.pieces:
            if piece.side == 1:
                valid[piece.abs-1][piece.i][piece.j][:] = piece.valid_moves

        return valid

chess = Chess()
chess.initialization()
chess.position_print()
print(chess.valid_moves())


    
    