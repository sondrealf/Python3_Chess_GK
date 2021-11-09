line=[" ","a","b","c","d","e","f","g","h  "]
hvite = "♜♝♞♛♚♟"
svarte = "♖♗♘♕♔♙"
tur = hvite
fjern = ""

cb = [
    ["♖","♗","♘","♕","♔","♘","♗","♖"],
    ["♙","♙","♙","♙","♙","♙","♙","♙"],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    ["♟","♟","♟","♟","♟","♟","♟","♟"],
    ["♜","♝","♞","♛","♚","♞","♝","♜"]
]

def printBrett(board):
    print("\u0332".join(" ".join(line)))
    for i in range(len(board)):
        last = board[i][-1:]
        last[0] += "|"
        print(str(len(board)-i)+"|"+"\u0332".join("l".join(board[i][:-1]+last)))
printBrett(cb)

def posYX(pos):
    pos = list(pos)
    while len(pos)!=2 or not pos[0].isalpha() or not pos[1].isnumeric() or int(pos[1])>8 or int(pos[1])<1:
        pos = input("Ikke gyldig, prøv igjen: ")
    return (8-int(pos[1]),ord(pos[0].lower())-97)

def sjakkpos(pos):
    return chr(97+pos[1])+str(8-pos[0])

def finnBrikke(board, pos):
    return board[pos[0]][pos[1]]

def flyttBrikke(board, pos1, pos2, brikke, gBrikke):
    global fjern
    board = board[:]
    board[pos1[0]] = board[pos1[0]][:]
    board[pos2[0]] = board[pos2[0]][:]

    fjern = board[pos2[0]][pos2[1]]
    board[pos1[0]][pos1[1]] = gBrikke
    board[pos2[0]][pos2[1]] = brikke

    return board

def lovligTrekk(board, pos1, brikke):
    trekk = []
    if brikke not in tur:
        return []

    #* Trekk for ♛♕, ♜♖ og ♝♗
    if brikke in "♛♕♜♖♝♗":
        pos = []
        if brikke in "♛♕♜♖":
            pos += [["pos1[1]-i>-1","(pos1[0],pos1[1]-i)"],["pos1[0]-i>-1","(pos1[0]-i,pos1[1])"],["pos1[1]+i<8","(pos1[0],pos1[1]+i)"],["pos1[0]+i<8","(pos1[0]+i,pos1[1])"]]
        if brikke in "♛♕♝♗":
            pos += [["pos1[0]+i<8 and pos1[1]+i<8","(pos1[0]+i,pos1[1]+i)"],["pos1[1]-i>-1 and pos1[0]-i>-1","(pos1[0]-i,pos1[1]-i)"],["pos1[0]-i>-1 and pos1[1]+i<8","(pos1[0]-i,pos1[1]+i)"],["pos1[0]+i<8 and pos1[1]-i>-1","(pos1[0]+i,pos1[1]-i)"]]
        
        for u in pos:
            i = 1
            while eval(u[0]):
                brikken = finnBrikke(board, eval(u[1]))
                if brikken not in tur:
                    trekk.append(eval(u[1]))
                if brikken in hvite+svarte:
                    break
                i += 1

    #* Trekk for ♚♔ og ♞♘
    if brikke in "♚♔♞♘":
        if brikke in "♚♔":
            pos = [["pos1[1] != 7","(pos1[0],pos1[1]+1)"],["pos1[1] != 0","(pos1[0],pos1[1]-1)"],["pos1[0] != 0","(pos1[0]-1,pos1[1])"],["pos1[0] != 7","(pos1[0]+1,pos1[1])"],["pos1[0] != 0 and pos1[1] != 7","(pos1[0]-1,pos1[1]+1)"],["pos1[0] != 0 and pos1[1] != 0","(pos1[0]-1,pos1[1]-1)"],["pos1[0] != 7 and pos1[1] != 7","(pos1[0]+1,pos1[1]+1)"],["pos1[0] != 7 and pos1[1] != 0","(pos1[0]+1,pos1[1]-1)"]]
        else:
            pos = [["pos1[0]+2 < 8 and pos1[1]+1 < 8","(pos1[0]+2,pos1[1]+1)"],["pos1[0]+2 < 8 and pos1[1]-1 > -1","(pos1[0]+2,pos1[1]-1)"],["pos1[0]+1 < 8 and pos1[1]+2 < 8","(pos1[0]+1,pos1[1]+2)"],["pos1[0]+1 < 8 and pos1[1]-2 > -1","(pos1[0]+1,pos1[1]-2)"],["pos1[0]-1 > -1 and pos1[1]+2 < 8","(pos1[0]-1,pos1[1]+2)"],["pos1[0]-1 > -1 and pos1[1]-2 > -1","(pos1[0]-1,pos1[1]-2)"],["pos1[0]-2 > -1 and pos1[1]+1 < 8","(pos1[0]-2,pos1[1]+1)"],["pos1[0]-2 > -1 and pos1[1]-1 > -1","(pos1[0]-2,pos1[1]-1)"]]

        for i in pos:
            if eval(i[0]):
                if finnBrikke(board, eval(i[1])) not in tur:
                    trekk.append(eval(i[1]))

    #* Trekk for ♟♙
    if brikke in "♟♙":
        if tur == svarte:
            steg, rad = (1, 1)
        else :
            steg, rad = (-1,6)
        
        pos = (pos1[0]+steg,pos1[1])
        if finnBrikke(board, pos) == " ":
            trekk.append(pos)
            pos = (pos1[0]+(2*steg),pos1[1])
            if finnBrikke(board, pos) == " " and pos1[0] == rad:
                trekk.append(pos)
                
        pos = [["pos1[1] != 7","(pos1[0]+steg,pos1[1]+1)"],["pos1[1] != 0","(pos1[0]+steg,pos1[1]-1)"]]
        for i in pos:
            if eval(i[0]):
                brikke2 = finnBrikke(board, eval(i[1]))
                if brikke2 != " " and brikke2 not in tur:
                    trekk.append(eval(i[1]))
    return trekk

