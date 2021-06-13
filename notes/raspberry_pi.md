## Raspberry pi

Get IP and set up program

```sh
% ping raspberrypi.local
PING raspberrypi.local (192.168.11.2): 56 data bytes
64 bytes from 192.168.11.2: icmp_seq=0 ttl=64 time=9.580 ms
% ssh pi@192.168.11.2
% raspberry
% scp -r homeAssistant/ pi@192.168.11.2:/home/pi/project
% % crontab -e
@reboot python3 src/main.py -v -b 10.0.0.23 -p 10.0.0.22
:wq
```

TODO:
Put wifi info into file
