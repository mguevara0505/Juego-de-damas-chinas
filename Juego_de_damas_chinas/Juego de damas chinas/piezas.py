from constantes import RED, WHITE, GREY, SQUARE_SIZE, CROWN
import pygame

class Pieza:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, fila, col, color):
        self.fila = fila
        self.col = col
        self.color = color
        self.rey = False 
        self.x = 0
        self.y = 0
        self.calcular_posicion()
    
    def calcular_posicion(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.fila + SQUARE_SIZE // 2

    def crear_rey(self):
        self.rey = True
    
    def dibujar(self, win):
        radio = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radio + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radio)
        if self.rey:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))
    
    def mover(self, fila, col):
        self.fila = fila
        self.col = col
        self.calcular_posicion()

    def __repr__(self):
        return str(self.color)
        