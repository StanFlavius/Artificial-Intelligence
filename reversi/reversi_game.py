import copy
import sys
import time
import pygame


# FUNCTIE CARE CONTRIBUIE LA REALIZAREA INTERFETEI GRAFICE A JOCULUI (GRID-UL)
def draw_grid(display, table):
    width_box = height_box = 80
    white_piece_image = pygame.image.load('white.png')
    black_piece_image = pygame.image.load('black.png')
    white_piece_image = pygame.transform.scale(white_piece_image, (width_box, height_box))
    black_piece_image = pygame.transform.scale(black_piece_image, (width_box, height_box))

    # GRID-UL ESTE PASTRAT SUB FORMA UNEI MATRICI DE BOX-URI DE 80*80
    grid = []
    for row in range(len(table)):
        grid_row = []
        for column in range(len(table[row])):
            box = pygame.Rect(column * (width_box + 1), row * (height_box + 1), width_box, height_box)
            grid_row.append(box)
            pygame.draw.rect(display, (255, 255, 255), box)
            if table[row][column] == 'w':
                display.blit(white_piece_image, (column * width_box, row * height_box))
            elif table[row][column] == 'b':
                display.blit(black_piece_image, (column * width_box, row * height_box))
        grid.append(grid_row)
    pygame.display.flip()
    return grid


# FUNCTIE CARE AJUTA LA REALIZAREA UNEI LISTE DE WEIGHTS (CONTRIBUIE LA REALIZARA UNEI MATRICI DE WEIGHTS, UTILIZATA LA CALCULAREA UNEI EURISTICI)
def create_line_weights(a, b, c, d):
    line = []
    line.append(a)
    line.append(b)
    line.append(c)
    line.append(d)
    copy_line = line
    rev_line = list(reversed(copy_line))
    row = []
    row.extend(line)
    row.extend(rev_line)
    return row


# FUNCTIA CARE FORMEAZA O MATRICE DE WEIGHTS PENTRU CALCULAREA UNEI EURISTICI
def create_matrix_weights():
    matrix = []
    first_row = create_line_weights(100, -20, 10, 5)
    second_row = create_line_weights(-20, -50, -2, -2)
    third_row = create_line_weights(10, -2, -1, -1)
    forth_row = create_line_weights(5, -2, -1, -1)
    matrix.append(first_row)
    matrix.append(second_row)
    matrix.append(third_row)
    matrix.append(forth_row)
    matrix.append(forth_row)
    matrix.append(third_row)
    matrix.append(second_row)
    matrix.append(first_row)
    return matrix


