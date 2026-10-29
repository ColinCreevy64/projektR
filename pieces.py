class Piece:
    def __init__(self, i, j, side):
        self.i = i
        self.j = j
        self.side = side

    def valid_position(self, i, j):
        if i >= 0 and i <= 7 and j >= 0 and j <= 7:
            return True
        return False

    def occupied(self, i, j, board):
        if not self.valid_position(i, j):
            return 0
        
        if board[8 * i + j] == 0:
            return 0
        elif board[8 * i + j] > 0:
            return 1
        else:
            return -1

class Pawn(Piece): 
    def __init__(self, i, j, side):
        super().__init__(i, j, side)
        self.valid_moves = [0] * 4
        self.attacking = ['x'] * 4
        self.abs = 1
        self.show = 'P'

    def valid_positions(self, board):
        if self.side == -1:
            mod_i = 7 - self.i
            mod_j = 7 - self.j
        else:
            mod_i = self.i
            mod_j = self.j

        for i in range(3):
            if self.valid_position(mod_i-1, mod_j-1+i):
                self.valid_moves[i] = -1
        if self.valid_moves[0] and self.occupied(mod_i-1, mod_j-1, board) == -1:
            self.valid_moves[0] = 1
        if self.valid_moves[1] and self.occupied(mod_i-1, mod_j, board) == 0:
            self.valid_moves[1] = 1
        if self.valid_moves[2] and self.occupied(mod_i-1, mod_j+1, board) == -1:
            self.valid_moves[2] = 1

        if mod_i == 6:
            self.valid_moves[3] = -1
            if self.occupied(mod_i-2, mod_j, board) == 0:
                self.valid_moves[3] = 1

    def calc_attacking(self):
        if self.side == -1:
            mod_i = 7 - self.i
            mod_j = 7 - self.j
        else:
            mod_i = self.i
            mod_j = self.j

        position = mod_i * 8 + mod_j
        for i in range(-1, 2):
            if self.valid_moves[i+1] == 1:
                self.attacking[i+1] = position - 8 + i
            elif self.valid_moves[i+1] == -1:
                self.attacking[i+1] = -1 * (position - 8 + 1)
        if self.valid_moves[3] == 1:
            self.attacking[3] = position - 16
        elif self.valid_moves[3] == -1:
            self.attacking[3] = -1 * (position - 16)

