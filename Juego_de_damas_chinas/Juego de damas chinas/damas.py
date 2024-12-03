import pygame
from constantes import WIDTH, HEIGHT, SQUARE_SIZE, RED
from juego import Juego

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Damas chinas')

def obtener_filas_col_desde_mouse(pos):
    x, y = pos
    fila = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return fila, col

def mostrar_ventana_inicio():
    # Colores
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    
    # Crear la ventana de inicio
    ventana_inicio = True
    fuente = pygame.font.SysFont(None, 20)
    texto = fuente.render("Bienvenido al juego de Damas Chinas. Avanza las fichas de forma diagonal y cómete todas las del enemigo", True, NEGRO)
    boton_aceptar = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50)
    
    while ventana_inicio:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_aceptar.collidepoint(event.pos):
                    ventana_inicio = False
        
        WIN.fill(BLANCO)
        WIN.blit(texto, (WIDTH//2 - texto.get_width()//2, HEIGHT//2 - 100))
        pygame.draw.rect(WIN, NEGRO, boton_aceptar)
        fuente_boton = pygame.font.SysFont(None, 45)
        texto_boton = fuente_boton.render("Aceptar", True, BLANCO)
        WIN.blit(texto_boton, (boton_aceptar.x + (boton_aceptar.width - texto_boton.get_width()) // 2, boton_aceptar.y + (boton_aceptar.height - texto_boton.get_height()) // 2))
        pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    juego = Juego(WIN)

    mostrar_ventana_inicio()  # Mostrar ventana de inicio antes del juego

    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                fila, col = obtener_filas_col_desde_mouse(pos)
                juego.seleccionar(fila, col)
        juego.actualizar()
    
    pygame.quit()

main()
