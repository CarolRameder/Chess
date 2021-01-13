class Move:
    """
    Class to define a move
    It contains all the information needed for representing a move
    """
    def __init__(self, start, end, board, enpassant=False, castle=False):
        """
        Constructor method for Move class
        :parameter start: tuple for representing coordinates of starting square
        :parameter end: tuple for representing coordinates of target square
        :parameter board: state object for representing game at a current state
        :parameter enpassant: flag for enpassant move :default = False
        :parameter castle: flag for castle move :default = False
        """
        self.sr = start[0]
        self.sc = start[1]
        self.er = end[0]
        self.ec = end[1]
        self.pieceCaptured = board[self.er][self.ec]

        self.pieceMoved = board[self.sr][self.sc]
        if self.pieceMoved == 'wp' and self.er == 0 or self.pieceMoved == "bp" and self.er == 7:
            self.isPawnPromotion = True
        else:
            self.isPawnPromotion = False

        self.isEnpassantMove = enpassant
        if self.isEnpassantMove:
            if self.pieceMoved == 'bp':
                self.pieceCaptured = 'wp'
            else:
                self.pieceCaptured = "bp"

        self.castle = castle

    def __eq__(self, other):
        """
        Override of equal operation using moveID
        :parameter other: move to be compared with
        """
        if isinstance(other, Move):
            return self.sr == other.sr and self.sc == other.sc and self.er == other.er and self.ec == other.ec
        return False

    #used for debugging
    def __str__(self):
        """
        String representation for a move
        :return: move_string
        """
        move_string = "Move: start_row: " + str(self.sr) + \
                      " start_column: " + str(self.sc) + " end_row: " + str(self.er) \
                      + " end_column " + str(self.ec) + '\n'
        return move_string

    def __repr__(self):
        """
        Unreferenced representation for move object
        :return: move_string
        """
        move_string = "Move: start_row: " + str(self.sr) + \
                      " start_column: " + str(self.sc) + " end_row: " + str(self.er) \
                      + " end_column " + str(self.ec) + '\n'
        return move_string
