import cv2
import mediapipe as mp
import time
import numpy as np
import requests

# Configurar la IP de la ESP32
esp32_ip = "192.168.1.6"

# Inicializar MediaPipe Hands y dibujo
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Configuración de la captura de video
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

# Configuración de los "botones" en la pantalla
button1_pos = (100, 100)
button2_pos = (300, 100)
button3_pos = (500, 100)
button_radius = 50

# Estado de cada LED y último tiempo de activación
led1_state = False
led2_state = False
led3_state = False
last_toggle_time = [0, 0, 0]  # Tiempos de los últimos cambios para cada LED
toggle_delay = 1.0  # Tiempo mínimo entre cambios (en segundos)

# Función para verificar si el dedo está sobre un "botón"
def is_finger_on_button(finger_pos, button_pos):
    distance = np.linalg.norm(np.array(finger_pos) - np.array(button_pos))
    return distance <= button_radius

# Función para enviar solicitudes a la ESP32
def toggle_led(led_number):
    try:
        response = requests.get(f"http://{esp32_ip}/toggle?led=led{led_number}")
        if response.status_code == 200:
            print(f"LED {led_number} cambiado")
    except requests.exceptions.RequestException as e:
        print(f"Error al comunicarse con la ESP32: {e}")

# Inicializar el módulo de manos de MediaPipe
with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("No se pudo capturar el video.")
            break

        # Convertir la imagen a RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        # Dibujar botones en la pantalla con colores y nombres correspondientes
        cv2.circle(frame, button1_pos, button_radius, (0, 255, 0) if led1_state else (0, 0, 255), -1)
        cv2.putText(frame, "Led 1", (button1_pos[0] - 30, button1_pos[1] + 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.circle(frame, button2_pos, button_radius, (0, 255, 0) if led2_state else (0, 0, 255), -1)
        cv2.putText(frame, "Led 2", (button2_pos[0] - 30, button2_pos[1] + 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.circle(frame, button3_pos, button_radius, (0, 255, 0) if led3_state else (0, 0, 255), -1)
        cv2.putText(frame, "Led 3", (button3_pos[0] - 30, button3_pos[1] + 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Dibujar las anotaciones solo si se detectan manos
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Extraer coordenadas del dedo índice
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_finger_coords = (
                    int(index_finger_tip.x * frame.shape[1]),
                    int(index_finger_tip.y * frame.shape[0])
                )
                cv2.circle(frame, index_finger_coords, 10, (255, 0, 0), -1)

                # Verificar si el dedo está sobre alguno de los "botones" y si ha pasado suficiente tiempo
                current_time = time.time()
                
                if is_finger_on_button(index_finger_coords, button1_pos) and current_time - last_toggle_time[0] > toggle_delay:
                    led1_state = not led1_state
                    toggle_led(1)
                    last_toggle_time[0] = current_time  # Actualizar el tiempo del último cambio para LED1

                elif is_finger_on_button(index_finger_coords, button2_pos) and current_time - last_toggle_time[1] > toggle_delay:
                    led2_state = not led2_state
                    toggle_led(2)
                    last_toggle_time[1] = current_time  # Actualizar el tiempo del último cambio para LED2

                elif is_finger_on_button(index_finger_coords, button3_pos) and current_time - last_toggle_time[2] > toggle_delay:
                    led3_state = not led3_state
                    toggle_led(3)
                    last_toggle_time[2] = current_time  # Actualizar el tiempo del último cambio para LED3

        # Mostrar el video
        cv2.imshow('Detección de Mano con Botones Virtuales', frame)

        # Cerrar la ventana al presionar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Liberar los recursos
cap.release()
cv2.destroyAllWindows()
