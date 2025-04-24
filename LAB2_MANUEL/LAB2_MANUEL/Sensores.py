import time
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

pizarra = [0, 0, 0, 0]

def s1():
    if globales.start_time == 0:
            pizarra[0] = 0
    pizarra[0]= time.time() - globales.start_time

def s2():
    sensor2 = int(input(Distance))
    print()
    pizarra[1] = sensor2
def s3():
    sensor3 = int(input(RPM_der))
    print()
    pizarra[2] = sensor3
def s4():
    sensor4 = int(input(RPM_izq))
    print()
    pizarra[3] = sensor4
def getPizarraSen(x):
    return pizarra[x - 1]
def pizarrasensorre():
    s1()
    #s2()
    s3()
    s4()