# Fluke 8000A Datalogger
The Fluke 8000 A Desk Multimeter from 1982 has an optional Digital Output Unit (DOU) which features a 20-pin PCB edge connector on the back of the device. This project uses a ATMega328P read and log the values on this port to a PC

## Getting started
### Hardware
- 3D printer
    - To print the connector, which can be found in the `/compontents` folder
- 0.5 mm solid core wire
    - Used to create the contact traces in the connector
- Any 5V logic ATMega MCU with sufficient IO
    - At least 16 are required unless you want to use a multiplexer

#### Wire diagram
TODO

### Software
#### MCU
This project uses PlatformIO; However the code can easily be converted to use Arduino IDE by simply copying the contents of `/src/main.cpp` to a `.ino` file. 

#### PC 
TODO


## Resources
- [Manual and Datasheet Fluke 8000A](https://xdevs.com/doc/Fluke/8000a.pdf)