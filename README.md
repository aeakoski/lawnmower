# lawnmower

## Run

### Optional (Good is starting server from other than lawnmower directory)

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