# CLASA 'GAME' DEFINESTE JOCUL SI PASTREAZA URMATOARELE DATE
#   DIMENSIUNEA TABLE, PRECUM SI TABLA
#   CULORILE JUCATORULUI SI A CALCULATORULUI
class Game:
    dimension = 8
    JMIN = None
    JMAX = None
    Empty = '#'

    # FUNCTIE DE CREARE A TABLEI (INITIAL IA FORMA DESCRISA IN FUNCTIE, IAR PE PARCURS IA FORMA DATA CA PARAMETRU)
    def __init__(self, t=None):
        if t != None:
            self.table = t
        else:
            self.table = []
            row = []
            for it1 in range(8):
                row = []
                for it2 in range(8):
                    row.append(self.__class__.Empty)
                self.table.append(row)
            self.table[3][3] = self.table[4][4] = 'w'
            self.table[3][4] = self.table[4][3] = 'b'
            '''for i in range(8):
                for j in range(8):
                    self.table[i][j] = 'b'

            self.table[1][0] = self.table[1][3] = self.table[1][4] = self.table[1][5] = 'w'
            self.table[4][0] = self.table[4][3] = 'w'
            self.table[0][5] = 'w'
            self.table[5][0] = self.table[5][1] = self.table[5][3] = self.table[5][4] = 'w'
            self.table[6][0] = self.table[6][1] = self.table[6][4] = self.table[6][5] = 'w'
            for i in range(7):
                self.table[7][i] = self.table[i][7] = 'w'
            self.table[7][7] = '#' '''

    # FUNCTIE CARE CALCULEAZA PUNCTAJELE FIECARUI PARTICIPANT LA JOC
    def calculate_score(self):
        nr_JMIN = 0
        nr_JMAX = 0
        for i in self.table:
            for j in i:
                if j == self.JMIN:
                    nr_JMIN += 1
                elif j == self.JMAX:
                    nr_JMAX += 1
        return (nr_JMIN, nr_JMAX)

    # FUNCTIE CARE VERIFICA DACA S-A AJUNS INTR-O STARE FINALA (MAI INTAI VERIFICA DACA AMBII PARTICIPANTI DAU PASS, IAR IN CAZ AFIRMATIV INSEAMNA CA S-A AJUNS LA O STARE FINALA)
    def isFinal(self):
        # VEDEM DACA PLAYER-UL MAI POATE FACE MUTARI
        list_possible_moves = get_possible_box(self.table)
        for (row, column) in list_possible_moves:
            copyTable = copy.deepcopy(self.table)
            moves = getAllMoves(copyTable, row, column, self.JMIN)
            if 1 in moves:
                return False
        # VEDEM DACA MAI POATE FACE MUTARI CALCULATORUL
        for (row, column) in list_possible_moves:
            copyTable = copy.deepcopy(self.table)
            moves = getAllMoves(copyTable, row, column, self.JMAX)
            if 1 in moves:
                return False

        # NICIUNUL NU MAI POATE FACE MUTARI, DECI AM AJUNS LA FINAL SI LE CALCULAM SCORURILE SI STABILIM CONCLUZIA
        (nr_JMIN, nr_JMAX) = self.calculate_score()
        if nr_JMIN > nr_JMAX:
            return self.JMIN
        elif nr_JMAX > nr_JMIN:
            return self.JMAX
        else:
            return 'REMIZA'

    # STABILIM POSIBILELE MUTARI
    def moves(self, player):
        list_moves = []
        list_possible_moves = get_possible_box(self.table)  # LUAM TOATE BOXU-URILE POSIBILE
        for (row, column) in list_possible_moves:
            copyTable = copy.deepcopy(self.table)
            # VERIFICAM DACA UN BOX ESTE VALID SAU NU
            moves = getAllMoves(copyTable, row, column, player)
            if 1 in moves:
                modifyTable(copyTable, moves, row, column, player)
                list_moves.append(Game(copyTable))
        return list_moves

    # EURISTICA NR.1 - PRIN INTERMEDIUL UNEI MATRICI DE WEIGHTS
    # FIECARE CELULA ARE O VALOARE IN FUNCTIE DE IMPORTANTA SA STRATEGICA PE TABLA(DE EX. COLTURILE SUNT CELE MAI IMPORTANTE DEOARECE NU MAI POT FI CUCERITE APOI)
    # LA CALCULAREA FORMULEI SE ATRIBUIE +1 PENTRU JMAX SI -1 PENTRU JMIN - ASTFEL SE ASIGURA MAXIMIZAREA LUI JMAX SI MINIMIZAREA LUI JMIN
    def calculate_heuristic_1(self, depth, currPlayer):
        situation_final = self.isFinal()
        if situation_final == self.JMIN:
            return (-99 - depth)
        elif situation_final == self.JMAX:
            return (99 + depth)
        elif situation_final == "REMIZA":
            return 0
        else:
            matrix_of_weights = create_matrix_weights()
            value = 0
            for i in range(len(self.table)):
                for j in range(len(self.table[i])):
                    if self.table[i][j] == self.JMAX:
                        value += matrix_of_weights[i][j]
                    elif self.table[i][j] == self.JMIN:
                        value -= matrix_of_weights[i][j]
            return value

    # EURISTICA NR.2 - NR. DE COLTURI CAPTURATE / NR DE MISCARI POSIBILE
    # COLTURILE SUNT BOX-URILE CELE MAI IMPORTANTE
    # PRIN INTERMEDIUL '(nr_corners_jmax - nr_corners_jmin)' MAXIMIZAM LA CALCULATOR SI MINIMIZAM LA PLAYER
    # MAXIMIZARE / MINIMIZARE FACEM SI PRIN INTERMEDIUL NR. DE MISCARI DISPONIBILE PT FIECARE PARTICIPANT
    # PRIN INTERMEDIUL '(nr_moves_jmax - nr_moves_jmin) // (nr_moves_jmin + nr_corners_jmax)' MAXIMIZAM LA CALCULATOR SI MINIMIZAM LA PLAYER
    def calculate_heuristic_2(self, depth):
        situation_final = self.isFinal()
        if situation_final == self.JMIN:
            return (-99 - depth)
        elif situation_final == self.JMAX:
            return (99 + depth)
        elif situation_final == "REMIZA":
            return 0
        else:
            nr_moves_jmax = 0
            list_possible_moves = get_possible_box(self.table)
            for (row, column) in list_possible_moves:
                copyTable = copy.deepcopy(self.table)
                moves = getAllMoves(copyTable, row, column, self.JMAX)
                if 1 in moves:
                    nr_moves_jmax += 1

            nr_moves_jmin = 0
            list_possible_moves = get_possible_box(self.table)
            for (row, column) in list_possible_moves:
                copyTable = copy.deepcopy(self.table)
                moves = getAllMoves(copyTable, row, column, self.JMIN)
                if 1 in moves:
                    nr_moves_jmin += 1

            nr_corners_jmax = 0
            if self.table[0][0] == self.JMAX:
                nr_corners_jmax += 1
            if self.table[0][7] == self.JMAX:
                nr_corners_jmax += 1
            if self.table[7][0] == self.JMAX:
                nr_corners_jmax += 1
            if self.table[7][7] == self.JMAX:
                nr_corners_jmax += 1

            nr_corners_jmin = 0
            if self.table[0][0] == self.JMIN:
                nr_corners_jmin += 1
            if self.table[0][7] == self.JMIN:
                nr_corners_jmin += 1
            if self.table[7][0] == self.JMIN:
                nr_corners_jmin += 1
            if self.table[7][7] == self.JMIN:
                nr_corners_jmin += 1

            return 10 * (nr_corners_jmax - nr_corners_jmin) + (nr_moves_jmax - nr_moves_jmin) // (nr_moves_jmin + nr_corners_jmax)

