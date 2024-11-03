
### Conexión de LEDs y resistencias a la ESP32-WROOM-32D

#### Componentes necesarios
- 3 LEDs (preferiblemente de diferentes colores para distinguirlos fácilmente).
- 3 resistencias de 220Ω a 330Ω (para limitar la corriente y proteger los LEDs).
- Jumpers de conexión.
- Una placa de pruebas (protoboard).

#### Diagrama de conexión
1. **LED1**:
   - **Ánodo (pierna larga) del LED1**: Conectar a **GPIO 23** de la ESP32.
   - **Cátodo (pierna corta) del LED1**: Conectar a un extremo de la **resistencia de 220Ω**.
   - El otro extremo de la **resistencia de 220Ω**: Conectar a **GND** en la ESP32.

2. **LED2**:
   - **Ánodo (pierna larga) del LED2**: Conectar a **GPIO 22** de la ESP32.
   - **Cátodo (pierna corta) del LED2**: Conectar a un extremo de la **resistencia de 220Ω**.
   - El otro extremo de la **resistencia de 220Ω**: Conectar a **GND** en la ESP32.

3. **LED3**:
   - **Ánodo (pierna larga) del LED3**: Conectar a **GPIO 21** de la ESP32.
   - **Cátodo (pierna corta) del LED3**: Conectar a un extremo de la **resistencia de 220Ω**.
   - El otro extremo de la **resistencia de 220Ω**: Conectar a **GND** en la ESP32.

#### Explicación de la conexión
Cada LED está conectado a un pin GPIO de la ESP32 (23, 22 y 21, respectivamente) que permitirá controlarlos de manera independiente. Las resistencias están en serie con los LEDs para limitar la corriente, protegiendo tanto los LEDs como la ESP32.

#### Nota
Si utilizas resistencias de un valor diferente, asegúrate de que sean lo suficientemente altas para proteger el LED, pero no tan altas como para impedir que el LED encienda correctamente.

---

Este esquema proporciona una explicación clara para quienes deseen replicar el proyecto y conecta correctamente los LEDs de manera segura a la ESP32-WROOM-32D.
