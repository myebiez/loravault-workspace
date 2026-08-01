#include <Arduino.h>
#include "wifi_manager.h"
#include "lora_receiver.h"
#include "supabase_client.h"

// SICP: The conductor of the system. 
// Dependencies flow unidirectionally. The main loop does no calculations itself.
void setup() {
    Serial.begin(115200);
    delay(1000); 
    
    Serial.println("\n=== LoRaVault ESP32 Gateway Active ===");
    
    setupWiFi();
    setupLoRa();
}

void loop() {
    // 1. Check for incoming UART LoRa transmission
    LoRaPacket packet = receiveLoRaPacket();
    
    // 2. Bridge to Cloud if packet meets criteria
    if (packet.valid) {
        sendToSupabase(packet);
    }
    
    // Pragmatic: Yield time to RTOS to prevent Watchdog Timer (WDT) kernel panics.
    delay(50);
}