#CLASA FOLOSITA DE ALGORITMII MIN_MAX SI ALPHA_BETA
class State:
    def __init__(self, table_game, currPlayer, depth, score=None):
        self.table_game = table_game #TABLA
        self.currPlayer = currPlayer #PARTICIPANTUL
        self.depth = depth  #ADANCIMEA
        self.score = score #SCORUL
        self.next_moves = [] #VIITOARELE CONFIGURATII
        self.optimal_move = None #CONFIGURATIA CEA MAI BUNA

    # GENERAM POSIBILELE CONFIGURATII DE JOC
    def moves(self):
        list_moves = self.table_game.moves(self.currPlayer)
        list_next_moves = []
        for move in list_moves:
            list_next_moves.append(State(move, getOtherColor(self.currPlayer), self.depth - 1))
        return list_next_moves

#FUNCTIE AJUTATOARE CARE OFERA TOATE BOX-URILE UNDE S-AR PUTEA PUNE O PIESA (VALIDE + INVALIDE)
def get_possible_box(table):
    list_boxes = []
    for i in range(Game.dimension):
        for j in range(Game.dimension):
            if table[i][j] == Game.Empty:
                if i - 1 >= 0 and table[i - 1][j] != Game.Empty:
                    list_boxes.append((i, j))
                elif i - 1 >= 0 and j + 1 <= Game.dimension - 1 and table[i - 1][j + 1] != Game.Empty:
                    list_boxes.append((i, j))
                elif j + 1 <= Game.dimension - 1 and table[i][j + 1] != Game.Empty:
                    list_boxes.append((i, j))
                elif i + 1 <= Game.dimension - 1 and j + 1 <= Game.dimension - 1 and table[i + 1][j + 1] != Game.Empty:
                    list_boxes.append((i, j))
                elif i + 1 <= Game.dimension - 1 and table[i + 1][j] != Game.Empty:
                    list_boxes.append((i, j))
                elif i + 1 <= Game.dimension - 1 and j - 1 >= 0 and table[i + 1][j - 1] != Game.Empty:
                    list_boxes.append((i, j))
                elif j - 1 >= 0 and table[i][j - 1] != Game.Empty:
                    list_boxes.append((i, j))
                elif i - 1 >= 0 and j - 1 >= 0 and table[i - 1][j - 1] != Game.Empty:
                    list_boxes.append((i, j))
    return list_boxes

