#include "lora_receiver.h"

// Hardware Mapping: ESP32 HardwareSerial 2 (RX2=16, TX2=17)
#define RX_PIN 16
#define TX_PIN 17

void setupLoRa() {
    Serial2.begin(9600, SERIAL_8N1, RX_PIN, TX_PIN);
    Serial.println("[LoRa] UART Interface Initialized (9600 8N1)");
}

LoRaPacket receiveLoRaPacket() {
    LoRaPacket packet = {"", 0.0, false};
    
    if (Serial2.available()) {
        // CLRS: \mathcal{O}(N) time complexity where N is the characters in the buffer.
        // We use string traversal to extract the payload strictly matching our private protocol.
        String raw = Serial2.readStringUntil('\n');
        raw.trim();
        
        int separatorIdx = raw.indexOf('|');
        if (separatorIdx > 0) {
            packet.uid = raw.substring(0, separatorIdx);
            packet.weightDelta = raw.substring(separatorIdx + 1).toFloat();
            packet.valid = true;
            
            // DOET: Feedback. Log clear success messages.
            Serial.println("[LoRa] Valid Packet Extracted -> UID: " + packet.uid + 
                           " | Delta: " + String(packet.weightDelta) + "g");
        } else {
            // DOET: Error Signifier. Never blame the user, log the exact malformed string.
            Serial.println("[LoRa] Error: Malformed private packet: " + raw);
        }
    }
    return packet;
}