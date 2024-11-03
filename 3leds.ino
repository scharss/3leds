#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "xxxxxx";
const char* password = "xxxxxx";

// Pines de los LEDs
const int LED1_PIN = 23;
const int LED2_PIN = 22;
const int LED3_PIN = 21;

WebServer server(80);  // Configura el servidor web en el puerto 80

// Estados de los LEDs
bool led1State = false;
bool led2State = false;
bool led3State = false;

// Función para controlar los LEDs
void handleLEDControl(String led) {
  if (led == "led1") {
    led1State = !led1State;
    digitalWrite(LED1_PIN, led1State ? HIGH : LOW);
    Serial.println("LED1 toggled " + String(led1State ? "ON" : "OFF"));
  } else if (led == "led2") {
    led2State = !led2State;
    digitalWrite(LED2_PIN, led2State ? HIGH : LOW);
    Serial.println("LED2 toggled " + String(led2State ? "ON" : "OFF"));
  } else if (led == "led3") {
    led3State = !led3State;
    digitalWrite(LED3_PIN, led3State ? HIGH : LOW);
    Serial.println("LED3 toggled " + String(led3State ? "ON" : "OFF"));
  }
  server.send(200, "text/plain", "OK");  // Responde con "OK" para confirmar que se ejecutó correctamente
}

void setup() {
  Serial.begin(115200);

  // Configuración de los pines de los LEDs como salida
  pinMode(LED1_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
  pinMode(LED3_PIN, OUTPUT);

  // Conexión a la red Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi.");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Configuración de la ruta para controlar los LEDs
  server.on("/toggle", []() {
    if (server.hasArg("led")) {  // Comprueba si hay un argumento "led" en la solicitud
      handleLEDControl(server.arg("led"));
    } else {
      server.send(400, "text/plain", "Missing LED argument");  // Responde con un error si falta el argumento
      Serial.println("Invalid request: Missing LED argument");
    }
  });

  server.begin();
  Serial.println("Server started.");
}

void loop() {
  server.handleClient();  // Maneja las solicitudes entrantes del cliente
}
