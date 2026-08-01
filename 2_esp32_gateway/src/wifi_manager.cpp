#include <WiFi.h>
#include "wifi_manager.h"

void setupWiFi() {
    Serial.print("[WiFi] Connecting to AP");
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    
    // Pragmatic: Fail-fast with bounded retries. Never loop infinitely in the void.
    int retries = 0;
    while (WiFi.status() != WL_CONNECTED && retries < 20) {
        delay(500);
        Serial.print(".");
        retries++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
        // DOET: Visibility. Output the system state to the physical debug monitor.
        Serial.println("\n[WiFi] Connected! IP: " + WiFi.localIP().toString());
    } else {
        Serial.println("\n[WiFi] CRITICAL ERROR: Failed to connect! Halting.");
        while(1); // CLRS: Halt execution; system invariants are broken.
    }
}