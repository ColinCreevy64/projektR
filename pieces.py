class Piece:
    def __init__(self, i, j, side):
        self.i = i
        self.j = j
        self.side = side
        self.dependencies = []

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

    def calc_dependencies(self, pieces):
        for piece in pieces:
            if piece.i * 8 + piece.j in self.attacking:
                piece.dependencies.append(self)

class Pawn(Piece): 
    def __init__(self, i, j, side):
        super().__init__(i, j, side)
        self.valid_moves = [0] * 4
        self.attacking = [-1] * 4
        self.abs = 1
        self.show = 'P'

    def valid_positions(self, board):
        for i in range(3):
            if self.valid_position(self.i-1, self.j-1+i):
                self.valid_moves[i] = -1
        if self.valid_moves[0] and self.occupied(self.i-1, self.j-1, board) == -1:
            self.valid_moves[0] = 1
        if self.valid_moves[1] and self.occupied(self.i-1, self.j, board) == 0:
            self.valid_moves[1] = 1
        if self.valid_moves[2] and self.occupied(self.i-1, self.j+1, board) == -1:
            self.valid_moves[2] = 1

        if self.i == 6:
            self.valid_moves[3] = -1
            if self.occupied(self.i-2, self.j, board) == 0:
                self.valid_moves[3] = 1

    def calc_attacking(self):
        position = self.i * 8 + self.j
        for i in range(-1, 2):
            if self.valid_moves[i+1] == 1:
                self.attacking[i+1] == position - 8 + i
        if self.valid_moves[3] == 1:
            self.attacking[3] = position - 16

class Rook(Piece):
    def __init__(self, i, j, side):
        super().__init__(i, j, side)
        self.valid_moves = [0] * 14
        self.attacking = [-1] * 14
        self.abs = 2
        self.show = 'R'

    def valid_positions_public(self, board, valid_moves):
        incrementX = 0
        incrementY = 0
        checked = 0

        # check above
        occ = self.occupied(self.i-(incrementX+1), self.j, board)
        while self.valid_position(self.i-(incrementX+1), self.j) and occ <= 0:
            incrementX += 1
            if occ == -1:
                break
            occ = self.occupied(self.i-(incrementX+1), self.j, board)
        for i in range(self.i-incrementX, self.i):
            valid_moves[checked + i] = 1
        checked += self.i
        # check left
        occ = self.occupied(self.i, self.j-(incrementY+1), board)
        while self.valid_position(self.i, self.j-(incrementY+1)) and occ <= 0:
            incrementY += 1
            if occ == -1:
                break
            occ = self.occupied(self.i, self.j-(incrementY+1), board)
        for i in range(self.j-incrementY, self.j):
            valid_moves[checked + i] = 1
        checked += self.j
        # check right
        incrementX = 0
        incrementY = 0
        occ = self.occupied(self.i, self.j+(incrementY+1), board)
        while self.valid_position(self.i, self.j+(incrementY+1)) and occ <= 0:
            incrementY += 1
            if occ == -1:
                break
            occ = self.occupied(self.i, self.j+(incrementY+1), board)
        for i in range(incrementY):
            valid_moves[checked + i] = 1
        checked += 7 - self.j
        # check below
        occ = self.occupied(self.i+(incrementX+1), self.j, board)
        while self.valid_position(self.i+(incrementX+1), self.j) and occ <= 0:
            incrementX += 1
            if occ == -1:
                break
            occ = self.occupied(self.i+(incrementX+1), self.j, board)
        for i in range(incrementX):
            valid_moves[checked + i] = 1

        return valid_moves

    def valid_positions(self, board):
        self.valid_positions_public(board, self.valid_moves)

    def calc_attacking_public(self, valid_moves, attacking):
        for i in range(8):
            # calculate vertical
            if i < self.i:
                if valid_moves[i] == 1:
                    attacking[i] = i * 8 + self.j
            if i > self.i:
                if valid_moves[i+7] == 1:                 
                    attacking[i+7] == i * 8 + self.j

            # calculate horizontal
            if i != self.i:
                if valid_moves[i+self.i] == 1:
                    attacking[i+self.i] == self.i * 8 + i

        return attacking

    def calc_attacking(self):
        self.calc_attacking_public(self.valid_moves, self.attacking)

class Knight(Piece):
    def __init__(self, i, j, side):
        super().__init__(i, j, side)
        self.valid_moves = [0] * 8
        self.attacking = [-1] * 8
        self.abs = 3
        self.show = 'H'

    def valid_positions(self, board):
        possible_moves = [[self.i-2, self.j-1], [self.i-2, self.j+1], [self.i-1, self.j-2], [self.i-1, self.j+2], [self.i+1, self.j-2], [self.i+1, self.j+2], [self.i+2, self.j-1], [self.i+2, self.j+1]]

        for i in range(8):
            if self.valid_position(possible_moves[i][0], possible_moves[i][1]):
                self.valid_moves[i] = -1
                if self.occupied(possible_moves[i][0], possible_moves[i][1], board) <= 0:
                    self.valid_moves[i] = 1

            
    def calc_attacking(self):
        possible_moves = [[self.i-2, self.j-1], [self.i-2, self.j+1], [self.i-1, self.j-2], [self.i-1, self.j+2], [self.i+1, self.j-2], [self.i+1, self.j+2], [self.i+2, self.j-1], [self.i+2, self.j+1]]

        for i in range(8):
            if self.valid_moves[i] == 1:
                self.attacking[i] = possible_moves[i][0] * 8 + possible_moves[i][1]