class Rook(Piece):
    def __init__(self, i, j, side):
        super().__init__(i, j, side)
        self.valid_moves = [0] * 14
        self.attacking = ['x'] * 14
        self.abs = 2
        self.show = 'R'

    def valid_positions_public(self, board, valid_moves):
        if self.side == -1:
            mod_i = 7 - self.i
            mod_j = 7 - self.j
        else:
            mod_i = self.i
            mod_j = self.j

        incrementX = 0
        incrementY = 0
        checked = 0

        # check above
        occ = self.occupied(mod_i-(incrementX+1), mod_j, board)
        while self.valid_position(mod_i-(incrementX+1), mod_j) and occ <= 0:
            incrementX += 1
            if occ == -1:
                break
            occ = self.occupied(mod_i-(incrementX+1), mod_j, board)
        if self.valid_position(mod_i - (incrementX+1), mod_j):
            valid_moves[mod_i-(incrementX+1)] = -1
        for i in range(mod_i-incrementX, mod_i):
            valid_moves[checked + i] = 1
        checked += mod_i
        # check left
        occ = self.occupied(mod_i, mod_j-(incrementY+1), board)
        while self.valid_position(mod_i, mod_j-(incrementY+1)) and occ <= 0:
            incrementY += 1
            if occ == -1:
                break
            occ = self.occupied(mod_i, mod_j-(incrementY+1), board)
        if self.valid_position(mod_i, mod_j-(incrementY+1)):
            valid_moves[checked + mod_j-(incrementY+1)] = -1
        for i in range(mod_j-incrementY, mod_j):
            valid_moves[checked + i] = 1
        checked += mod_j
        # check right
        incrementX = 0
        incrementY = 0
        occ = self.occupied(mod_i, mod_j+(incrementY+1), board)
        while self.valid_position(mod_i, mod_j+(incrementY+1)) and occ <= 0:
            incrementY += 1
            if occ == -1:
                break
            occ = self.occupied(mod_i, mod_j+(incrementY+1), board)
        if self.valid_position(mod_i, mod_j+(incrementY+1)):
            valid_moves[checked + incrementY] = -1
        for i in range(incrementY):
            valid_moves[checked + i] = 1
        checked += 7 - mod_j
        # check below
        occ = self.occupied(mod_i+(incrementX+1), mod_j, board)
        while self.valid_position(mod_i+(incrementX+1), mod_j) and occ <= 0:
            incrementX += 1
            if occ == -1:
                break
            occ = self.occupied(mod_i+(incrementX+1), mod_j, board)
        if self.valid_position(mod_i+(incrementX+1), mod_j):
            valid_moves[checked + incrementX] = -1
        for i in range(incrementX):
            valid_moves[checked + i] = 1

        return valid_moves

    def valid_positions(self, board):
        self.valid_positions_public(board, self.valid_moves)

    def calc_attacking_public(self, valid_moves, attacking):
        if self.side == -1:
            mod_i = 7 - self.i
            mod_j = 7 - self.j
        else:
            mod_i = self.i
            mod_j = self.j

        for i in range(8):
            # calculate vertical
            if i < mod_i:
                if valid_moves[i] == 1:
                    attacking[i] = i * 8 + mod_j
                elif valid_moves[i] == -1:
                    attacking[i] = -1 * (i * 8 + mod_j)
            if i > mod_i:
                if valid_moves[i-1+7] == 1:                 
                    attacking[i-1+7] == i * 8 + mod_j
                elif valid_moves[i-1+7] == -1:
                    attacking[i-1+7] = -1 * (i * 8 + mod_j)

            # calculate horizontal
            if i != mod_i:
                if valid_moves[i+mod_i] == 1:
                    attacking[i+mod_i] == mod_i * 8 + i
                elif valid_moves[i+mod_i] == -1:
                    attacking[i+mod_i] = -1 * (mod_i * 8 + i)

        return attacking

    def calc_attacking(self):
        self.calc_attacking_public(self.valid_moves, self.attacking)

class Knight(Piece):
    def __init__(self, i, j, side):
        super().__init__(i, j, side)
        self.valid_moves = [0] * 8
        self.attacking = ['x'] * 8
        self.abs = 3
        self.show = 'H'

    def valid_positions(self, board):
        if self.side == -1:
            mod_i = 7 - self.i
            mod_j = 7 - self.j
        else:
            mod_i = self.i
            mod_j = self.j

        possible_moves = [[mod_i-2, mod_j-1], [mod_i-2, mod_j+1], [mod_i-1, mod_j-2], [mod_i-1, mod_j+2], [mod_i+1, mod_j-2], [mod_i+1, mod_j+2], [mod_i+2, mod_j-1], [mod_i+2, mod_j+1]]

        for i in range(8):
            if self.valid_position(possible_moves[i][0], possible_moves[i][1]):
                self.valid_moves[i] = -1
                if self.occupied(possible_moves[i][0], possible_moves[i][1], board) <= 0:
                    self.valid_moves[i] = 1

            
    def calc_attacking(self):
        if self.side == -1:
            mod_i = 7 - self.i
            mod_j = 7 - self.j
        else:
            mod_i = self.i
            mod_j = self.j

        possible_moves = [[mod_i-2, mod_j-1], [mod_i-2, mod_j+1], [mod_i-1, mod_j-2], [mod_i-1, mod_j+2], [mod_i+1, mod_j-2], [mod_i+1, mod_j+2], [mod_i+2, mod_j-1], [mod_i+2, mod_j+1]]

        for i in range(8):
            if self.valid_moves[i] == 1:
                self.attacking[i] = possible_moves[i][0] * 8 + possible_moves[i][1]
            elif self.valid_moves[i] == -1:
                self.attacking[i] = -1 * possible_moves[i][0] * 8 + possible_moves[i][1]

