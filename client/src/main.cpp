/*
 * e-Alfred client-side code 
 */


/*
 *  Includes
 */
#include <ArduinoJson.h>
#include <SPI.h>
#include <Ethernet.h>

/*
 *  Macros
 */
#define SERIAL_BAUD_RATE      115200
const byte MAC_ADDRESS [6] =  {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};

/*
 *  Declaring EthernetServer
 */
EthernetServer server(80);

/*
 *  Parsing function
 */
JsonObject& ParseRequest (String req_body) {
  StaticJsonBuffer<300> JSONBuffer;                         //Memory pool
  JsonObject& parsed = JSONBuffer.parseObject(req_body); //Parse message
 
  if (!parsed.success()) {   //Check for errors in parsing
    Serial.println("===== Parsing failed");
    return;
  }

  return parsed;
}

/*
 *  Executing function
 */
int ExecuteActions (JsonObject& parsed_request) {
  int request_type = parsed_request["request_type"]; //Get request type 
  int port_type = parsed_request["port_type"];//Get the port type
  int port_number = parsed_request["port_number"];//Get the port number
  int value = parsed_request["value"];//Get the value


  if (request_type == 0){
    int reading = 0;
    if (port_type == 0){
      pinMode("A" + port_number,INPUT);
      reading = analogRead("A" + port_number);
    }
    if (port_type == 1){
      pinMode(port_number,INPUT);
      reading = digitalRead(port_number);
    }
    return reading;
  }
  
  if (request_type == 1){
    if (port_type == 0){
      pinMode("A" + port_number,OUTPUT);
      analogWrite("A" + port_number, value);
    }
    if (port_type == 1){
      pinMode(port_number,OUTPUT);
      digitalWrite(port_number,value);
    }
    return value;
  }
   
   
   if (request_type == 2){
    if (port_type == 1){
      pinMode(port_number,OUTPUT);
      analogWrite(port_number,value);
    }
    return value;
  }

  return -1;
}

/*
 *  POST response function
 */
String BuildResponse (int reading) {
  String response = "";
  response += "{\"data\": ";
  response += reading;
  response += "}";
  return response;
}

/*
 *  Setup
 */
void setup() {
  // Starts serial
  Serial.begin(SERIAL_BAUD_RATE);
  while (!Serial) {
    ;
  }

  // Starts server
  Ethernet.begin(MAC_ADDRESS);
  server.begin();
  Serial.print("Arduino IP: ");
  Serial.println(Ethernet.localIP());
}


void loop() {
  // Listen for incoming clients
  EthernetClient client = server.available();
  if (client) {
    boolean currentLineIsBlank = true;
    String req_str = "";
    String req_body = "";
    int data_length = -1;
    boolean post_request = false;

    while (client.connected()) 
    {
      if (client.available()) {
        // Getting request string
        char c = client.read();
        req_str += c;

        // Parsing GET requests
        if (c == '\n' && currentLineIsBlank && req_str.startsWith("GET")) {
          client.println("<html><head><title>e-Alfred</title></head><body><h2> You found me! (e-Alfred)</h2></body></html>");
          break;
        }
        // Parsing POST requests
        if (c == '\n' && currentLineIsBlank && req_str.startsWith("POST")) {
          post_request = true;
          String aux = req_str.substring(req_str.indexOf("Content-Length:") + 15);
          aux.trim();
          data_length = aux.toInt();
          while(data_length-- > 0)
          {
            c = client.read();
            req_body += c;
          }
          JsonObject& parsed = ParseRequest(req_body);
          int reading = ExecuteActions(parsed);
          String response = BuildResponse(reading);

          String httpResponse = "HTTP/1.1 200 OK";
          httpResponse += "\r\nContent-Type: application/json";
          httpResponse += "\r\nContent-Length: ";
          httpResponse += response.length();
          httpResponse += "\r\nConnection: close\r\n\r\n";
          httpResponse += response + " ";
          // client.println("HTTP/1.1 200 OK");
          // client.print("Content-Length: ");
          // client.println(response.length());
          // client.println("Connection: close");
          // client.println("Content-Type: application/json");
          client.println(httpResponse);
          Serial.println(httpResponse);
          // REMOVE!!!!!!!!!!!!!!!!!!!!!!!!!!!
          // client.println("<html><head><title>e-Alfred</title></head><body><h2> You found me! (e-Alfred)</h2></body></html>");

          break;
        }
        // I have no idea what's happening here
        if (c == '\n') {
          currentLineIsBlank = true;
        } else if (c != '\r') {
          currentLineIsBlank = false;
        }
      }
    }
    Serial.print("BODY => ");
    Serial.println(req_body);

    // give the web browser time to receive the data
    delay(1);
    // close the connection:
    client.stop();
    Serial.println("client disconnected");
  }
}