#ALGORITMUL MIN_MAX
def min_max_algorithm(state):
    if state.depth == 0 or state.table_game.isFinal():
        state.score = state.table_game.calculate_heuristic_1(state.depth, state.currPlayer)
        return state

    #IAU VIITOARELE CONFIGURATII
    state.next_moves = state.moves()

    #APLICA MIN_MAX PE ELE
    future_moves = [min_max_algorithm(move) for move in state.next_moves]

    # print(state.table_game.isFinal())
    # print(future_moves)
    # print(Game.JMIN)
    if state.currPlayer == state.table_game.JMIN:
        #IAU CONFIGURATIA MINIMA DEOARECE SUNT IN CAZUL LUI JMIN
        state.optimal_move = min(future_moves, key=lambda x: x.score)
    elif state.currPlayer == state.table_game.JMAX:
        #IAU CONFIGURATIA MAXIMA DEOARECE SUNT IN CAZUL LUI JMAX
        state.optimal_move = max(future_moves, key=lambda x: x.score)
    state.score = state.optimal_move.score

    return state

#ALGORITMUL ALPHA_BETA
def alpha_beta_algorithm(alpha, beta, state):
    if state.depth == 0 or state.table_game.isFinal():
        state.score = state.table_game.calculate_heuristic_1(state.depth, state.currPlayer)
        return state

    if alpha > beta: #INTERVLA INVALID => STOP
        return state

    state.next_moves = state.moves()

    if state.currPlayer == Game.JMAX:
        #CALCULEZ SCORUL
        currScore = float('-inf')
        for move in state.next_moves:
            newState = alpha_beta_algorithm(alpha, beta, move)
            # print("curr" + str(currScore))
            # print(newState.score)
            if currScore < newState.score:
                state.optimal_move = newState
                currScore = newState.score
            if alpha < newState.score:
                alpha = newState.score
                if alpha >= beta:
                    break

    elif state.currPlayer == Game.JMIN:
        # CALCULEZ SCORUL
        currScore = float('inf')
        for move in state.next_moves:
            newState = alpha_beta_algorithm(alpha, beta, move)
            if currScore > newState.score:
                state.optimal_move = newState
                currScore = newState.score
            if beta > newState.score:
                beta = newState.score
                if alpha >= beta:
                    break

    state.score = state.optimal_move.score
    return state

#FUNCTIE AJUTATOARE CARE DA CULOAREA CELUILALT PARTICIPANT
def getOtherColor(color):
    if color == 'b':
        return 'w'
    else:
        return 'b'

#FUNCTIE AJUTATOARE CARE PRECIZEAZA DACA PUNAND PIESA DE CULOARE color PE POZITIA position VA DETERMINA O CONFIGURATIE VALIDA IN STANGA
def verify_line_right(line, color, position):
    if position + 1 >= len(line):
        return 0
    elif line[position + 1] != getOtherColor(color):
        return 0
    ok_right = 0
    for it in range(position + 1, len(line)):
        # print(it)
        if line[it] == getOtherColor(color):
            ok_right = 1
        elif line[it] == Game.Empty:
            ok_right = 0
            break
        elif line[it] == color:
            if ok_right == 1:
                ok_right = 2
                break
    if ok_right == 2:
        return 1
    return 0

#FUNCTIE AJUTATOARE CARE PRECIZEAZA DACA PUNAND PIESA DE CULOARE color PE POZITIA position VA DETERMINA O CONFIGURATIE VALIDA IN DREAPTA
def verify_line_left(line, color, position):
    if position - 1 < 0:
        return 0
    elif line[position - 1] != getOtherColor(color):
        return 0
    ok_left = 0
    for it in range(position - 1, -1, -1):
        # print(it)
        if line[it] == getOtherColor(color):
            ok_left = 1
        elif line[it] == Game.Empty:
            ok_left = 0
            break
        elif line[it] == color:
            if ok_left == 1:
                ok_left = 2
                break

    if ok_left == 2:
        return 1
    return 0

#FUNCTIE AJUTATOARE CARE PRECIZEAZA DACA PUNAND PIESA DE CULOARE color PE POZITIA position VA DETERMINA O CONFIGURATIE VALIDA
def verify_line(line, color, position):
    ok_right = verify_line_right(line, color, position)
    ok_left = verify_line_left(line, color, position)

    '''print(ok_left)
    print(ok_right)'''

    if ok_left == 0 and ok_right == 0:
        return 0
    return 1

