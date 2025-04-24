import time
import Sensores
import Acciones
import posicion
import globales
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


tareaT = False
tiempo = 10
dt=0.1

tareaT = False

if globales.start_time == 0:
    globales.start_time = time.time()

tiempo = 20
while not tareaT:
    Sensores.pizarrasensorre()
    posicion.pos(Sensores.getPizarraSen(3),Sensores.getPizarraSen(4))
    if Sensores.getPizarraSen(1) >= tiempo:
        Acciones.pizarraComportamiento(1)
        tareaT = True
    elif posicion.getPos(3) < 45:
        Acciones.pizarraComportamiento(3)   
    else:
        Acciones.pizarraComportamiento(2)
    time.sleep(dt)


print("FIN")