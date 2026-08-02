#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "supabase_client.h"

// SICP: Prosedur tunggal yang bertindak sebagai Smart Router
void sendToSupabase(const LoRaPacket& packet) {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("[Supabase] Abort: WiFi disconnected. Cannot bridge payload.");
        return;
    }

    HTTPClient http;
    String endpoint = String(SUPABASE_URL);
    
    // 1. Tentukan Endpoint Berdasarkan Tipe Paket
    if (packet.type == TELEMETRY) {
        endpoint += "/rest/v1/transactions_log";
    } else if (packet.type == REGISTRATION) {
        endpoint += "/rest/v1/users";
    } else {
        return; // Abaikan jika tipe tidak diketahui
    }
    
    http.begin(endpoint);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("apikey", SUPABASE_KEY);
    http.addHeader("Authorization", "Bearer " + String(SUPABASE_KEY));
    http.addHeader("Prefer", "return=representation");

    // 2. Rakit JSON Payload secara dinamis (Memory-safe di ESP32)
    StaticJsonDocument<256> doc;
    
    if (packet.type == TELEMETRY) {
        doc["rfid_uid"] = packet.uid;
        doc["weight_delta"] = packet.weightDelta;
    } else if (packet.type == REGISTRATION) {
        doc["rfid_uid"] = packet.uid;
        doc["nik"] = packet.nik; // Kirim NIK ke Cloud
    }
    
    String requestBody;
    serializeJson(doc, requestBody);

    // 3. Tembakkan ke Supabase API
    Serial.println("[Supabase] Executing POST to: " + endpoint);
    int httpResponseCode = http.POST(requestBody);

    if (httpResponseCode >= 200 && httpResponseCode < 300) {
        Serial.println("[Supabase] Success! Payload accepted. HTTP " + String(httpResponseCode));
    } 
    // Penanganan anggun jika UID sudah pernah tersinkron (Conflict / 409)
    else if (packet.type == REGISTRATION && httpResponseCode == 409) {
        Serial.println("[Supabase] Notice: UID " + packet.uid + " sudah tersinkronisasi di Cloud.");
    } 
    else {
        Serial.println("[Supabase] POST Failed! HTTP " + String(httpResponseCode) + 
                       " | Reason: " + http.errorToString(httpResponseCode));
    }
    
    http.end();
}