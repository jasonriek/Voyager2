#include <Preferences.h>
#include <nvs_flash.h>
Preferences preferences;

#include "math.h"
#include <Wire.h>
#include <ArduinoJson.h>
StaticJsonDocument<256> jsonCmdReceive;
StaticJsonDocument<256> jsonInfoSend;

#include "IMU.h"
#include "config.h"
#include "speed.h"

#include "IRCutCtrl.h"
#include "motorCtrl.h"
#include "pwmServoCtrl.h"
#include "screenCtrl.h"
#include "powerInfo.h"
#include "busServoCtrl.h"

#include "baseFunctions.h"
#include "commands.h"

void setup() {
  Wire.begin(S_SDA, S_SCL);
  Serial.begin(UART_BAUD);  // Initialize serial communication at 1,000,000 baud
  preferences.begin("config", false);
  leftRate = preferences.getFloat("leftRate", 1);
  rightRate = preferences.getFloat("rightRate", 1);

  while(!Serial){}
  pinInit();
  IRIO_Init();
  pwmServoInit();
  pwmServoCtrl(90);
  busServoInit();

  InitScreen();
  allDataUpdate();
  imuInit();
}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming JSON message
    String receivedJson = Serial.readStringUntil('\n');
    readCommand(receivedJson);
  }
  delay(100);
}