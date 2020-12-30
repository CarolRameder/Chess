from State import GameState
from State import Move
import pygame as pg


#set up
wid=512
height=512
dim=8
field_sz=height//dim
img={}
MAX_FPS=15

pg.init()
screen=pg.display.set_mode((wid,height))

#incarc imaginile intr-un vector, pentru a fi mai optima afisarea lor
def loadimg():
    pieces=['bp', 'br','bn','bb','bk','bq','wp', 'wr','wn','wb','wk','wq']
    for p in pieces:
        img[p]=pg.transform.scale(pg.image.load("images/"+p+".png"), (field_sz, field_sz))


def draw(board):
    colors=[pg.Color("white"), pg.Color("grey")]
    for r in range(dim):
        for c in range(dim):
            col=colors[((r+c)%2)]#cand suma coordonatelor e para , campul este alb, valabil din oricare parte
            pg.draw.rect(screen, col, pg.Rect(c*field_sz, r*field_sz, field_sz, field_sz))
            piesa=board[r][c]
            if piesa != "--":
                screen.blit(img[piesa], pg.Rect(c*field_sz, r*field_sz, field_sz, field_sz))


def main():
    click2 = []
    evn=()
    screen.fill(pg.Color("white"))
    curent=GameState()
    loadimg()
    running=True
    while running:
        for e in pg.event.get():
            if e.type== pg.QUIT:
                running=False
            elif e.type==pg.MOUSEBUTTONDOWN:
                loc=pg.mouse.get_pos()
                col=loc[0]//field_sz
                lin=loc[1]//field_sz
                evn=(lin, col)
                click2.append(evn)
            if len(click2)==2:
                move=Move(click2[0], click2[1],curent.board)
                curent.makeMove(move)
                evn=()
                click2=[]
        draw(curent.board)
        pg.display.flip()

if __name__ == "__main__":
    main()
