#pragma once
#include <Arduino.h>

// SICP: Abstraksi Tipe Data
enum PacketType {
    UNKNOWN,
    TELEMETRY,
    REGISTRATION
};

struct LoRaPacket {
    PacketType type;
    String uid;
    float weightDelta; // Hanya dipakai jika type == TELEMETRY
    String nik;        // Hanya dipakai jika type == REGISTRATION
    bool valid;
};

void setupLoRa();
LoRaPacket receiveLoRaPacket();