import Sensores
import math
# === Variables de posición ===
x = 0.0
y = 0.0
theta = 0.0  # Orientación en radianes
#----------------DIMENSIONES DEL CARRO----------------
h=114 #Distancia de las ruedas mm
R=9.5 #Radio de la llanta mm  
dt=0.1
position = [0, 0, 0]
def pos(RPM_R, RPM_L):
    global x, y, theta
    VR_encoder=RPM_R * (2 * math.pi * R) / 60
    VL_encoder=RPM_L * (2 * math.pi * R) / 60

    VT_encoder = (VR_encoder + VL_encoder) / 2
    omega_encoder = (VR_encoder - VL_encoder) / h

    # Actualizar posición y orientación
    x = x + VT_encoder * math.cos(theta) * dt
    y = y + VT_encoder * math.sin(theta) * dt
    theta = theta + omega_encoder * dt
    position[0]=x
    position[1]=y
    position[2]=theta
    print(f"[POS] x={x:.3f} m, y={y:.3f} m, θ={math.degrees(theta):.2f}°")

def getPos(x):
    return position[x - 1]