def check(board):
    trekk = []
    rolle()
    for i in range(len(board)):
        for u in range(len(board[i])):
            if board[i][u] in tur:
                trekk += lovligTrekk(board, (i,u), board[i][u])
            rolle()
            if board[i][u] == tur[4]:
                konge = (i,u)
            rolle()
    rolle()
    if konge in trekk:
        return (True, trekk, konge)
    return (False, trekk, konge)

def rolle():
    global tur
    tur = [hvite, svarte][tur==hvite]

def sjakk(board):
    spiller = ["Hvit","Svart"][tur == svarte]
    
    sjekk, gtrekk, konge = check(board)
    if sjekk:
        trekk = [i for i in lovligTrekk(board, konge, tur[4]) if i not in check(flyttBrikke(board, konge, i, tur[4], " ")[:])[1]]
        if trekk == []:
            matt = True
            rolle()
            gtrekk = check(board)[1]
            rolle()
            for i in lovligTrekk(board, konge,tur[4]):
                gtrekk.pop(gtrekk.index(i))

            for i in gtrekk:
                gBrikke = board[i[0]][i[1]]
                board[i[0]][i[1]] = tur[0]
                test = check(board)[0]
                board[i[0]][i[1]] = gBrikke
                if not test:
                    matt = False
            if matt:
                return print(f"Sjakk matt! {spiller} tapte")
        print(f"{spiller} er i sjakk")
        brikke = tur[4]
    trekk = []
    feil = False
    while trekk==[]:
        if feil:
            print("Du skrev feil || valgte en feil brikke || brikken kan ikke flytte på seg")
        pos1 = posYX(input(f"Hvilken brikke ønsker {spiller} å flytte?(eks. c2) "))
        brikke = finnBrikke(board,pos1)
        trekk = lovligTrekk(board, pos1, brikke)
        feil = True

    sjakktrekk = [sjakkpos(i) for i in trekk]
    print(f"Trekk for {brikke}: {sjakktrekk}")

    pos2 = posYX(input(f"Hvor ønsker du å flytte {brikke}? "))
    while pos2 not in trekk:
        pos2 = posYX(input(f"Ikke et gyldig trekk, hvor ønsker du å flytte {brikke}? "))

    if check(flyttBrikke(board,pos1,pos2,brikke," "))[0]:
        print("-------------------")
        print("Det er ikke lov å sette seg selv i sjakk, prøv på nytt")
        print("-------------------")
        return sjakk(board)
    
    if brikke == "♟" and pos2[0]==0:
        brikke = ["♛","♜","♞","♝"][int(input("Hva ønsker du å promotere ♟ til [♛, ♜, ♞, ♝]?  1, 2, 3 eller 4? "))-1]
    if brikke == "♙" and pos2[0]==7:
        brikke = ["♕","♖","♘","♗"][int(input("Hva ønsker du å promotere ♙ til [♕, ♖, ♘, ♗]?  1, 2 eller 3? "))-1]
        
    board = flyttBrikke(board,pos1,pos2,brikke," ")
    printBrett(board)
    rolle()
    sjakk(board)
sjakk(cb)