class Bishop(Piece):
    def __init__(self, i, j, side):
        super().__init__(i, j, side)
        self.valid_moves = [0] * 13
        self.attacking = ['x'] * 13
        self.abs = 4
        self.show = 'B'

    def valid_positions_public(self, board, valid_moves):
        if self.side == -1:
            mod_i = 7 - self.i
            mod_j = 7 - self.j
        else:
            mod_i = self.i
            mod_j = self.j

        increment = 0
        checked = 0

        # check upper left
        occ = self.occupied(mod_i-(increment+1), mod_j-(increment+1), board)
        while self.valid_position(mod_i-(increment+1), mod_j-(increment+1)) and occ <= 0:
            increment += 1
            if occ == -1:
                break
            occ = self.occupied(mod_i-(increment+1), mod_j-(increment+1), board)
        if self.valid_position(mod_i-(increment+1), mod_j-(increment+1)):
            valid_moves[increment] = -1
        for i in range(increment):
            valid_moves[checked + i] = 1
        checked += min(mod_i, mod_j)
        increment = 0
        # check upper right
        occ = self.occupied(mod_i-(increment+1), mod_j+(increment+1), board)
        while self.valid_position(mod_i-(increment+1), mod_j+(increment+1)) and occ <= 0:
            increment += 1
            if occ == -1:
                break
            occ = self.occupied(mod_i-(increment+1), mod_j+(increment+1), board)
        if self.valid_position(mod_i-(increment+1), mod_j+(increment+1)):
            valid_moves[checked + increment] = -1
        for i in range(increment):
            valid_moves[checked + i] = 1
        checked += min(mod_i, 7-mod_j)
        # check lower left
        occ = self.occupied(mod_i+(increment+1), mod_j-(increment+1), board)
        while self.valid_position(mod_i+(increment+1), mod_j-(increment+1)) and occ <= 0:
            increment += 1
            if occ == -1:
                break
            occ = self.occupied(mod_i+(increment+1), mod_j-(increment+1), board)
        if self.valid_position(mod_i+(increment+1), mod_j-(increment+1)):
            valid_moves[checked + increment] = -1
        for i in range(increment):
            valid_moves[checked + i] = 1
        checked += min(7-mod_i, mod_j)
        # check lower right
        occ = self.occupied(mod_i+(increment+1), mod_j+(increment+1), board)
        while self.valid_position(mod_i+(increment+1), mod_j+(increment+1)) and occ <= 0:
            increment += 1
            if occ == -1:
                break
            occ = self.occupied(mod_i+(increment+1), mod_j+(increment+1), board)
        if self.valid_position(mod_i+(increment+1), mod_j+(increment+1)):
            valid_moves[checked + increment] = -1
        for i in range(increment):
            valid_moves[checked + i] = 1

        return valid_moves

    def valid_positions(self, board):
        self.valid_positions_public(board, self.valid_moves)

    def calc_attacking_public(self, valid_moves, attacking):
        if self.side == -1:
            mod_i = 7 - self.i
            mod_j = 7 - self.j
        else:
            mod_i = self.i
            mod_j = self.j

        ul = min(mod_i, mod_j)
        ur = min(mod_i, 7-mod_j)
        bl = min(7-mod_i, mod_j)
        br = min(7-mod_i, 7-mod_j)
        for i in range(7):
            # calculate upper left
            if i < ul:
                if valid_moves[i] == 1:
                    attacking[i] = (mod_i-i-1) * 8 + (mod_j-i-1)
                elif valid_moves[i] == -1:
                    attacking[i] = -1 * ((mod_i-i-1) * 8 + (mod_j-i-1))
            # calculate upper right
            if i < ur:
                if valid_moves[i+ul] == 1:
                    attacking[i+ul] = (mod_i-i-1) * 8 + (mod_j+i+1)
                elif valid_moves[i+ul] == -1:
                    attacking[i+ul] = -1 * ((mod_i-i-1) * 8 + (mod_j+i+1))
            # calculate bottom left
            if i < bl:
                if valid_moves[i+ul+ur] == 1:
                    attacking[i+ul+ur] = (mod_i+i+1) * 8 + (mod_j-i-1)
                elif valid_moves[i+ul+ur] == -1:
                    attacking[i+ul+ur] = -1 * ((mod_i+i+1) * 8 + (mod_j-i-1))
            # calculate bottom right
            if i < br:
                if valid_moves[i+ul+ur+bl] == 1:
                    attacking[i+ul+ur+bl] = (mod_i+i+1) * 8 + (mod_j+i+1)
                elif valid_moves[i+ul+ur+bl] == -1:
                    attacking[i+ul+ur+bl] = -1 * ((mod_i+i+1) * 8 + (mod_j+i+1))

        return attacking

    def calc_attacking(self):
        self.calc_attacking_public(self.valid_moves, self.attacking)

