from Move import Move

class CastleRights:
    """
    Class for representing a castle move
    """

    def __init__(self, wks, bks, wqs, bqs):
        """
        Constructor method for castle representation
        :parameter wks - white king side
        :parameter bks - black king side
        :parameter wqs - white queen side
        :parameter bqs - black queen side
        """
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class GameState:
    """
    Class to represent the current state of the board
    """

    def __init__(self):
        """
        Constructor method
        """
        self.board = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
        ]

        self.turn_white = True
        self.moveLog = []
        self.wKingPos = (7, 4)
        self.bKingPos = (0, 4)

        #ends
        self.checkMate = False
        self.staleMate = False

        #rights
        self.enpas_pos = ()
        self.cr_castle_r = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.cr_castle_r.wks, self.cr_castle_r.bks,
                                             self.cr_castle_r.wqs, self.cr_castle_r.bqs)]

    def make_move(self, move, check_valid=True):
        """
        Check valid indicates if the move is generated for check validation and pins, or it's a real move
        :parameter move - object representing the move to be made
        :parameter check_valid - flag for validity of the move based on actual use in the game
        """
        self.board[move.sr][move.sc] = "--"
        self.board[move.er][move.ec] = move.pieceMoved
        self.moveLog.append(move)
        self.turn_white = not self.turn_white
        if move.pieceMoved == 'wk':
            self.wKingPos = (move.er, move.ec)
        elif move.pieceMoved == 'bk':
            self.bKingPos = (move.er, move.ec)

        if move.isEnpassantMove:
            self.board[move.sr][move.ec] = "--"

        if move.pieceMoved[1] == 'p' and abs(move.sr - move.er) == 2:
            self.enpas_pos = ((move.er + move.sr) // 2, move.ec)
        else:
            self.enpas_pos = ()

        if move.isPawnPromotion and not check_valid:
            promoted_piece = "a"
            while promoted_piece not in ('q', 'r', 'b', 'n'):
                promoted_piece = input("Promote to q, r, b, or n: ")
            self.board[move.er][move.ec] = move.pieceMoved[0] + promoted_piece

        # castle
        if move.castle:
            if move.ec - move.sc == 2:
                self.board[move.er][move.ec - 1] = self.board[move.er][move.ec + 1]
                self.board[move.er][move.ec + 1] = '--'
            else:
                self.board[move.er][move.ec + 1] = self.board[move.er][move.ec - 2]
                self.board[move.er][move.ec - 2] = '--'

        # castle rights on rook, king move
        self.update_castle_rights(move)
        self.castleRightsLog.append(CastleRights(self.cr_castle_r.wks, self.cr_castle_r.bks,
                                                 self.cr_castle_r.wqs, self.cr_castle_r.bqs))

    def update_castle_rights(self, move):
        """
        Method to update the castle move posibilities for both colours
        :parameter move - the move performed to be cheked against
        """
        #deleting the right to castle on moving k/r
        #King
        if move.pieceMoved == 'wk':
            self.cr_castle_r.wks = False
            self.cr_castle_r.wqs = False
        elif move.pieceMoved == 'bk':
            self.cr_castle_r.bks = False
            self.cr_castle_r.bqs = False

        #Rook
        elif move.pieceMoved == 'wR':
            if move.sr == 7:
                if move.sc == 0:
                    self.cr_castle_r.wqs = False
                elif move.sc == 7:
                    self.cr_castle_r.wks = False
        elif move.pieceMoved == 'bR':
            if move.sr == 0:
                if move.sc == 0:
                    self.cr_castle_r.bqs = False
                elif move.sc == 7:
                    self.cr_castle_r.bks = False

    def undo_move(self):
        """
        Method for undoing the moves made during the game
        """
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.sr][move.sc] = move.pieceMoved
            self.board[move.er][move.ec] = move.pieceCaptured
            self.turn_white = not self.turn_white

            # king pos
            if move.pieceMoved == 'wk':
                self.wKingPos = (move.sr, move.sc)
            elif move.pieceMoved == 'bk':
                self.bKingPos = (move.sr, move.sc)

            # enpassant
            if move.isEnpassantMove:
                self.board[move.er][move.ec] = "--"
                self.board[move.sr][move.ec] = move.pieceCaptured
                self.enpas_pos = (move.er, move.ec)

            # pawn x2
            if move.pieceMoved[1] == "p" and abs(move.sr - move.er) == 2:
                self.enpas_pos = ()

            # castle rights
            self.castleRightsLog.pop()
            self.cr_castle_r = self.castleRightsLog[-1]

            # castle moves
            if move.castle:
                if move.ec - move.sc == 2:
                    self.board[move.er][move.ec + 1] = self.board[move.er][move.ec - 1]
                    self.board[move.er][move.ec - 1] = '--'
                else:
                    self.board[move.er][move.ec - 2] = self.board[move.er][move.ec + 1]
                    self.board[move.er][move.ec + 1] = '--'

    def square_under_attack(self, r, c):
        """
        Checking if a certain square is under attack
        :param r: row of the square
        :param c: column of the square
        :return: boolean if the square is under attack
        """""
        self.turn_white = not self.turn_white
        opp_moves = self.get_all_possible_moves()
        self.turn_white = not self.turn_white
        for move in opp_moves:
            if move.er == r and move.ec == c:
                return True
        return False

    def in_check(self):
        """
        Method for checking if the any of the kings are in check
        """
        if self.turn_white:
            return self.square_under_attack(self.wKingPos[0], self.wKingPos[1])
        else:
            return self.square_under_attack(self.bKingPos[0], self.bKingPos[1])

    def get_valid_moves(self):
        """
        Method for computing all valid moves
        :return moves - a list of Move objects with all the valid moves
        """
        # castling and en-passant rights are stored, because move affects these values
        temp_enpassant_possible = self.enpas_pos
        temp_castle = CastleRights(self.cr_castle_r.wks, self.cr_castle_r.bks,
                                   self.cr_castle_r.wqs, self.cr_castle_r.bqs)

        # for validating a possible move
        #1 all possibile moves are generated
        #2 each pos moves are made
        #3 generate opponent move
        #4 check if any of those moves let the king attacked
        #5 moves which let the king in chess are eliminated
        #6 the moves are undone
        moves = self.get_all_possible_moves()  # 1

        # castle moves are directly introduced in valid moves
        if not self.turn_white:
            self.get_castle_moves(self.bKingPos[0], self.bKingPos[1], moves)
        else:
            self.get_castle_moves(self.wKingPos[0], self.wKingPos[1], moves)

        for i in range(len(moves) - 1, -1, -1):  # 2
            self.make_move(moves[i])
            # 3 #4
            self.turn_white = not self.turn_white
            if self.in_check():
                moves.remove(moves[i])  # 5
            self.turn_white = not self.turn_white
            self.undo_move()

        # game ending possibilities
        if len(moves) == 0:
            if self.in_check():
                self.checkMate = True
                print("Checkmate !")
            else:
                self.staleMate = True
                print("Stalemate !")
        else:
            self.checkMate = False
            self.staleMate = False

        # the rigths are restored, and the values are not affected
        self.enpas_pos = temp_enpassant_possible
        self.cr_castle_r = temp_castle

        return moves

    def get_all_possible_moves(self):
        """
        Method for getting a list of all the possible moves based on the rules of chess
        :return moves
        """
        moves = []
        for i in range(8):
            for j in range(8):
                color = self.board[i][j][0]
                if (color == 'b' and not self.turn_white) or (color == 'w' and self.turn_white):
                    p_type = self.board[i][j][1]
                    if p_type == 'r':
                        self.get_rook_moves(i, j, moves)
                    elif p_type == 'k':
                        self.get_king_moves(i, j, moves)
                    elif p_type == 'q':
                        self.get_queen_moves(i, j, moves)
                    elif p_type == 'p':
                        self.get_pawn_moves(i, j, moves)
                    elif p_type == 'b':
                        self.get_bishop_moves(i, j, moves)
                    elif p_type == 'n':
                        self.get_knight_moves(i, j, moves)
        return moves

    def get_rook_moves(self, i, j, moves):
        """
        Method for computing all the moves based on rock piece movement
        :parameter i - row on which the rock is
        :parameter j - column on which the rock is
        :parameter moves - list of all the possible moves
        """
        # the rook can move in 4 directions
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))

        # player's turn are important de determine what pieces they can capture
        if self.turn_white:
            oponent_colour = 'b'
        else:
            oponent_colour = 'w'

        # all 4 directions are covered as long as the fields are empty
        for d in directions:
            for m in range(1, 8):
                cri = i + d[0] * m
                crj = j + d[1] * m
                if 0 <= cri <= 7 and 0 <= crj <= 7:  # check if the table ends
                    # the landing square mai be empty
                    if self.board[cri][crj] == '--':
                        moves.append(Move((i, j), (cri, crj), self.board))
                    # oponent_colour piece that may be captured
                    elif self.board[cri][crj][0] == oponent_colour:
                        moves.append(Move((i, j), (cri, crj), self.board))
                        break
                    # own piece
                    else:
                        break
                else:
                    break

    def get_king_moves(self, i, j, moves):
        """
        Method for computing all the moves based on king piece movement
        :parameter i - row on which the king is
        :parameter j - column on which the king is
        :parameter moves - list of all possible moves
        """
        directions = ((1, 1), (1, -1), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (-1, 0))
        if self.turn_white:
            oponent = 'b'
        else:
            oponent = 'w'
        for d in directions:
            cri = i + d[0]
            crj = j + d[1]
            if 0 <= cri <= 7 and 0 <= crj <= 7:
                # empty
                if self.board[cri][crj][0] == '-':
                    moves.append(Move((i, j), (cri, crj), self.board))

                # oponent
                elif self.board[cri][crj][0] == oponent:
                    moves.append(Move((i, j), (cri, crj), self.board))

    def get_castle_moves(self, r, c, moves):
        """
        Method for computing all castle moves
        :parameter r - row on which the move is being performed
        :parameter c - column on which the move is being performed
        :parameter moves - list of all possible moves
        """
        if self.square_under_attack(r, c):
            return

        #king side
        #checking previous rights and player turn
        if (self.cr_castle_r.wks and self.turn_white) or (self.cr_castle_r.bks and not self.turn_white):
            if self.board[r][c + 2] == '--' and self.board[r][c + 1] == '--':
                if self.square_under_attack(r, c + 2) is False and self.square_under_attack(r, c + 1) is False:
                    moves.append(Move((r, c), (r, c + 2), self.board, castle=True))

        #queen side
        if (self.turn_white and self.cr_castle_r.wqs) or (not self.turn_white and self.cr_castle_r.bqs):
            if self.board[r][c - 2]== '--' and self.board[r][c - 1] == '--' and self.board[r][c - 3] == '--':
                if self.square_under_attack(r, c - 1) is False and self.square_under_attack(r, c - 2) is False:
                    moves.append(Move((r, c), (r, c - 2), self.board, castle=True))

    def get_bishop_moves(self, i, j, moves):
        """
        Method for computing all the moves based on king piece movement
        :param i: row on which the bishop is
        :param j: column on which the bishop is
        :param moves: list of all possible moves
        """
        directions = ((-1, 1), (1, -1), (1, 1), (-1, -1))
        if self.turn_white:
            oponent = 'b'
        else:
            oponent = 'w'
        for d in directions:
            for m in range(1, 8):
                cri = i + d[0] * m
                crj = j + d[1] * m
                if 0 <= cri <= 7 and 0 <= crj <= 7:
                    # empty
                    if self.board[cri][crj][0] == '-':
                        # print(i, j, cri, crj)
                        moves.append(Move((i, j), (cri, crj), self.board))

                    # oponent
                    elif self.board[cri][crj][0] == oponent:
                        # print(i, j, cri, crj)
                        moves.append(Move((i, j), (cri, crj), self.board))
                        break
                    # piesa mea
                    else:
                        break
                else:
                    break

    def get_queen_moves(self, i, j, moves):
        """
        Method for computing all the moves based on quenn piece movement
        :param i: row on which the queen is
        :param j: column on which the queen is
        :param moves: list of all the moves possible
        """
        self.get_rook_moves(i, j, moves)
        self.get_bishop_moves(i, j, moves)

    def get_pawn_moves(self, i, j, moves):
        """
        Method for computing all the moves based on pawn piece movement
        :param i: row on which the pawn is
        :param j: column on which the pawn is
        :param moves: list of all the moves possible
        """
        # white pawn
        if self.turn_white:
            # one&two squares moves
            if self.board[i - 1][j] == "--":
                moves.append(Move((i, j), (i - 1, j), self.board))
                if i == 6 and self.board[i - 2][j] == "--":
                    moves.append(Move((i, j), (i - 2, j), self.board))
            # capturing
            # left
            if j >= 1:
                if self.board[i - 1][j - 1][0] == "b":
                    moves.append(Move((i, j), (i - 1, j - 1), self.board))
                elif (i - 1, j - 1) == self.enpas_pos:
                    moves.append(Move((i, j), (i - 1, j - 1), self.board, enpassant=True))

            # right
            if j <= 6:
                if self.board[i - 1][j + 1][0] == "b":
                    moves.append(Move((i, j), (i - 1, j + 1), self.board))
                elif (i - 1, j + 1) == self.enpas_pos:
                    moves.append(Move((i, j), (i - 1, j + 1), self.board, enpassant=True))
        # black
        else:
            # one&two squares moves
            if self.board[i + 1][j] == "--":
                moves.append(Move((i, j), (i + 1, j), self.board))
                if i == 1 and self.board[i + 2][j] == "--":
                    moves.append(Move((i, j), (i + 2, j), self.board))
            # capturing
            # left
            if j >= 1:
                if self.board[i + 1][j - 1][0] == "w":
                    moves.append(Move((i, j), (i + 1, j - 1), self.board))
                elif (i + 1, j - 1) == self.enpas_pos:
                    moves.append(Move((i, j), (i + 1, j - 1), self.board, enpassant=True))
            # right
            if j <= 6:
                if self.board[i + 1][j + 1][0] == "w":
                    moves.append(Move((i, j), (i + 1, j + 1), self.board))
                elif (i + 1, j + 1) == self.enpas_pos:
                    moves.append(Move((i, j), (i + 1, j + 1), self.board, enpassant=True))

    def get_knight_moves(self, i, j, moves):
        """
        Method for computing all the moves based on knight piece movement
        :param i: row on which knight is
        :param j: column on which knight is
        :param moves: list of all possible moves
        """
        directions = ((2, 1), (2, -1), (1, 2), (1, -2), (-2, 1), (-2, -1), (-1, 2), (-1, -2))
        if self.turn_white:
            opon = 'b'
        else:
            opon = 'w'
        for d in directions:
            cri = i + d[0]
            crj = j + d[1]
            if 0 <= cri <= 7 and 0 <= crj <= 7:
                # empty
                if self.board[cri][crj][0] == '-':
                    moves.append(Move((i, j), (cri, crj), self.board))

                # oponent
                elif self.board[cri][crj][0] == opon:
                    moves.append(Move((i, j), (cri, crj), self.board))