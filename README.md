# lawnmower
The purpose of this build is summarized in three milestones:

1. Make a robot lawnmower remote controlled via computer
2. Make Robot lawn mower autonomous inside an area using a statically mounted camera pointed at a designated mowing area
3. Cut a Van Gogh

## Run

### Optional (Mandatory if starting server from different directory)

sudo nano /etc/environment

PATH_TO_MOWER_FILES="/home/pi/lawnmower/"

### Mandatory

Plug in Arduino using usb

pip3 install pyserial

python3 server.py

Server runs on port 8080


## Autostart on boot
```
sudo crontab -e

>>> @reboot /usr/local/bin/forever start -c /usr/bin/python3.7 /home/pi/soil-data/serial-ingestion.py

```

## Arduino wires

| Color|Pin|
|---|---|
|Brun-lila|7|
|Grön-lila|6|
|Lila-grå|Gnd|
|Gul-grå|5v|
|(1) Grön-röd|10|
|(2) Grön-röd|9|
