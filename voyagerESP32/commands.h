#define MOVE 1
#define TURN 2


void readCommand(String receivedJson) {
  // Parse the command
  DynamicJsonDocument jsonDoc(256);
  DeserializationError error = deserializeJson(jsonDoc, receivedJson);
  int directionR = 0;
  int directionL = 0;
  
  // Check for parsing errors
  if (error) {
    Serial.print("Error decoding received JSON: ");
    Serial.println(error.c_str());
  }
  else {
      // Get the command
      int cmd = jsonDoc["cmd"].as<int>();

      String message = "Nothing to do...";
      switch(cmd) {

        case EMERGENCY_STOP:
          emergencyStop();
          message = "Emergency stop called.";
          break;

        case MOVE:
          // Moves the right wheels
          directionR = jsonDoc["valA"].as<float>();
          // Moves the left wheels
          directionL = jsonDoc["valB"].as<float>();
          webMotorCtrl(directionR, directionL);
          message = "Voyager is moving.";
          break;

        case TURN:
          //  (1, -1) turns right
          //  (-1, 1) turns left
          directionR = jsonDoc["valA"].as<float>();
          directionL = jsonDoc["valB"].as<float>();
          webMotorCtrl(directionR, directionL);
          message = "Voyager is turning.";
          break;
      }

      // Send a response back to the client
      DynamicJsonDocument responseDoc(200);
      responseDoc["message"] = message;
      String responseJson;
      serializeJson(responseDoc, responseJson);
      Serial.println(responseJson);
      //handleDeviceInfo();
  }

}