#FUNCTIE AJUTATOARE CARE IA RANDUL AFERENT UNUI BOX DETERMINAT PRIN row SI column
def get_row(table, row, column):
    list_for_row = []
    # add left
    list_for_row_left = []
    copy_column = column
    while copy_column >= 0:
        list_for_row_left.append(table[row][copy_column])
        copy_column -= 1
    # add right
    list_for_row_right = []
    copy_column = column + 1
    while copy_column <= Game.dimension - 1:
        list_for_row_right.append(table[row][copy_column])
        copy_column += 1
    list_for_row_left.reverse()
    for i in list_for_row_left:
        list_for_row.append(i)
    for i in list_for_row_right:
        list_for_row.append(i)
    return (list_for_row, column)

#FUNCTIE AJUTATOARE IA COLOANA AFERENTA UNUI BOX DETERMINAT PRIN row SI column
def get_column(table, row, column):
    list_for_column = []
    # ADD UP
    list_for_column_up = []
    copy_row = row
    while copy_row >= 0:
        list_for_column_up.append(table[copy_row][column])
        copy_row -= 1
    # ADD DOWN
    copy_row = row + 1
    list_for_column_down = []
    while copy_row <= Game.dimension - 1:
        list_for_column_down.append(table[copy_row][column])
        copy_row += 1
    list_for_column_up.reverse()
    for i in list_for_column_up:
        list_for_column.append(i)
    for i in list_for_column_down:
        list_for_column.append(i)
    return (list_for_column, row)

#FUNCTIE AJUTATOARE IA DIAGONALA PRINCIPALA AFERENTA UNUI BOX DETERMINAT PRIN row SI column
def get_pp_diagonal(table, row, column):
    list_for_pp_diag = []
    # ADD UP
    list_for_pp_diag_up = []
    copy_row = row
    copy_column = column
    while copy_column >= 0 and copy_row >= 0:
        list_for_pp_diag_up.append(table[copy_row][copy_column])
        copy_column -= 1
        copy_row -= 1

    # ADD DOWN
    list_for_pp_diag_down = []
    copy_row = row + 1
    copy_column = column + 1
    while copy_column <= Game.dimension - 1 and copy_row <= Game.dimension - 1:
        list_for_pp_diag_down.append(table[copy_row][copy_column])
        copy_column += 1
        copy_row += 1

    list_for_pp_diag_up.reverse()
    for i in list_for_pp_diag_up:
        list_for_pp_diag.append(i)
    for i in list_for_pp_diag_down:
        list_for_pp_diag.append(i)
    return (list_for_pp_diag, len(list_for_pp_diag_up))

#FUNCTIE AJUTATOARE IA DIAGONALA SECUNDARA AFERENTA UNUI BOX DETERMINAT PRIN row SI column
def get_sec_diagonal(table, row, column):
    list_for_sec_diag = []
    # ADD UP
    list_for_sec_diag_up = []
    copy_row = row
    copy_column = column
    while copy_column <= Game.dimension - 1 and copy_row >= 0:
        list_for_sec_diag_up.append(table[copy_row][copy_column])
        copy_column += 1
        copy_row -= 1
    # ADD DOWN
    list_for_sec_diag_down = []
    copy_row = row + 1
    copy_column = column - 1
    while copy_column >= 0 and copy_row <= Game.dimension - 1:
        list_for_sec_diag_down.append(table[copy_row][copy_column])
        copy_column -= 1
        copy_row += 1
    list_for_sec_diag_up.reverse()
    for i in list_for_sec_diag_up:
        list_for_sec_diag.append(i)
    for i in list_for_sec_diag_down:
        list_for_sec_diag.append(i)
    return (list_for_sec_diag, len(list_for_sec_diag_up))

