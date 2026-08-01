#pragma once
#include <Arduino.h>

// SICP: Data Abstraction. We do not pass raw strings around; we pass validated structures.
struct LoRaPacket {
    String uid;
    float weightDelta;
    bool valid;
};

void setupLoRa();
LoRaPacket receiveLoRaPacket();