# Práctica: Agentes Reactivos

Repositorio para la práctica universitaria de **Agentes Reactivos**. Implementa dos agentes reactivos simulados con Pygame, tal como se describen en el documento de la práctica (Tareas 1 y 2). La Tarea 3 (agente aspirador en NetLogo) no está incluida en este repositorio.

## Estructura del repositorio

| Carpeta | Descripción |
|---|---|
| `tarea1_agente_reactivo/` | Agente reactivo que se desplaza en un entorno virtual de 500x500 píxeles, evitando obstáculos. El agente (cuadrado verde) se mueve en una dirección hasta chocar con un obstáculo (rectángulo rojo) o con el borde de la pantalla, y entonces cambia de dirección de manera aleatoria. Sin memoria ni planeación: solo reacciona a la percepción actual. |
| `tarea2_aspirador/` | Agente aspirador autónomo (modelo de Russell y Norvig) sobre una cuadrícula de 10x10 celdas. Si la celda actual está sucia la limpia; si está limpia se mueve aleatoriamente a una celda vecina. Las celdas sucias se dibujan en marrón y las limpias en blanco. |

## Requisitos

- Python 3.7+
- Pygame

## Instalación

```bash
pip install -r requirements.txt
```

O directamente:

```bash
pip install pygame
```

## Cómo ejecutar

Tarea 1 — Agente reactivo que evita obstáculos:

```bash
python tarea1_agente_reactivo/agente_reactivo.py
```

Tarea 2 — Agente aspirador autónomo:

```bash
python tarea2_aspirador/aspirador_autonomo.py
```

Para salir de cualquier simulación, cierra la ventana de Pygame.