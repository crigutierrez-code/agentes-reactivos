import pygame
import random

# Configuración de la pantalla
ANCHO, ALTO = 500, 500
COLOR_FONDO = (30, 30, 30)

# Configuración del agente
TAMANIO_AGENTE = 20
COLOR_AGENTE = (0, 255, 0)
VELOCIDAD_AGENTE = 2

# MEJORA (profe): múltiples agentes para observar su interacción
NUMERO_AGENTES = 3
COLORES_AGENTES = [COLOR_AGENTE, (0, 128, 255), (255, 255, 0)]

# MEJORA (profe): optimizar el cambio de dirección usando heurísticas
# en lugar de elección aleatoria (tecla H para alternar el modo)
MODO_HEURISTICA = True
PASOS_SENSOR = 8  # pasos que "ve" el agente hacia adelante

# Configuración de los obstáculos
COLOR_OBSTACULO = (255, 0, 0)
NUMERO_OBSTACULOS = 5
TAMANIO_OBSTACULO = 40

# Inicialización de Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Agente Reactivo")

print("Controles: flechas = mover el agente verde (manual) | M = manual SI/NO | H = heuristica SI/NO")

# Posición inicial del agente
agente_x = random.randint(0, ANCHO - TAMANIO_AGENTE)
agente_y = random.randint(0, ALTO - TAMANIO_AGENTE)
direccion = random.choice(["ARRIBA", "ABAJO", "IZQUIERDA", "DERECHA"])

# Generar obstáculos en posiciones aleatorias
obstaculos = []
for _ in range(NUMERO_OBSTACULOS):
    obs_x = random.randint(0, ANCHO - TAMANIO_OBSTACULO)
    obs_y = random.randint(0, ALTO - TAMANIO_OBSTACULO)
    obstaculos.append(pygame.Rect(obs_x, obs_y, TAMANIO_OBSTACULO, TAMANIO_OBSTACULO))

# MEJORA (profe): múltiples agentes. El primero (verde) se puede
# controlar manualmente con las flechas para compararlo con los reactivos.
agentes = []
for i in range(NUMERO_AGENTES):
    agentes.append({
        "x": random.randint(0, ANCHO - TAMANIO_AGENTE),
        "y": random.randint(0, ALTO - TAMANIO_AGENTE),
        "direccion": random.choice(["ARRIBA", "ABAJO", "IZQUIERDA", "DERECHA"]),
        "color": COLORES_AGENTES[i % len(COLORES_AGENTES)],
        "manual": i == 0,
    })

# MEJORA (profe): control manual del primer agente (tecla M para activar/desactivar)
control_manual = True


# Función para mover el agente
def mover_agente(x, y, direccion):
    if direccion == "ARRIBA":
        y -= VELOCIDAD_AGENTE
    elif direccion == "ABAJO":
        y += VELOCIDAD_AGENTE
    elif direccion == "IZQUIERDA":
        x -= VELOCIDAD_AGENTE
    elif direccion == "DERECHA":
        x += VELOCIDAD_AGENTE
    return x, y


# Función para verificar colisión (bordes, obstáculos y otros agentes)
def verificar_colision(x, y, indice_agente=None):
    rectangulo_agente = pygame.Rect(x, y, TAMANIO_AGENTE, TAMANIO_AGENTE)
    if x < 0 or x > ANCHO - TAMANIO_AGENTE or y < 0 or y > ALTO - TAMANIO_AGENTE:
        return True  # Colisión con los bordes
    for obs in obstaculos:
        if rectangulo_agente.colliderect(obs):
            return True  # Colisión con un obstáculo
    # MEJORA (profe): interacción entre agentes (se evitan entre sí)
    for i, agente in enumerate(agentes):
        if i != indice_agente:
            rect_otro = pygame.Rect(agente["x"], agente["y"], TAMANIO_AGENTE, TAMANIO_AGENTE)
            if rectangulo_agente.colliderect(rect_otro):
                return True  # Colisión con otro agente
    return False


# MEJORA (profe): espacio libre en una dirección (sensor sencillo hacia adelante)
def espacio_libre(x, y, direccion):
    pasos = 0
    while pasos < PASOS_SENSOR:
        x, y = mover_agente(x, y, direccion)
        if verificar_colision(x, y):
            break
        pasos += 1
    return pasos


# MEJORA (profe): nueva dirección con heurística: elige la dirección con
# más espacio libre en lugar de una elección totalmente aleatoria.
def nueva_direccion(indice_agente):
    x = agentes[indice_agente]["x"]
    y = agentes[indice_agente]["y"]
    direcciones = ["ARRIBA", "ABAJO", "IZQUIERDA", "DERECHA"]
    random.shuffle(direcciones)

    if MODO_HEURISTICA:
        mejor_direccion = agentes[indice_agente]["direccion"]
        mejor_espacio = -1
        for d in direcciones:
            nx, ny = mover_agente(x, y, d)
            if not verificar_colision(nx, ny, indice_agente):
                espacio = espacio_libre(x, y, d)
                if espacio > mejor_espacio:
                    mejor_espacio = espacio
                    mejor_direccion = d
        return mejor_direccion
    else:
        # Comportamiento original: cambio de dirección aleatorio
        return random.choice(direcciones)


# Bucle principal
ejecutando = True
while ejecutando:
    pygame.time.delay(20)

    # Verificar eventos (cierre de ventana y teclas del control manual)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            # MEJORA (profe): control manual con las flechas del teclado
            if evento.key == pygame.K_UP:
                agentes[0]["direccion"] = "ARRIBA"
            elif evento.key == pygame.K_DOWN:
                agentes[0]["direccion"] = "ABAJO"
            elif evento.key == pygame.K_LEFT:
                agentes[0]["direccion"] = "IZQUIERDA"
            elif evento.key == pygame.K_RIGHT:
                agentes[0]["direccion"] = "DERECHA"
            elif evento.key == pygame.K_m:
                control_manual = not control_manual
                print("Modo manual: " + ("SI" if control_manual else "NO"))
            elif evento.key == pygame.K_h:
                MODO_HEURISTICA = not MODO_HEURISTICA
                print("Heuristica: " + ("SI" if MODO_HEURISTICA else "NO"))

    # Mover los agentes
    for i, agente in enumerate(agentes):
        if agente["manual"] and control_manual:
            # Modo manual: avanza solo si no hay colisión; el jugador decide el giro
            nuevo_x, nuevo_y = mover_agente(agente["x"], agente["y"], agente["direccion"])
            if not verificar_colision(nuevo_x, nuevo_y, i):
                agente["x"], agente["y"] = nuevo_x, nuevo_y
        else:
            # Modo reactivo: si hay colisión, cambiar dirección
            nuevo_x, nuevo_y = mover_agente(agente["x"], agente["y"], agente["direccion"])
            if verificar_colision(nuevo_x, nuevo_y, i):
                agente["direccion"] = nueva_direccion(i)
            else:
                agente["x"], agente["y"] = nuevo_x, nuevo_y

    # Dibujar el entorno
    pantalla.fill(COLOR_FONDO)
    for agente in agentes:
        pygame.draw.rect(pantalla, agente["color"], (agente["x"], agente["y"], TAMANIO_AGENTE, TAMANIO_AGENTE))
    for obs in obstaculos:
        pygame.draw.rect(pantalla, COLOR_OBSTACULO, obs)

    pygame.display.update()

# Cerrar Pygame
pygame.quit()