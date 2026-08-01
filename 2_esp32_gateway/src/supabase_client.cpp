#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "supabase_client.h"

// SICP: Procedural Abstraction mapping the hardware layer directly into the REST layer.
void sendToSupabase(const LoRaPacket& packet) {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("[Supabase] Abort: WiFi disconnected. Cannot bridge payload.");
        return;
    }

    HTTPClient http;
    // Route matches our upcoming PostgreSQL schema
    String endpoint = String(SUPABASE_URL) + "/rest/v1/transactions_log";
    
    http.begin(endpoint);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("apikey", SUPABASE_KEY);
    http.addHeader("Authorization", "Bearer " + String(SUPABASE_KEY));
    http.addHeader("Prefer", "return=representation"); // Returns the inserted row

    // Pragmatic Programmer: DRY Memory Management.
    // Static allocation prevents heap fragmentation on the ESP32.
    StaticJsonDocument<200> doc;
    doc["rfid_uid"] = packet.uid;
    doc["weight_delta"] = packet.weightDelta;
    
    String requestBody;
    serializeJson(doc, requestBody);

    Serial.println("[Supabase] Executing POST request...");
    int httpResponseCode = http.POST(requestBody);

    if (httpResponseCode >= 200 && httpResponseCode < 300) {
        Serial.println("[Supabase] Success! Payload accepted. HTTP " + String(httpResponseCode));
    } else {
        // Error Recovery: Provide actionable feedback.
        Serial.println("[Supabase] POST Failed! HTTP " + String(httpResponseCode) + 
                       " | Reason: " + http.errorToString(httpResponseCode));
    }
    
    http.end();
}