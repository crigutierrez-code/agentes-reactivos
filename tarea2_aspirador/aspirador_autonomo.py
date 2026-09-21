import pygame
import random

# Configuración de la pantalla
ANCHO, ALTO = 400, 400
TAMANIO_CELDA = 40
FILAS = ANCHO // TAMANIO_CELDA
COLUMNAS = ALTO // TAMANIO_CELDA

# Colores
COLOR_FONDO = (30, 30, 30)
COLOR_SUCIO = (139, 69, 19)  # Marrón
COLOR_LIMPIO = (255, 255, 255)  # Blanco
COLOR_ASPIRADOR = (0, 255, 0)  # Verde

# MEJORA (profe): múltiples aspiradores para simular trabajo colaborativo
NUMERO_ASPIRADORES = 3
COLORES_ASPIRADORES = [COLOR_ASPIRADOR, (0, 128, 255), (255, 255, 0)]

# MEJORA (profe): estadísticas de eficiencia
movimientos = 0
celdas_limpiadas = 0
tiempo_inicio = 0

# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Aspirador Autónomo")

# Generar el entorno con suciedad aleatoria (1 = sucio, 0 = limpio)
entorno = [[random.choice([0, 1]) for _ in range(COLUMNAS)] for _ in range(FILAS)]

# Posición inicial de los aspiradores
aspiradores = []
for i in range(NUMERO_ASPIRADORES):
    aspiradores.append({
        "x": random.randint(0, FILAS - 1),
        "y": random.randint(0, COLUMNAS - 1),
        "color": COLORES_ASPIRADORES[i % len(COLORES_ASPIRADORES)],
    })


# Función para mover el aspirador a una celda vecina aleatoria
def mover_aspirador(x, y, indice):
    movimientos_posibles = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(movimientos_posibles)  # Aleatorizar movimientos
    for dx, dy in movimientos_posibles:
        nuevo_x, nuevo_y = x + dx, y + dy
        if 0 <= nuevo_x < FILAS and 0 <= nuevo_y < COLUMNAS:
            if not celda_ocupada(nuevo_x, nuevo_y, indice):
                return nuevo_x, nuevo_y
    return x, y  # Si no puede moverse, se queda en el mismo lugar


# Comprueba si una celda ya está ocupada por otro aspirador
def celda_ocupada(x, y, indice):
    for i, aspirador in enumerate(aspiradores):
        if i != indice and aspirador["x"] == x and aspirador["y"] == y:
            return True
    return False


# MEJORA (profe): optimización del movimiento: buscar celdas sucias
# cercanas antes de moverse aleatoriamente.
def mover_inteligente(x, y, indice):
    vecinos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(vecinos)
    # Primero: si hay una celda vecina sucia, ir hacia ella
    for dx, dy in vecinos:
        nuevo_x, nuevo_y = x + dx, y + dy
        if 0 <= nuevo_x < FILAS and 0 <= nuevo_y < COLUMNAS:
            if entorno[nuevo_x][nuevo_y] == 1 and not celda_ocupada(nuevo_x, nuevo_y, indice):
                return nuevo_x, nuevo_y
    # Segundo: si no hay suciedad cerca, moverse a una celda vecina aleatoria
    return mover_aspirador(x, y, indice)


# Verifica si el entorno está completamente limpio
def entorno_limpio():
    for fila in entorno:
        if 1 in fila:
            return False
    return True


# Bucle principal
ejecutando = True
tiempo_inicio = pygame.time.get_ticks()
while ejecutando:
    pygame.time.delay(500)  # Pausa para visualizar mejor el movimiento

    # Verificar eventos (cierre de ventana)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Reglas del aspirador: si la casilla está sucia la limpia; si está
    # limpia, se mueve (ahora buscando suciedad cercana).
    for i, aspirador in enumerate(aspiradores):
        if entorno[aspirador["x"]][aspirador["y"]] == 1:
            entorno[aspirador["x"]][aspirador["y"]] = 0  # Limpiar la casilla
            celdas_limpiadas += 1
            # MEJORA (profe): registrar estadísticas de limpieza
            print("Celda limpiada {} | movimientos {} | tiempo {:.1f}s".format(
                celdas_limpiadas, movimientos, (pygame.time.get_ticks() - tiempo_inicio) / 1000))
        else:
            # Si la casilla ya está limpia, moverse a otra casilla
            nuevo_x, nuevo_y = mover_inteligente(aspirador["x"], aspirador["y"], i)
            if (nuevo_x, nuevo_y) != (aspirador["x"], aspirador["y"]):
                movimientos += 1  # MEJORA (profe): registrar movimientos
            aspirador["x"], aspirador["y"] = nuevo_x, nuevo_y

    # Dibujar el entorno
    pantalla.fill(COLOR_FONDO)
    for i in range(FILAS):
        for j in range(COLUMNAS):
            color = COLOR_SUCIO if entorno[i][j] == 1 else COLOR_LIMPIO
            pygame.draw.rect(pantalla, color, (j * TAMANIO_CELDA, i * TAMANIO_CELDA, TAMANIO_CELDA, TAMANIO_CELDA))

    # Dibujar los aspiradores
    for aspirador in aspiradores:
        pygame.draw.rect(pantalla, aspirador["color"], (aspirador["y"] * TAMANIO_CELDA, aspirador["x"] * TAMANIO_CELDA, TAMANIO_CELDA, TAMANIO_CELDA))

    # MEJORA (profe): mostrar el progreso de limpieza con una barra visual
    segundos = (pygame.time.get_ticks() - tiempo_inicio) / 1000
    sucias = sum(fila.count(1) for fila in entorno)
    total_celdas = FILAS * COLUMNAS
    limpias = total_celdas - sucias
    barra_x, barra_y, barra_ancho, barra_alto = 5, 5, 200, 12
    pygame.draw.rect(pantalla, (0, 0, 0), (barra_x, barra_y, barra_ancho, barra_alto))
    pygame.draw.rect(pantalla, (0, 180, 0),
                     (barra_x, barra_y, int(barra_ancho * limpias / total_celdas), barra_alto))
    pygame.display.update()

    # MEJORA (profe): terminar cuando el entorno esté limpio y registrar el tiempo
    if entorno_limpio():
        segundos = (pygame.time.get_ticks() - tiempo_inicio) / 1000
        print("Entorno limpio en {:.1f} segundos con {} movimientos y {} celdas limpiadas.".format(
            segundos, movimientos, celdas_limpiadas))
        pygame.time.delay(3000)
        ejecutando = False

# Cerrar Pygame
pygame.quit()