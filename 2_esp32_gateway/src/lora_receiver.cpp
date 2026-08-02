#include "lora_receiver.h"

// Hardware Mapping: ESP32 HardwareSerial 2 (RX2=16, TX2=17)
#define RX_PIN 16
#define TX_PIN 17

void setupLoRa() {
    Serial2.begin(9600, SERIAL_8N1, RX_PIN, TX_PIN);
    Serial.println("[LoRa] UART Interface Initialized (9600 8N1)");
}

LoRaPacket receiveLoRaPacket() {
    LoRaPacket packet = {UNKNOWN, "", 0.0, "", false};
    
    if (Serial2.available()) {
        // CLRS: \mathcal{O}(N) time complexity where N is the characters in the buffer.
        String raw = Serial2.readStringUntil('\n');
        raw.trim();
        
        int firstPipe = raw.indexOf('|');
        if (firstPipe > 0) {
            String prefix = raw.substring(0, firstPipe);
            
            // ROUTE 1: TELEMETRI SENSOR (Format: TLM|UID|DELTA)
            if (prefix == "TLM") {
                int secondPipe = raw.indexOf('|', firstPipe + 1);
                if (secondPipe > 0) {
                    packet.type = TELEMETRY;
                    packet.uid = raw.substring(firstPipe + 1, secondPipe);
                    packet.weightDelta = raw.substring(secondPipe + 1).toFloat();
                    packet.valid = true;
                    
                    Serial.println("[LoRa] TLM Diterima -> UID: " + packet.uid + " | Delta: " + String(packet.weightDelta) + "g");
                }
            } 
            // ROUTE 2: REGISTRASI CLOUD (Format: REG|UID|NIK)
            else if (prefix == "REG") {
                int secondPipe = raw.indexOf('|', firstPipe + 1);
                if (secondPipe > 0) {
                    packet.type = REGISTRATION;
                    packet.uid = raw.substring(firstPipe + 1, secondPipe);
                    packet.nik = raw.substring(secondPipe + 1); // Ambil sisa string sebagai NIK
                    packet.valid = true;
                    
                    Serial.println("[LoRa] REG Diterima -> UID: " + packet.uid + " | NIK: " + packet.nik);
                }
            } else {
                Serial.println("[LoRa] Error: Prefix tidak valid -> " + raw);
            }
        }
    }
    return packet;
}