class Queen(Piece):
    def __init__(self, i, j, side):
        super().__init__(i, j, side)
        self.valid_moves = [0] * 14 + [0] * 13
        self.attacking = ['x'] * 14 + ['x'] * 13
        self.abs = 5
        self.show = 'Q'

    def valid_positions(self, board):
        rook = Rook(self.i, self.j, self.side)
        bishop = Bishop(self.i, self.j, self.side)
        self.valid_moves[:14] = rook.valid_positions_public(board, self.valid_moves[:14])
        self.valid_moves[14:] = bishop.valid_positions_public(board, self.valid_moves[14:])

    def calc_attacking(self):
        rook = Rook(self.i, self.j, self.side)
        bishop = Bishop(self.i, self.j, self.side)
        self.attacking[:14] = rook.calc_attacking_public(self.valid_moves[:14], self.attacking[:14])
        self.attacking[14:] = bishop.calc_attacking_public(self.valid_moves[14:], self.attacking[14:])

class King(Piece):
    def __init__(self, i, j, side):
        super().__init__(i, j, side)
        self.valid_moves = [0] * 8
        self.attacking = ['x'] * 8
        self.abs = 6
        self.show = 'K'

    def valid_positions(self, board, pieces):
        if self.side == -1:
            mod_i = 7 - self.i
            mod_j = 7 - self.j
        else:
            mod_i = self.i
            mod_j = self.j

        possible = ['x'] * 8
        offset = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 and j != 0:
                    if self.valid_position(mod_i+i, mod_j+j):
                            if self.occupied(mod_i+i, mod_j+j, board) <= 0:
                                possible[(i+1) * 3 + (j+1) - offset] = (mod_i+i) * 8 + (mod_j+j)
                else:
                    offset = 1

        for piece in pieces:
            if piece.side == self.side or piece == self:
                continue
            else:
                if all(x == -1 for x in possible):
                    break
                for pos in piece.attacking:
                    if pos in possible:
                        possible[possible.index(pos)] = -1

        for i in range(8):
            if possible[i] != -1:
                self.valid_moves[i] = 1

    def calc_attacking(self, board):
        if self.side == -1:
            mod_i = 7 - self.i
            mod_j = 7 - self.j
        else:
            mod_i = self.i
            mod_j = self.j

        self.attacking = [-1] * 8
        offset = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 and j != 0:
                    if self.valid_position(mod_i+i, mod_j+j) and self.occupied(mod_i+i, mod_j+j, board) <= 0:
                            self.attacking[(i+1) * 3 + (j+1) - offset] = (mod_i+i) * 8 + (mod_j+j) 
                else:
                    offset = 1
            