class Bishop(Piece):
    def __init__(self, i, j, side):
        super().__init__(i, j, side)
        self.valid_moves = [0] * 13
        self.attacking = [-1] * 13
        self.abs = 4
        self.show = 'B'

    def valid_positions_public(self, board, valid_moves):
        increment = 0
        checked = 0

        # check upper left
        occ = self.occupied(self.i-(increment+1), self.j-(increment+1), board)
        while self.valid_position(self.i-(increment+1), self.j-(increment+1)) and occ <= 0:
            increment += 1
            if occ == -1:
                break
            occ = self.occupied(self.i-(increment+1), self.j-(increment+1), board)
        for i in range(increment):
            valid_moves[checked + i] = 1
        checked += min(self.i, self.j)
        increment = 0
        # check upper right
        occ = self.occupied(self.i-(increment+1), self.j+(increment+1), board)
        while self.valid_position(self.i-(increment+1), self.j+(increment+1)) and occ <= 0:
            increment += 1
            if occ == -1:
                break
            occ = self.occupied(self.i-(increment+1), self.j+(increment+1), board)
        for i in range(increment):
            valid_moves[checked + i] = 1
        checked += min(self.i, 7-self.j)
        # check lower left
        occ = self.occupied(self.i+(increment+1), self.j-(increment+1), board)
        while self.valid_position(self.i+(increment+1), self.j-(increment+1)) and occ <= 0:
            increment += 1
            if occ == -1:
                break
            occ = self.occupied(self.i+(increment+1), self.j-(increment+1), board)
        for i in range(increment):
            valid_moves[checked + i] = 1
        checked += min(7-self.i, self.j)
        # check lower right
        occ = self.occupied(self.i+(increment+1), self.j+(increment+1), board)
        while self.valid_position(self.i+(increment+1), self.j+(increment+1)) and occ <= 0:
            increment += 1
            if occ == -1:
                break
            occ = self.occupied(self.i+(increment+1), self.j+(increment+1), board)
        for i in range(increment):
            valid_moves[checked + i] = 1

        return valid_moves

    def valid_positions(self, board):
        self.valid_positions_public(board, self.valid_moves)

    def calc_attacking_public(self, valid_moves, attacking):
        ul = min(self.i, self.j)
        ur = min(self.i, 7-self.j)
        bl = min(7-self.i, self.j)
        br = min(7-self.i, 7-self.j)
        for i in range(7):
            # calculate upper left
            if i < ul:
                if valid_moves[i] == 1:
                    attacking[i] = (self.i-i) * 8 + (self.j-i)
            # calculate upper right
            if i < ur:
                if valid_moves[i+ul] == 1:
                    attacking[i+ul] = (self.i-i) * 8 + (self.j+i)
            # calculate bottom left
            if i < bl:
                if valid_moves[i+ul+ur] == 1:
                    attacking[i+ul+ur] = (self.i+i) * 8 + (self.j-i)
            # calculate bottom right
            if i < br:
                if valid_moves[i+ul+ur+bl] == 1:
                    attacking[i+ul+ur+bl] = (self.i+i) * 8 + (self.j+i)

        return attacking

    def calc_attacking(self):
        self.calc_attacking_public(self.valid_moves, self.attacking)

class Queen(Piece):
    def __init__(self, i, j, side):
        super().__init__(i, j, side)
        self.valid_moves = [[0] * 14, [0] * 13]
        self.attacking = [[-1] * 14, [-1] * 13]
        self.abs = 5
        self.show = 'Q'

    def valid_positions(self, board):
        rook = Rook(self.i, self.j, self.side)
        bishop = Bishop(self.i, self.j, self.side)
        self.valid_moves[0] = rook.valid_positions_public(board, self.valid_moves)
        self.valid_moves[1] = bishop.valid_positions_public(board, self.valid_moves)

    def calc_attacking(self):
        rook = Rook(self.i, self.j, self.side)
        bishop = Bishop(self.i, self.j, self.side)
        self.attacking[0] = rook.calc_attacking_public(self.valid_moves, self.attacking)
        self.attacking[1] = bishop.calc_attacking_public(self.valid_moves, self.attacking)

class King(Piece):
    def __init__(self, i, j, side):
        super().__init__(i, j, side)
        self.valid_moves = [-1] * 8
        self.attacking = [-1] * 8
        self.abs = 6
        self.show = 'K'

    def valid_positions(self, board, pieces):
        possible = [-1] * 8
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 and j != 0:
                    if self.valid_position(self.i+i, self.j+j, board):
                            possible[(i+1) * 3 + (j+1)] = (self.i+i) * 8 + (self.j+j)

        for piece in pieces:
            if piece == self:
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
        self.attacking = [-1] * 8
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 and j != 0:
                    if self.valid_position(self.i+i, self.j+j, board):
                            self.attacking[(i+1) * 3 + (j+1)] = (self.i+i) * 8 + (self.j+j) 
            