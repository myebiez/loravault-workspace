#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "supabase_client.h"

// SICP: Prosedur tunggal yang bertindak sebagai Smart Router dengan Security Definer
void sendToSupabase(const LoRaPacket& packet) {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("[Supabase] Abort: WiFi disconnected. Cannot bridge payload.");
        return;
    }

    HTTPClient http;
    String endpoint = String(SUPABASE_URL);
    
    // 1. Tentukan Endpoint Berdasarkan Tipe Paket (MENGGUNAKAN SECURE RPC)
    if (packet.type == TELEMETRY) {
        endpoint += "/rest/v1/rpc/secure_insert_telemetry";
    } else if (packet.type == REGISTRATION) {
        endpoint += "/rest/v1/rpc/secure_sync_user";
    } else {
        return; // Abaikan jika tipe tidak diketahui
    }
    
    http.begin(endpoint);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("apikey", SUPABASE_KEY);
    http.addHeader("Authorization", "Bearer " + String(SUPABASE_KEY));

    // 2. Rakit JSON Payload secara dinamis (Memory-safe di ESP32)
    // Menyuntikkan HMAC/Token Rahasia Gateway untuk melewati RLS
    StaticJsonDocument<256> doc;
    doc["p_token"] = GATEWAY_TOKEN;
    
    if (packet.type == TELEMETRY) {
        doc["p_rfid_uid"] = packet.uid;
        doc["p_weight_delta"] = packet.weightDelta;
    } else if (packet.type == REGISTRATION) {
        doc["p_rfid_uid"] = packet.uid;
        doc["p_nik"] = packet.nik;
    }
    
    String requestBody;
    serializeJson(doc, requestBody);

    // 3. Tembakkan ke Supabase API
    Serial.println("[Supabase] Executing POST to: " + endpoint);
    int httpResponseCode = http.POST(requestBody);

    // 4. State Machine & Feedback (DOET)
    if (httpResponseCode >= 200 && httpResponseCode < 300) {
        Serial.println("[Supabase] Success! Payload accepted. HTTP " + String(httpResponseCode));
        
        // TRANSMIT ACK BALIK KE LORA KHUSUS UNTUK REGISTRASI
        if (packet.type == REGISTRATION) {
            // Format: ACK|UID\n
            Serial2.print("ACK|");
            Serial2.println(packet.uid);
            Serial.println("[LoRa] ACK Transmitted back to Vault.");
        }
    } 
    // Penanganan anggun jika UID sudah pernah tersinkron (Conflict / 409)
    // RPC mungkin tidak selalu mengembalikan 409 pada exception, 
    // namun blok ini menjadi jaring pengaman jika implementasi database mendeteksi duplikat
    else if (packet.type == REGISTRATION && httpResponseCode == 409) {
        Serial.println("[Supabase] Notice: UID " + packet.uid + " sudah tersinkronisasi di Cloud.");
        // Tetap kirim ACK agar Pi Zero berhenti mencoba sync (Mencegah Infinite Loop)
        Serial2.print("ACK|");
        Serial2.println(packet.uid);
        Serial.println("[LoRa] ACK Transmitted back to Vault (Resolved Conflict).");
    } 
    else {
        Serial.println("[Supabase] POST Failed! HTTP " + String(httpResponseCode) + 
                       " | Reason: " + http.errorToString(httpResponseCode));
    }
    
    http.end();
}