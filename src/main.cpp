#include <Arduino.h>

// Pin definitions
#define FL8000A_MSD 14   // First digit 1/0
#define FL8000A_2MSD_8 2 // Second digit 8/4/2/1
#define FL8000A_2MSD_4 3
#define FL8000A_2MSD_2 4
#define FL8000A_2MSD_1 5
#define FL8000A_3MSD_8 6 // Third digit 8/4/2/1
#define FL8000A_3MSD_4 7
#define FL8000A_3MSD_2 8
#define FL8000A_3MSD_1 9
#define FL8000A_LSD_8 10 // Last digit 8/4/2/1
#define FL8000A_LSD_4 11
#define FL8000A_LSD_2 12
#define FL8000A_LSD_1 13
#define FL8000A_POLARITY 15 // Polarity 1/0
#define FL8000A_OVERLOAD 17 // Display overload warning 1/0
#define FL8000A_BUSY 16     // Busy signal 1/0

char busy = 0;
char busy_last = 0;

void setup()
{
  Serial.begin(9600);

  pinMode(FL8000A_MSD, INPUT);
  pinMode(FL8000A_2MSD_8, INPUT);
  pinMode(FL8000A_2MSD_4, INPUT);
  pinMode(FL8000A_2MSD_2, INPUT);
  pinMode(FL8000A_2MSD_1, INPUT);
  pinMode(FL8000A_3MSD_8, INPUT);
  pinMode(FL8000A_3MSD_4, INPUT);
  pinMode(FL8000A_3MSD_2, INPUT);
  pinMode(FL8000A_3MSD_1, INPUT);
  pinMode(FL8000A_LSD_8, INPUT);
  pinMode(FL8000A_LSD_4, INPUT);
  pinMode(FL8000A_LSD_2, INPUT);
  pinMode(FL8000A_LSD_1, INPUT);
  pinMode(FL8000A_POLARITY, INPUT);
  pinMode(FL8000A_OVERLOAD, INPUT);
  pinMode(FL8000A_BUSY, INPUT);
}

void update()
{
  // Read the input pins
  uint8_t msd = digitalRead(FL8000A_MSD);
  uint8_t msd2 = digitalRead(FL8000A_2MSD_8) * 8 + digitalRead(FL8000A_2MSD_4) * 4 + digitalRead(FL8000A_2MSD_2) * 2 + digitalRead(FL8000A_2MSD_1);
  uint8_t msd3 = digitalRead(FL8000A_3MSD_8) * 8 + digitalRead(FL8000A_3MSD_4) * 4 + digitalRead(FL8000A_3MSD_2) * 2 + digitalRead(FL8000A_3MSD_1);
  uint8_t lsd = digitalRead(FL8000A_LSD_8) * 8 + digitalRead(FL8000A_LSD_4) * 4 + digitalRead(FL8000A_LSD_2) * 2 + digitalRead(FL8000A_LSD_1);
  uint8_t polarity = digitalRead(FL8000A_POLARITY);
  uint8_t overload = digitalRead(FL8000A_OVERLOAD);

  // Print the values
  char buffer[64];
  sprintf(buffer, "{\"digits\":[%d, %d, %d, %d], "
                  "\"polarity\":%d, "
                  "\"overload\":%d}",
                  msd, msd2, msd3, lsd,
                  polarity, overload);
  Serial.println(buffer);
}

void loop()
{
  // Read the input pins
  busy = digitalRead(FL8000A_BUSY);

  // Update Serial if busy falling edge
  if (busy == 0 && busy_last == 1)
  {
    update();
  }

  busy_last = busy;
}
