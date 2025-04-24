#include <Wire.h>
#include "MPU6050_6Axis_MotionApps20.h" //recomendación usar magnetómetro
#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>

//Para la comunicación remota
//const char* ssid = "MARB04";
const char* ssid = "rapspi5";
const char* password = "24052004";
//const char* mqtt_server = "192.168.0.16"; 
const char* mqtt_server = "10.42.0.1";

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  WiFi.disconnect(true);  // borra configuraciones anteriores
  delay(1000);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado, IP:");
  Serial.println(WiFi.localIP());
}

// Pines
#define MOTOR_A1 15
#define MOTOR_A2 2
#define MOTOR_B1 32
#define MOTOR_B2 16

#define LED1 27
#define LED2 5

#define ENCODER_A 23
#define ENCODER_B 14

#define TRIGGER_PIN 12
#define ECHO_PIN 13

#define SDA_PIN 21
#define SCL_PIN 22

#define PWM_A 4
#define PWM_B 25

// Variables de PWM
const int freq = 5000;       // Frecuencia del PWM
const int resolution = 8;    // Resolución en bits (0-255)
const int channel_A = 0;
const int channel_B = 1;

// Variables para sesor de velocidad
volatile unsigned long pulseCountA = 0;
volatile unsigned long pulseCountB = 0;
unsigned long lastMillis = 0;
float RPMA = 0;
float RPMB = 0;
const int pulsesPerRevolution = 20; 
unsigned long currentMillis = 0;
float diametroRueda_cm = 1.9; 
float velocidad_cm_sA = 0;
float velocidad_cm_sB = 0;

void IRAM_ATTR encoderA_ISR(){
  pulseCountA++;
}
void IRAM_ATTR encoderB_ISR(){
  pulseCountB++;
}

// Variables MPU
/*
bool dmpReady = false;
uint8_t mpuIntStatus;
uint8_t devStatus;
uint16_t packetSize;
uint16_t fifoCount;
uint8_t fifoBuffer[64];
Quaternion q;
VectorFloat gravity;
float ypr[3];  // yaw, pitch, roll  
float yawDegrees, degrees;
MPU6050 mpu;
*/


//Variables para sensor ultrasónico
long duration;
float distance;
int flag_send;
void callback(char* topic, byte* payload, unsigned int length) {
  payload[length] = '\0';  // Asegura que sea una cadena terminada en null
  String data = String((char*)payload);
  Serial.print("Mensaje recibido: ");
  Serial.println(data);

  int commaIndex = data.indexOf(',');
  if (commaIndex > 0) {
    int pwm_izq = data.substring(0, commaIndex).toInt();
    int pwm_der = data.substring(commaIndex + 1).toInt();

    // Aplicar PWM
    ledcWrite(PWM_B, pwm_izq);
    ledcWrite(PWM_A, pwm_der);
    flag_send=1;
  }
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("ESP32Client")) {
      Serial.println("Conectado al broker");
      client.subscribe("motor/pwm");
    } else {
      Serial.print("Fallo, estado: ");
      Serial.print(client.state());
      delay(5000);
    }
  }
}

/*
void getdegree(){
  if (!dmpReady) return;
  fifoCount = mpu.getFIFOCount();

  if (fifoCount == 1024) {
    mpu.resetFIFO();
    Serial.println("¡FIFO overflow!");
  } else if (fifoCount >= packetSize) {
    mpu.getFIFOBytes(fifoBuffer, packetSize);
    
    // Obtener cuaternión y calcular yaw/pitch/roll
    mpu.dmpGetQuaternion(&q, fifoBuffer);
    mpu.dmpGetGravity(&gravity, &q);
    mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);

    // Imprimir solo el ángulo de giro en eje Z (Yaw)
    yawDegrees = ypr[0] * 180 / M_PI;
  }
}
*/


void getVelRPM(){
  if (currentMillis - lastMillis >= 1000) {
    lastMillis = currentMillis;
    RPMA = (pulseCountA * 60.0) / pulsesPerRevolution;
    RPMB = (pulseCountB * 60.0) / pulsesPerRevolution;
    pulseCountA = 0;
    pulseCountB = 0;
  }
}

void getDistancia(){
  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);

  duration = pulseIn(ECHO_PIN, HIGH);

  distance = duration * 0.034 / 2; //en centimetros
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  // Configurar salidas digitales
  pinMode(MOTOR_A1, OUTPUT);
  pinMode(MOTOR_A2, OUTPUT);
  pinMode(MOTOR_B1, OUTPUT);
  pinMode(MOTOR_B2, OUTPUT);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);

  // Configurar entradas con interrupciones
  pinMode(ENCODER_A, INPUT_PULLUP);
  pinMode(ENCODER_B, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(ENCODER_A), encoderA_ISR, RISING);
  attachInterrupt(digitalPinToInterrupt(ENCODER_B), encoderB_ISR, RISING);

  // Configurar sensor ultrasónico
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // Configurar MPU
/*
  Wire.begin(SDA_PIN, SCL_PIN);  // SDA, SCL
  mpu.initialize();
  devStatus = mpu.dmpInitialize();
  mpu.setXAccelOffset(2174);
  mpu.setYAccelOffset(-103);
  mpu.setZAccelOffset(1812);
  mpu.setXGyroOffset(-46);
  mpu.setYGyroOffset(4);
  mpu.setZGyroOffset(68);
  if (devStatus == 0) {
    mpu.setDMPEnabled(true);
    dmpReady = true;
    packetSize = mpu.dmpGetFIFOPacketSize();
    Serial.println("DMP inicializado correctamente.");
  } else {
    Serial.print("Error al inicializar DMP. Código: ");
    Serial.println(devStatus);
  }
*/

  // Configurar PWM

  bool okA = ledcAttachChannel(PWM_A, freq, resolution, channel_A);
  bool okB = ledcAttachChannel(PWM_B, freq, resolution, channel_B);
    if (!okA || !okB) {
    Serial.println("Error configurando PWM.");
  }

}
void adelante(){
  digitalWrite(MOTOR_A1, LOW);
  digitalWrite(MOTOR_A2, HIGH);
  digitalWrite(MOTOR_B1, HIGH);
  digitalWrite(MOTOR_B2, LOW);
}

unsigned long lastSend = 0;
void loop() {
  adelante();

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  currentMillis = millis();
  getVelRPM();
  getDistancia();

  if(flag_send==1){
    char payload[50];
    snprintf(payload, sizeof(payload), "%d,%d,%.2f", RPMA, RPMB, distance);
    client.publish("robot/sensores", payload);
  }
    //client.publish("sensor/rpmb", String(RPMB).c_str());
}



