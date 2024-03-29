# lawnmower
The purpose of this build is summarized in three milestones:

1. Make a robot lawnmower remote controlled via computer
2. Make Robot lawn mower autonomous inside an area using a statically mounted camera pointed at a designated mowing area
3. Cut a Van Gogh

## Run

Plug in the Arduino to the PC

Start the server, providing portnumber

python3 socket_server.py 5000

Start the client proviing hostname and portnumber

python3 socket_server.py 0.0.0.0 5000

### Mandatory

Plug in Arduino using usb

pip3 install pyserial

pip3 install bitstring

python3 socket_server.py

Server runs on port 5000

## Develop
Add new dependencies to


## Autostart on boot
```
crontab -e

>>> @reboot /usr/local/bin/forever start -c /usr/bin/python3.7 /home/pi/soil-data/serial-ingestion.py

```
# Arduino

## Wires

| Color|Pin|
|---|---|
|Brun-lila|7|
|Grön-lila|6|
|Lila-grå|5v|
|Gul-grå|Gnd|
|(1) Grön-röd|10|
|(2) Grön-röd|9|

### On the motor driver
5v       5v output
EL       Motor enable input (5v)
Signal   speedometer output
Z/F      forward/reverse control (5v/GND)
VR       speed control (0..5v)
GND      ground

## Serial protocol
|LEFT_MOTOR_SIGNED_SHORT|RIGHT_MOTOR_SIGNED_SHORT|DIRECTION_BYTE|

DIRECTION_BYTE := 0000 00[0|1][0|1]
Where the last two bytes are the direction on the left and the right wheel

#### LEFT_MOTOR_SIGNED_SHORT
A short (2 bytes) containing a number between 0-1023. Values higher than 1023 will be interpreted as 1023. Values lower than 0 will be interpreted as 0. The value sets the PWM frequency of the left motor driver.

#### RIGHT_MOTOR_SIGNED_SHORT
A short (2 bytes) containing a number between 0-1023. Values higher than 1023 will be interpreted as 1023. Values lower than 0 will be interpreted as 0. The value sets the PWM frequency of the left motor driver.

#### DIRECTION_BYTE
- First bit represents left wheels spinning direction
- Second bit represents right wheels spinning direction
- Rest six bits are left unused available for future enhancements
