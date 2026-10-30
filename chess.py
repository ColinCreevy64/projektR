import pieces as P

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
        self.pieces = []
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
                *([[0] * 14 for i in range(8)] for j in range(8)),
                [[0] * 7 for i in range(8)], 
                [[0] * 7] + [[0] * 9 for i in range(6)] + [[0] * 7],
                [[0] * 7] + [[0] * 9] + [[0] * 11 for i in range(4)] + [[0] * 9] + [[0] * 7],
                *([[[0] * 7] + [[0] * 9] + [[0] * 11] + [[0] * 13 for i in range(2)] + [[0] * 11] + [[0] * 9] + [[0] * 7] for j in range(2)]),           
                [[0] * 7] + [[0] * 9] + [[0] * 11 for i in range(4)] + [[0] * 9] + [[0] * 7],   
                [[0] * 7] + [[0] * 9 for i in range(6)] + [[0] * 7],
                [[0] * 7 for i in range(8)]
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
        # pjesaci
        for i in range(8):
            pawn = P.Pawn(1, i, -1)
            self.pieces.append(pawn)
            self.board0[8 + i] = pawn.side * pawn.abs
            self.board1[55 - i] = -1 * pawn.side * pawn.abs

            pawn = P.Pawn(6, i, 1)
            self.pieces.append(pawn)
            self.board0[48 + i] = pawn.side * pawn.abs
            self.board1[15 - i] = -1 * pawn.side * pawn.abs

        # kule
        for i in [0, 7]:
            rook = P.Rook(0, i, -1)
            self.pieces.append(rook)
            self.board0[i] = rook.side * rook.abs
            self.board1[63 - i] = -1 * rook.side * rook.abs

            rook = P.Rook(7, i, 1)
            self.pieces.append(rook)
            self.board0[56 + i] = rook.side * rook.abs
            self.board1[7 - i] = -1 * rook.side * rook.abs

        # konji
        for i in [1, 6]:
            knight = P.Knight(0, i, -1)
            self.pieces.append(knight)
            self.board0[i] = knight.side * knight.abs
            self.board1[63 - i] = -1 * knight.side * knight.abs

            knight = P.Knight(7, i, 1)
            self.pieces.append(knight)
            self.board0[56 + i] = knight.side * knight.abs
            self.board1[7 - i] = -1 * knight.side * knight.abs      

        # lovci
        for i in [2, 5]:
            bishop = P.Bishop(0, i, -1)
            self.pieces.append(bishop)
            self.board0[i] = bishop.side * bishop.abs
            self.board1[63 - i] = -1 * bishop.side * bishop.abs

            bishop = P.Bishop(7, i, 1)
            self.pieces.append(bishop)
            self.board0[56 + i] = bishop.side * bishop.abs
            self.board1[7 - i] = -1 * bishop.side * bishop.abs

        # kraljice
        queen = P.Queen(0, 3, -1)
        self.pieces.append(queen)
        self.board0[3] = queen.side * queen.abs
        self.board1[59] = -1 * queen.side * queen.abs

        queen = P.Queen(7, 3, 1)
        self.pieces.append(queen)
        self.board0[59] = queen.side * queen.abs
        self.board1[3] = -1 * queen.side * queen.abs

        # kralj
        king = P.King(0, 4, -1)
        self.pieces.append(king)
        self.board0[4] = king.side * king.abs
        self.board1[60] = -1 * king.side * king.abs

        king = P.King(7, 4, 1)
        self.pieces.append(king)
        self.board0[60] = king.side * king.abs
        self.board1[4] = -1 * king.side * king.abs

        for piece in self.pieces:
            if isinstance(piece, P.King):
                if piece.side == -1:
                    piece.valid_positions(self.board1, self.pieces)
                    piece.calc_attacking(self.board1)
                else:
                    piece.valid_positions(self.board0, self.pieces)
                    piece.calc_attacking(self.board0)

            else:
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
            print(8-i, end=' ')
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
                if isinstance(piece, P.Pawn):
                    valid[piece.abs-1][piece.i-1][piece.j][:] = piece.valid_moves
                else:
                    valid[piece.abs-1][piece.i][piece.j][:] = piece.valid_moves

        return valid

    def move_to_code(self, move):
        # input move of shape B1HC3 -> [piece, i, j, move_index]

        move = move.upper().strip()
        move = [move[:2], move[2], move[3:]]

        i = 7 - (int(move[0][1]) - 1)
        j = ord(move[0][0]) - ord('A')

        for piece in self.pieces:
            if piece.i == i and piece.j == j:
                if piece.show == move[1]:
                    k = 7 - (int(move[2][1]) - 1)
                    l = ord(move[2][0]) - ord('A') 
                    if piece.side == -1:
                        k = 7 - k
                        l = 7 - l

                    if k * 8 + l in piece.attacking:
                        move_index = piece.attacking.index(k * 8 + l)

                        return piece.abs-1, i, j, move_index
        return False

    def code_to_move(self, piece, i, j, move_index):
        move = ''
        for p in self.pieces:
            if p.i == i and p.j == j:
                if p.abs-1 == piece:
                    k = 7 - (p.attacking[move_index] // 8)
                    l = p.attacking[move_index] % 8
                    if p.side == -1:
                        k = 7 - k
                        l = 7 - l

                    move += chr(ord('A') + j)
                    move += str(8 - i)
                    move += p.show
                    move += chr(ord('A') + l)
                    move += str(k+1)

                    return move

        return False

    def calc_dependencies(self, i, j):
        dependent = []

        for piece in self.pieces:
            if (i * 8 + j) in piece.attacking or -1 * (i * 8 + j) in piece.attacking:
                dependent.append(piece)

        return dependent

    def move(self, piece, i, j, move_index, player_side):
        for p in self.pieces:
            if p.abs-1 == piece and p.i == i and p.j == j and p.side == player_side:
                if p.valid_moves[move_index] == 1:
                    k = p.attacking[move_index] // 8
                    l = p.attacking[move_index] % 8
                    if p.side == -1:
                        k = 7 - k
                        l = 7 - l

                    for remove in self.pieces:
                        if remove.i == k and remove.j == l:
                            self.pieces.remove(remove)
                            break

                    dependent = self.calc_dependencies(p.i, p.j)
                    dependent.extend(self.calc_dependencies(k, l))
                    print(dependent)
                    for d in dependent:
                        print(d)

                    self.board0[p.i * 8 + p.j] = 0
                    self.board1[(7-p.i) * 8 + (7-p.j)] = 0
                    p.i = k
                    p.j = l
                    self.board0[p.i * 8 + p.j] = p.side * p.abs
                    self.board1[(7-p.i) * 8 + (7-p.j)] = p.side * p.abs

                    for d in dependent:
                        if isinstance(d, P.King):
                            continue
                        if d.side == -1:
                            d.valid_positions(self.board1)
                        else:
                            d.valid_positions(self.board0)
                        d.calc_attacking()
                    self.pieces[-2].valid_positions(self.board1, self.pieces)
                    self.pieces[-2].calc_attacking(self.board1)
                    self.pieces[-1].valid_positions(self.board0, self.pieces)
                    self.pieces[-1].calc_attacking(self.board0)

                return True

        return False

    def player_move(self, player_side):
        move = input('Enter valid move: ')
        code = self.move_to_code(move)

        if code:
            return self.move(*code, player_side)

        return False

chess = Chess()
chess.initialization()
chess.position_print()
while True:
    correct = chess.player_move(chess.player)
    if correct:
        chess.player *= -1
        for piece in chess.pieces:
            print(piece.attacking)
        chess.position_print()
    else:
        print('enter valid move')




    
    