#FUNCTIE AJUTATOARE CARE PREIA RANDUL, COLOANA, DIAGONALA PP SI DIAGONALA SEC AFERENTE UNUI BOX DETERMINAT DE row SI column SI PRECIZEAZA PT FIECARE DACA SE POATE REALIZA O CONFIGURATIE VALIDA
def getAllMoves(table, row, column, color):
    if row < 0 or row > 8:
        return 0

    if column < 0 or column > 8:
        return 0

    move = []
    # print(get_row(table, row, column)[0])
    # print(column)
    move.append(verify_line(get_row(table, row, column)[0], color, column))
    move.append(verify_line(get_column(table, row, column)[0], color, row))
    move.append(verify_line(get_pp_diagonal(table, row, column)[0], color, get_pp_diagonal(table, row, column)[1] - 1))
    move.append(
        verify_line(get_sec_diagonal(table, row, column)[0], color, get_sec_diagonal(table, row, column)[1] - 1))
    return move

#FUNCTIE AJUTATOARE CARE MODIFICA O LINIE CONFORM REGULILOR JOCULUI
def modifyLine(line, position, color):
    # MODIFY TO THE RIGHT IF POSSIBLE
    ok_right = 0
    for it in range(position + 1, len(line)):
        # print(it)
        if line[it] == getOtherColor(color):
            ok_right = 1
        elif line[it] == Game.Empty:
            ok_right = 0
            break
        elif line[it] == color:
            if ok_right == 1:
                ok_right = 2
                break
    if ok_right == 2:
        for it in range(position + 1, len(line)):
            if line[it] == getOtherColor(color):
                line[it] = color
            elif line[it] == color:
                break
    # MODIFY TO THE LEFT IF POSSIBLE
    ok_left = 0
    for it in range(position - 1, -1, -1):
        # print(it)
        if line[it] == getOtherColor(color):
            ok_left = 1
        elif line[it] == Game.Empty:
            ok_left = 0
            break
        elif line[it] == color:
            if ok_left == 1:
                ok_left = 2
                break

    if ok_left == 2:
        for it in range(position - 1, -1, -1):
            if line[it] == getOtherColor(color):
                line[it] = color
            elif line[it] == color:
                break

    #MODIFY IN THAT POSITION
    line[position] = color
    return line

#FUNCTIE AJUTATOARE CARE MODIFICA O TABLA DE JOC
def modifyTable(table, moves, row, column, color):
    for it in range(len(moves)):
        if moves[it]:
            if it == 0: #RANDUL
                line = get_row(table, row, column)[0]
                pos = column
                modified_line = modifyLine(line, pos, color)
                # MODIFY LEFT
                copy_column = column
                copy_pos = pos
                while copy_column >= 0:
                    table[row][copy_column] = modified_line[copy_pos]
                    copy_column -= 1
                    copy_pos -= 1
                # MODIFY RIGHT
                copy_column = column + 1
                copy_pos = pos + 1
                while copy_column <= Game.dimension - 1:
                    table[row][copy_column] = modified_line[copy_pos]
                    copy_pos += 1
                    copy_column += 1
            elif it == 1: #COLOANA
                line = get_column(table, row, column)[0]
                pos = row
                modified_line = modifyLine(line, pos, color)
                # ADD UP
                copy_row = row
                copy_pos = pos
                while copy_row >= 0:
                    table[copy_row][column] = modified_line[copy_pos]
                    copy_row -= 1
                    copy_pos -= 1
                # ADD DOWN
                copy_row = row + 1
                copy_pos = pos + 1
                while copy_row <= Game.dimension - 1:
                    table[copy_row][column] = modified_line[copy_pos]
                    copy_row += 1
                    copy_pos += 1
            elif it == 2:#DIAGONALA PP
                line = get_pp_diagonal(table, row, column)[0]
                pos = get_pp_diagonal(table, row, column)[1] - 1
                # print(line)
                # print(pos)
                modified_line = modifyLine(line, pos, color)
                # print(modified_line)
                # ADD UP
                copy_row = row
                copy_column = column
                copy_pos = pos
                while copy_column >= 0 and copy_row >= 0:
                    table[copy_row][copy_column] = modified_line[copy_pos]
                    copy_column -= 1
                    copy_row -= 1
                    copy_pos -= 1
                # ADD DOWN
                copy_row = row + 1
                copy_column = column + 1
                copy_pos = pos + 1
                while copy_column <= Game.dimension - 1 and copy_row <= Game.dimension - 1:
                    table[copy_row][copy_column] = modified_line[copy_pos]
                    copy_column += 1
                    copy_row += 1
                    copy_pos += 1
            else: #DIAGONALA SEC
                line = get_sec_diagonal(table, row, column)[0]
                pos = get_sec_diagonal(table, row, column)[1] - 1
                # print(line)
                # print(pos)
                modified_line = modifyLine(line, pos, color)
                # print(modified_line)
                # MODIFY UP
                copy_row = row
                copy_column = column
                copy_pos = pos
                while copy_column <= Game.dimension - 1 and copy_row >= 0:
                    table[copy_row][copy_column] = modified_line[copy_pos]
                    copy_column += 1
                    copy_row -= 1
                    copy_pos -= 1
                # AMODIFY DOWN
                copy_row = row + 1
                copy_column = column - 1
                copy_pos = pos + 1
                while copy_column >= 0 and copy_row <= Game.dimension - 1:
                    table[copy_row][copy_column] = modified_line[copy_pos]
                    copy_column -= 1
                    copy_row += 1
                    copy_pos += 1

