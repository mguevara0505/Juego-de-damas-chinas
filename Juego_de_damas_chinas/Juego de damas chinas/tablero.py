import pygame
from constantes import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from piezas import Pieza

class Tablero:
    def __init__(self):
        self.tablero = []
        self.rojo_izquierda = self.blanco_izquierda = 12
        self.reyes_rojos = self.reyes_blancos = 0
        self.crear_tablero()
    
    def dibujar_cuadrados(self, win):
        win.fill(BLACK)
        for fila in range(ROWS):
            for col in range(fila % 2, COLS, 2):
                pygame.draw.rect(win, RED, (fila*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def mover(self, pieza, fila, col):
        self.tablero[pieza.fila][pieza.col], self.tablero[fila][col] = self.tablero[fila][col], self.tablero[pieza.fila][pieza.col]
        pieza.mover(fila, col)

        if fila == ROWS - 1 or fila == 0:
            pieza.crear_rey()
            if pieza.color == WHITE:
                self.reyes_blancos += 1
            else:
                self.reyes_rojos += 1
    
    def obtener_pieza(self, fila, col):
        return self.tablero[fila][col]


    def crear_tablero(self):
        for fila in range(ROWS):
            self.tablero.append([])
            for col in range(COLS):
                if col % 2 == ((fila + 1) % 2):
                    if fila < 3:
                        self.tablero[fila].append(Pieza(fila, col, WHITE))
                    elif fila > 4:
                        self.tablero[fila].append(Pieza(fila, col, RED))
                    else:
                        self.tablero[fila].append(0)
                else:
                    self.tablero[fila].append(0)
    
    def dibujar(self, win):
        self.dibujar_cuadrados(win)
        for fila in range(ROWS):
            for col in range(COLS):
                pieza = self.tablero[fila][col]
                if pieza != 0:
                    pieza.dibujar(win)
    
    def remover(self, piezas):
        for pieza in piezas:
            self.tablero[pieza.fila][pieza.col] = 0
            if pieza != 0:
                if pieza.color == RED:
                    self.rojo_izquierda -= 1
                else:
                    self.blanco_izquierda -= 1
    
    def ganador(self):
        if self.rojo_izquierda <= 0:
            return WHITE
        elif self.blanco_izquierda <= 0:
            return RED
        
        return None
    
    def obtener_movimientos_validos(self, pieza):
        movimientos = {}
        izquierda = pieza.col - 1
        derecha = pieza.col + 1
        fila = pieza.fila

        if pieza.color == RED or pieza.rey:
            movimientos.update(self._atravesar_izquierda(fila - 1, max(fila-3, -1), -1, pieza.color, izquierda))
            movimientos.update(self._atravesar_derecha(fila - 1, max(fila-3, -1), -1, pieza.color, derecha))

        if pieza.color == WHITE or pieza.rey:
            movimientos.update(self._atravesar_izquierda(fila + 1, min(fila+3, ROWS), 1, pieza.color, izquierda))
            movimientos.update(self._atravesar_derecha(fila + 1, min(fila+3, ROWS), 1, pieza.color, derecha))
    
        return movimientos

    def _atravesar_izquierda(self, inicio, detener, saltar, color, izquierda, saltado=[]):
        movimientos = {}
        ultimo = []
        for r in range(inicio, detener, saltar):
            if izquierda < 0:
                break

            actual = self.tablero[r][izquierda]
            if actual == 0:
                if saltado and not ultimo:
                    break
                elif saltado:
                    movimientos[(r, izquierda)] = ultimo + saltado
                else:
                    movimientos[(r, izquierda)] = ultimo
                
                if ultimo:
                    if saltar == -1:
                        fila = max(r-3, 0)
                    else:
                        fila = min(r+3, ROWS)
                    movimientos.update(self._atravesar_izquierda(r+saltar, fila, saltar, color, izquierda-1, saltado=ultimo))
                    movimientos.update(self._atravesar_derecha(r+saltar, fila, saltar, color, izquierda+1, saltado=ultimo))
                break
            elif actual.color == color:
                break
            else:
                ultimo = [actual]

            izquierda -= 1
        
        return movimientos

    def _atravesar_derecha(self, inicio, detener, saltar, color, derecha, saltado=[]):
        movimientos = {}
        ultimo = []
        for r in range(inicio, detener, saltar):
            if derecha >= COLS:
                break

            actual = self.tablero[r][derecha]
            if actual == 0:
                if saltado and not ultimo:
                    break
                elif saltado:
                    movimientos[(r, derecha)] = ultimo + saltado
                else:
                    movimientos[(r, derecha)] = ultimo
                
                if ultimo:
                    if saltar == -1:
                        fila = max(r-3, 0)
                    else:
                        fila = min(r+3, ROWS)

                    movimientos.update(self._atravesar_izquierda(r+saltar, fila, saltar, color, derecha-1, saltado=ultimo))
                    movimientos.update(self._atravesar_derecha(r+saltar, fila, saltar, color, derecha+1, saltado=ultimo))
                break
            elif actual.color == color:
                break
            else:
                ultimo = [actual]

            derecha += 1
        
        return movimientos