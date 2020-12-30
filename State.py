class GameState():
    def __init__(self):
        self.board = [
            ["br","bn","bb","bq","bk","bb","bn","br"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
        ]
        self.whiteToMove=True
        self.moveLog=[]

    def makeMove(self,move):
        pieceToMove=self.board[move.sr][move.sc]
        self.board[move.sr][move.sc]="--"
        self.board[move.er][move.ec]=pieceToMove
        self.whiteToMove= not self.whiteToMove

#start si end sunt 2 vectori cu cate 2 pozitii 0 - l , 1 -  c
class Move():
    def __init__(self, start, end, board):
        self.sr=start[0]
        self.sc=start[1]
        self.er=end[0]
        self.ec=end[1]