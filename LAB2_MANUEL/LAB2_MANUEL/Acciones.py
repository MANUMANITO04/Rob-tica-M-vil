import Sensores
import math
import time
import paho.mqtt.client as mqtt

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

def on_connect(client, userdata, flags, rc):
    print("Conectado con código: " + str(rc))
    client.subscribe("sensor/rpma")
    client.subscribe("sensor/rpmb")

def on_message(client, userdata, msg):
    global RPM_izq, RPM_der
    try:
        if msg.topic == "sensor/rpma":
            RPM_izq = float(msg.payload.decode())
        elif msg.topic == "sensor/rpmb":
            RPM_der = float(msg.payload.decode())
        elif msg.topic == "sensor/ultra":
            Distance = float(msg.payload.decode())
    except ValueError:
        print(f"Error al convertir mensaje en {msg.topic}: {msg.payload}")

#===========CONFIGURACIÓN DEL CLIENTE MQTT============
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_message = on_message
client.connect("10.42.0.1", 1883, 60)

client.loop_start()

# === Variables de posición ===
x = 0.0
y = 0.0
theta = 0.0  # Orientación en radianes

#----------------DIMENSIONES DEL CARRO----------------
h=114 #Distancia de las ruedas mm
R=9.5 #Radio de la llanta mm 

def motores(VT, W):
    VR_MAX=50
    VL_MAX=50
    VR = VT+(W*h/2) #velocidad lineal del motor derecho mm/s
    VL = VT-(W*h/2) #velocidad lineal del motor izquierdo mm/s
    PWM_R=VR*255/VR_MAX
    PWM_L=VL*255/VL_MAX
    client.publish("motor/pwma", PWM_R)
    client.publish("motor/pwmb", PWM_L)
    

def compor1():
    print("PARAR")
    #run(0)
    motores(0,0)

def compor2():
    print("AVANZAR")
    #run(15)
    motores(20,0)

def compor3():
    print("GIRAR")
    #run_angle(15, 6)
    motores(8,5)

def pizarraComportamiento(tarea):
    if tarea == 1:
        compor1()
    elif tarea == 2:
        compor2()
    elif tarea == 3:
        compor3()