#FUNCTIE AJUTATOARE CARE VERIFICA DACA UN PARTICIPANT ARE POSIBILITATEA SA PUNA VREO PIESA
def check_can_put(table, color):
    list_possible_moves = get_possible_box(table)
    for (row, column) in list_possible_moves:
        copyTable = copy.deepcopy(table)
        moves = getAllMoves(copyTable, row, column, color)
        if 1 in moves:
            return True
    return False


def main():
    print('Choose the algorithm (1 or 2)')
    print('These are the options: ')
    print('1. MinMax')
    print('2. AlphaBeta')
    while True:
        whichAlgorithm = input()
        if whichAlgorithm in ['1', '2']:
            whichAlgorithm = int(whichAlgorithm)
            break
        else:
            print("Insert data again")

    print('Choose the dificulty (1, 2 or 3): ')
    print('1. Easy')
    print('2. Normal')
    print('3. Hard')
    whichDifficulty = 0
    while True:
        whichDifficulty = input()
        if whichDifficulty in ['1', '2', '3']:
            whichDifficulty = int(whichDifficulty)
            break
        else:
            print("Insert data again")

    if whichDifficulty == 1:
        maxDepth = 2
    elif whichDifficulty == 2:
        maxDepth = 4
    else:
        maxDepth = 6

    print('Choose the color of your pices: b for black and w for white\nBlack will start')
    while True:
        whichColor = input()
        if whichColor in ['b', 'w']:
            break
        else:
            print("Insert data again")
    if whichColor == 'b':
        Game.JMAX = 'w'
        Game.JMIN = 'b'
    else:
        Game.JMAX = 'b'
        Game.JMIN = 'w'

    newGame = Game()
    currState = State(newGame, 'b', maxDepth)

    print("Initial Table")
    print('  ' + 'a ' + 'b ' + 'c ' + 'd ' + 'e ' + 'f ' + 'g ' + 'h ')
    for it in range(8):
        print(str(it), end=" ")
        for it2 in range(8):
            print(currState.table_game.table[it][it2], end=" ")
        print("\n", end="")
    print("\n")

    if newGame.JMIN == 'b':
        print("PLAYER'S TURN")

    pygame.init()
    pygame.display.set_caption('Reversi')
    screen = pygame.display.set_mode(size=[640, 640])
    grid = draw_grid(screen, newGame.table)

    counter_player = 0
    counter_computer = 0
    initial_time_player = int(round(time.time() * 1000))
    initial_time_game = int(round(time.time()) * 1000)
    while True:
        # VERIFICAM DACA AM AJUNS LA FINALUL JOCULUI
        situation = currState.table_game.isFinal()
        if situation != False:
            if situation == currState.table_game.JMIN:
                print("THE WINNER IS PLAYER")
            elif situation == currState.table_game.JMAX:
                print("THE WINNER IS PC")
            else:
                print(situation)
            (nr_JMIN, nr_JMAX) = currState.table_game.calculate_score()
            print("PLAYER HAS " + str(nr_JMIN) + " POINTS")
            print("COMPUTER HAS " + str(nr_JMAX) + " POINTS")
            final_time_game = int(round(time.time()) * 1000)
            print("THE MATCH TOOK " + str(final_time_game - initial_time_game) + " MILLISECONDS")
            print("COPMUTER HAD " + str(counter_computer) + " MOVES")
            print("PLAYER HAD " + str(counter_player) + " MOVES")
            break
        if currState.currPlayer == newGame.JMIN: #E RANDUL PLAYER-ULUI
            if check_can_put(currState.table_game.table, currState.currPlayer) == False: #VERIFICA DACA POATE PUNE PIESE
                print("PLAYER CAN NOT PLACE A PIECE. PASS")
                currState.currPlayer = getOtherColor(currState.currPlayer)
                break
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("PLAYER QUITED")
                        (nr_JMIN, nr_JMAX) = currState.table_game.calculate_score()
                        print("PLAYER HAS " + str(nr_JMIN) + " POINTS")
                        print("COMPUTER HAS " + str(nr_JMAX) + " POINTS")
                        if nr_JMAX > nr_JMIN:
                            print("PC WON")
                        elif nr_JMIN > nr_JMAX:
                            print("PLAYER WON")
                        else:
                            print("DRAW")
                        final_time_game = int(round(time.time()) * 1000)
                        print("THE MATCH TOOK " + str(final_time_game - initial_time_game) + " MILLISECONDS")
                        print("COMPUTER HAD " + str(counter_computer) + " MOVES")
                        print("PLAYER HAD " + str(counter_player) + " MOVES")
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for i in range(len(grid)):
                            for j in range(len(grid[i])):
                                if grid[i][j].collidepoint(pos):
                                    if currState.table_game.table[i][j] == Game.Empty:
                                        # print("DA_APAS")
                                        # print(i)
                                        # print(j)
                                        row = i
                                        column = j
                                        moves = getAllMoves(currState.table_game.table, row, column,currState.currPlayer)
                                        if 1 in moves:
                                            counter_player += 1
                                            # print("mutare valida")
                                            modifyTable(currState.table_game.table, moves, row, column,currState.currPlayer)
                                            # SCHIMB JUCATORUL
                                            currState.currPlayer = getOtherColor(currState.currPlayer)
                                            final_time_player = int(round(time.time() * 1000))
                                            print("Player's thinking time " + str(
                                                final_time_player - initial_time_player) + " Milliseconds.")
                                            print("The table after player's move")
                                            print('  ' + 'a ' + 'b ' + 'c ' + 'd ' + 'e ' + 'f ' + 'g ' + 'h ')
                                            for it in range(8):
                                                print(str(it), end=" ")
                                                for it2 in range(8):
                                                    print(currState.table_game.table[it][it2], end=" ")
                                                print("\n", end="")
                                            print("\n")
                                        else:
                                            print("INVALID MOVE. RETRY!")
        else:
            if currState.currPlayer == newGame.JMAX: #E RANDUL CALCULATORULUI
                print("COMPUTER'S TURN")
                if check_can_put(currState.table_game.table, currState.currPlayer) == False: #VERIFICA DACA POATE SA PUNA PIESE
                    print("COMPUTER CAN NOT PLACE A PIECE. PASS")
                    currState.currPlayer = getOtherColor(currState.currPlayer)
                    break
                else:
                    counter_computer += 1
                    initial_time_computer = int(round(time.time() * 1000))
                    if whichAlgorithm == 1:
                        state_opponent = min_max_algorithm(currState)
                    else:
                        state_opponent = alpha_beta_algorithm(-500, 500, currState)
                    currState.table_game.table = state_opponent.optimal_move.table_game.table
                    currState.currPlayer = getOtherColor(currState.currPlayer)
                    final_time_computer = int(round(time.time() * 1000))
                    print("Computer's thinking time " + str(
                        final_time_computer - initial_time_computer) + " Milliseconds.")
                    initial_time_player = int(round(time.time() * 1000))
                print("The table after computer's move")
                print('  ' + 'a ' + 'b ' + 'c ' + 'd ' + 'e ' + 'f ' + 'g ' + 'h ')
                for it in range(8):
                    print(str(it), end=" ")
                    for it2 in range(8):
                        print(currState.table_game.table[it][it2], end=" ")
                    print("\n", end="")
                print("\n")
                print("PLAYER'S TURN")
        grid = draw_grid(screen, currState.table_game.table)
        pygame.display.update()


'''if __name__ == '__main__':
    main()'''
