
/* =========================================================
   PROJECT: AI-BASED SMART METRO CROWD MONITORING SYSTEM

   BOARD: ESP32
   LANGUAGE: Arduino C++

   FUNCTION:
   1. Receive data from Raspberry Pi through UART
   2. Separate passenger count and crowd status
   3. Validate received information
   4. Display information on 16x2 LCD using I2C
   5. Detect communication failure using timeout
   ========================================================= */


// ---------------------------------------------------------
// 1. INCLUDE REQUIRED LIBRARIES
// ---------------------------------------------------------

#include <Wire.h>               // I2C communication
#include <LiquidCrystal_I2C.h>  // LCD control


// ---------------------------------------------------------
// 2. LCD CONFIGURATION
// ---------------------------------------------------------

// LCD I2C address = 0x27
// Number of columns = 16
// Number of rows = 2

LiquidCrystal_I2C lcd(0x27, 16, 2);


// ---------------------------------------------------------
// 3. UART PIN CONFIGURATION
// ---------------------------------------------------------

#define RXD2 16
#define TXD2 17

// RXD2 receives data from Raspberry Pi
// TXD2 can transmit data back if needed


// ---------------------------------------------------------
// 4. GLOBAL VARIABLES
// ---------------------------------------------------------

int passengerCount = 0;

// Initial crowd status
String crowdStatus = "WAITING";

// Stores the time of last valid data reception
unsigned long lastReceived = 0;

// Communication timeout = 5 seconds
const unsigned long TIMEOUT = 5000;


// ---------------------------------------------------------
// 5. SETUP FUNCTION
// ---------------------------------------------------------

void setup()
{

    // Initialize USB serial communication
    // Used for debugging through Serial Monitor

    Serial.begin(115200);


    // Initialize UART2 communication
    //
    // 115200 = Baud rate
    // SERIAL_8N1 = 8 data bits, no parity, 1 stop bit
    // RXD2 = GPIO16
    // TXD2 = GPIO17

    Serial2.begin(
        115200,
        SERIAL_8N1,
        RXD2,
        TXD2
    );


    // Initialize I2C
    // GPIO21 = SDA
    // GPIO22 = SCL

    Wire.begin(21, 22);


    // Initialize LCD

    lcd.init();

    // Turn on LCD backlight
    lcd.backlight();


    // Display startup message

    lcd.setCursor(0, 0);

    lcd.print("METRO MONITOR");

    lcd.setCursor(0, 1);

    lcd.print("INITIALIZING...");


    delay(2000);

    lcd.clear();


    // Initialize timeout reference
    lastReceived = millis();

    Serial.println("ESP32 INITIALIZED");

}


// ---------------------------------------------------------
// 6. FUNCTION TO UPDATE LCD
// ---------------------------------------------------------

void updateLCD()
{

    // Clear previous display contents
    lcd.clear();


    // First row: passenger count

    lcd.setCursor(0, 0);

    lcd.print("PASSENGERS: ");

    lcd.print(passengerCount);


    // Second row: crowd status

    lcd.setCursor(0, 1);

    lcd.print("STATUS: ");

    lcd.print(crowdStatus);

}


// ---------------------------------------------------------
// 7. FUNCTION TO PROCESS RECEIVED DATA
// ---------------------------------------------------------

void processData(String data)
{

    // Remove spaces and newline characters
    data.trim();


    // Find position of comma
    //
    // Example:
    // data = "35,MEDIUM"
    // separator = 2

    int separator = data.indexOf(',');


    // If comma is not found, reject the message

    if (separator == -1)
    {
        Serial.println("INVALID DATA FORMAT");
        return;
    }


    // Extract passenger count
    //
    // substring(0, 2) gives "35"

    String countString = data.substring(
        0,
        separator
    );


    // Extract crowd status
    //
    // substring(3) gives "MEDIUM"

    String statusString = data.substring(
        separator + 1
    );


    // Remove unwanted spaces

    countString.trim();

    statusString.trim();


    // Validate that count contains only digits

    if (countString.length() == 0)
    {
        return;
    }

    for (int i = 0; i < countString.length(); i++)
    {
        if (!isDigit(countString[i]))
        {
            Serial.println("INVALID COUNT");
            return;
        }
    }


    // Convert String into integer

    int newCount = countString.toInt();


    // Validate passenger count

    if (newCount < 0 || newCount > 1000)
    {
        Serial.println("INVALID PASSENGER COUNT");
        return;
    }


    // Validate crowd status

    if (
        statusString != "LOW" &&
        statusString != "MEDIUM" &&
        statusString != "HIGH" &&
        statusString != "OVERLOAD"
    )
    {
        Serial.println("INVALID CROWD STATUS");
        return;
    }


    // Update global variables

    passengerCount = newCount;

    crowdStatus = statusString;


    // Update the last valid reception time

    lastReceived = millis();


    // Print received information in Serial Monitor

    Serial.print("PASSENGERS: ");

    Serial.println(passengerCount);

    Serial.print("CROWD STATUS: ");

    Serial.println(crowdStatus);


    // Update LCD

    updateLCD();

}


// ---------------------------------------------------------
// 8. MAIN LOOP
// ---------------------------------------------------------

void loop()
{

    // Check whether UART2 has incoming data

    if (Serial2.available() > 0)
    {

        // Read incoming data until newline character

        String receivedData = Serial2.readStringUntil('\n');


        // Process received information

        processData(receivedData);

    }


    // -----------------------------------------------------
    // CHECK COMMUNICATION TIMEOUT
    // -----------------------------------------------------

    // millis() gives elapsed time since ESP32 started
    //
    // If no valid data arrives within 5 seconds,
    // display a communication error.

    if (millis() - lastReceived > TIMEOUT)
    {

        lcd.setCursor(0, 0);

        lcd.print("NO LIVE DATA    ");


        lcd.setCursor(0, 1);

        lcd.print("CHECK CONNECTION");

    }

}
