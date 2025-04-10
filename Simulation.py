import pygame
import math

# Inicializar Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Robot")
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
ROBOT_COLOR = (0, 100, 255)
OBSTACLE_COLOR = (255, 0, 0)
BLACK = (0, 0, 0)

# Parámetros del robot
robot_pos = [425, 200]
robot_angle = 0
robot_radius = 10
speed = 2
turn_speed = 2

# Obstáculo
obstacle = pygame.Rect(400, 280, 50, 50)

# Estado del sistema
board = [0, 0, 0]

# Objetivos
target_angle = -120
target_distance = 100

def s1():
    return int(math.sqrt((robot_pos[0] - start_pos[0])**2 + (robot_pos[1] - start_pos[1])**2))

def s2():
    return int(robot_angle)

def s3():
    dx = math.cos(math.radians(robot_angle)) * robot_radius
    dy = math.sin(math.radians(robot_angle)) * robot_radius
    front_point = (robot_pos[0] + dx, robot_pos[1] + dy)
    return 1 if obstacle.collidepoint(front_point) else 0

def boardSens():
    board[0] = s1()
    board[1] = s2()
    board[2] = s3()

def getboardSens(x):
    return board[x - 1]

def C1():
    print("ACCION: Parado")

def C2():
    print("ACCION: Avanza")
    dx = math.cos(math.radians(robot_angle)) * speed
    dy = math.sin(math.radians(robot_angle)) * speed
    robot_pos[0] += dx
    robot_pos[1] += dy

def C3():
    print("ACCION: Giro Derecha")
    global robot_angle
    robot_angle = (robot_angle - turn_speed) % 360

def C4():
    print("ACCION: Giro Izquierda")
    global robot_angle
    robot_angle = (robot_angle + turn_speed) % 360

def C5():
    print("ACCION: Set valores de Saux y S1")

def draw_robot():
    pygame.draw.circle(screen, ROBOT_COLOR, (int(robot_pos[0]), int(robot_pos[1])), robot_radius)
    dx = math.cos(math.radians(robot_angle)) * 20
    dy = math.sin(math.radians(robot_angle)) * 20
    pygame.draw.line(screen, BLACK, robot_pos, (robot_pos[0] + dx, robot_pos[1] + dy), 2)

# Bucle principal
main_loop = True

while main_loop:
    # Reset de estado al inicio de cada ciclo
    start_pos = robot_pos.copy()
    saux = (robot_angle + target_angle) % 360
    internal_loop = True

    while internal_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_loop = False

        screen.fill(WHITE)
        pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle)
        draw_robot()
        boardSens()

        # Comportamiento según sensores
        if getboardSens(3) == 1:  # Obstáculo detectado
            C1()
            C4()
            internal_loop = False  # <-- Se rompe el bucle para reiniciar desde nueva orientación
        else:
            if getboardSens(2) == saux:
                if getboardSens(1) >= target_distance:
                    C1()
                    C5()
                    internal_loop = False  # <-- Se rompe el bucle y vuelve a empezar
                else:
                    C2()
            else:
                if (saux - getboardSens(2)) % 360 > 180:
                    C3()
                else:
                    C4()

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
