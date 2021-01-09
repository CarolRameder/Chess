#print("hei")
class GameState():
    def __init__(self):
        self.board = [
            ["br","bn","bb","bq","bk","bb","bn","br"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","br","--","--","--","wp","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wr","wn","wb","wq","wk","wb","wn","wr"]
        ]
        self.whiteToMove=True
        self.moveLog=[]

    def makeMove(self,move):
        pieceToMove=self.board[move.sr][move.sc]
        self.board[move.sr][move.sc]="--"
        self.board[move.er][move.ec]=pieceToMove
        self.whiteToMove= not self.whiteToMove


    def getValidMov(self):
        return self.getAllPosMov()

    def getAllPosMov(self):
        moves=[] #lista de mutari ce va fi returnata
        #parcurg tabla , tinand cont de cine urmeaza sa mute
        for i in range(8):
            for j in range(8):
                color= self.board[i][j][0]#pe prima pozitie vom avea mereu culoarea piesei
                if (color=='b' and self.whiteToMove is False)  or (color=='w' and self.whiteToMove):
                    pType=self.board[i][j][1]
                    #print(pType)
                    if pType=='r':
                        self.getRookMov(i,j,moves) #adauga la moves[] toate mutarile posibile de pion de pe coordonatele date
                        #print("hei")
                    elif pType == 'k':
                        self.getKingMov(i, j, moves)
                    elif pType == 'q':
                        self.getQueenMov(i, j, moves)
                    elif pType == 'p':
                        self.getPawnMov(i, j, moves)
                    elif pType == 'b':
                        self.getBishopMov(i, j, moves)
                    elif pType == 'n':
                        self.getKnightMov(i, j, moves)
        return moves

    def getRookMov(self, i, j, moves):
        dir=((-1,0), (0, -1), (1,0), (0,1))
        if self.whiteToMove:
            opon='b'
        else:
            opon='w'
        print("These are ",i,j)
        for d in dir:
            for m in range(1,8):
                cri=i+d[0]*m
                crj=j+d[1]*m
                #print(cri, crj)
                if 0<=cri<= 7 and 0<=crj<= 7:
                    # empty
                    if self.board[cri][crj][0]=='-':
                        print(i,j,cri,crj)
                        moves.append(Move((i, j), (cri, crj), self.board))

                    #oponent
                    elif self.board[cri][crj][0]==opon:
                        print(i,j,cri, crj)
                        moves.append(Move((i, j), (cri, crj), self.board))
                        break
                    #piesa mea
                    else:
                        break
                else:
                    break

    def getKingMov(self, i, j, moves):
        pass

    def getQueenMov(self, i, j, moves):
        pass

    def getPawnMov(self, i, j, moves):
        #white pawn
        if self.whiteToMove:
            #one&two squares moves
            if self.board[i-1][j]=="--":
                moves.append(Move((i,j), (i-1,j), self.board))
                if i==6 and self.board[i-2][j]=="--":
                    moves.append(Move((i,j), (i-2,j), self.board))
            #capturing
            #left
            if j>=1:
                if self.board[i-1][j-1][0]=="b":
                    moves.append(Move((i, j), (i-1, j-1), self.board))
            #right
            if j<=6:
                if self.board[i-1][j+1][0]=="b":
                    moves.append(Move((i, j), (i-1, j+1), self.board))
        #black
        else:
            # one&two squares moves
            if self.board[i+1][j]=="--":
                moves.append(Move((i,j), (i+1,j), self.board))
                if i==1 and self.board[i+2][j]=="--":
                    moves.append(Move((i,j), (i+2,j), self.board))
            # capturing
            #right
            if j>=1:
                if self.board[i+1][j-1][0]=="w":
                    moves.append(Move((i, j), (i+1, j-1), self.board))
            #right
            if j<=6:
                if self.board[i+1][j+1][0]=="w":
                    moves.append(Move((i, j), (i+1, j+1), self.board))

    def getBishopMov(self, i, j, moves):
        pass

    def getKnightMov(self, i, j, moves):
        pass

#start si end sunt 2 vectori cu cate 2 pozitii 0 - l , 1 -  c
class Move():
    def __init__(self, start, end, board):
        self.sr=start[0]
        self.sc=start[1]
        self.er=end[0]
        self.ec=end[1]

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.sr == other.sr and self.sc == other.sc and self.er == other.er and self.ec == other.sc
