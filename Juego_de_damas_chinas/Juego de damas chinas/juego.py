import pygame
from tablero import Tablero
from constantes import RED, WHITE, SQUARE_SIZE, BLUE
from random import choice

pygame.font.init()
class Juego:
    def __init__(self, win):
        self._init()
        self.win = win
    
    def mostrar_mensaje(self, mensaje):
        WIN = pygame.display.set_mode((800, 800))
        font = pygame.font.Font(None, 36)

        # Dividir el mensaje en líneas por el carácter '\n'
        lineas = mensaje.split('\n')

        # Renderizar cada línea en una superficie separada
        y = 10  # Posición inicial en el eje y
        for linea in lineas:
            text = font.render(linea, True, (255, 0, 0))
            WIN.blit(text, (10, y))
            y += text.get_height()  

        pygame.display.flip()
        pygame.time.wait(5000)
        
    def obtener_mensaje_teoria_conteo(self): 
        mensajes = [ 
        "¿Sabías que la combinación de 5 \n objetos tomados de 2 en 2 se calcula como 5C2?",
        "La permutación de 4 objetos es 4! = 24.", 
        "Para contar subconjuntos de un conjunto de 3 elementos, \n usamos 2^3 = 8 subconjuntos.",
        "¿Sabías que el factorial de un número representa \n todas las formas de ordenar ese número de elementos?",
        "La combinación es como elegir un equipo de fútbol, \n mientras que la permutación es como ordenar a \n los jugadores en el campo.",
        "¿Cuántas contraseñas de 8 caracteres \n puedes crear usando solo letras minúsculas? \n¡Son 26^8 posibilidades! \nAsí de importante es la teoría del conteo \n para la seguridad informática.",
        "Una combinación es un subconjunto de \n elementos donde el orden no importa. \n El número de combinaciones de n elementos tomados \n de k en k se denota \n por C(n,k) o nCk.",
        " El número de caminos más cortos de la esquina \n inferior izquierda a la esquina superior \n derecha de una cuadrícula \n de m x n es C(m+n, m).",
        " Si n+1 objetos se colocan en n cajas,\n entonces al menos una caja contendrá al menos dos objetos.",
        "¿De cuántas formas se pueden ordenar n \n genes en un cromosoma? \n La respuesta es n!.",
        "La teoría del conteo estudia las \n diferentes formas de organizar y seleccionar elementos \n de un conjunto, utilizando conceptos como \n permutaciones, \n combinaciones y variaciones, y \n aplicando principios como el \n multiplicativo y el aditivo.",
        "Si tienes 3 camisetas, 2 pantalones y 2 pares de zapatos, \n ¿cuántas combinaciones diferentes de ropa puedes hacer? \n Pista (Principio multiplicativo)",
        " En una heladería hay 10 sabores diferentes. \n ¿Cuántas combinaciones de 2 sabores puedes elegir? \nPista (Combinaciones)",
        "¿De cuántas formas puedes ordenar 5 \n libros diferentes en un estante? \n Pista (Permutaciones)",
        ] 
        return choice(mensajes)
    
    def actualizar(self):
        self.tablero.dibujar(self.win)
        self.dibujar_movimientos_validos(self.movimientos_validos)
        pygame.display.update()
    
    def _init(self):
        self.seleccionado = None
        self.tablero = Tablero()
        self.turno = RED
        self.movimientos_validos = {}
    
    def ganador(self):
        return self.tablero.ganador
    
    def reiniciar(self):
        self._init()

    def seleccionar(self, fila, col):
        if self.seleccionado:
            resultado = self._mover(fila, col)
            if not resultado:
                self.seleccionado = None
                self.seleccionar(fila, col)

        pieza = self.tablero.obtener_pieza(fila, col)
        if pieza != 0 and pieza.color == self.turno:
            self.seleccionado = pieza
            self.movimientos_validos = self.tablero.obtener_movimientos_validos(pieza)
            return True

        return False

    
    def _mover(self, fila, col):
        pieza = self.tablero.obtener_pieza(fila, col)
        if self.seleccionado and pieza == 0 and (fila, col) in self.movimientos_validos:
            self.tablero.mover(self.seleccionado, fila, col)
            saltado = self.movimientos_validos[(fila, col)]
            if saltado:
                self.tablero.remover(saltado)
                mensaje = self.obtener_mensaje_teoria_conteo()
                self.mostrar_mensaje(mensaje)
            self.cambiar_turno()
        else:
            return False
        
        return True
    
    def dibujar_movimientos_validos(self, movimientos):
        for movimiento in movimientos:
            fila, col = movimiento
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, fila * SQUARE_SIZE + SQUARE_SIZE//2), 15)
    
    def cambiar_turno(self):
        self.movimientos_validos = {}
        if self.turno == RED:
            self.turno = WHITE
        else:
            self.turno = RED