# Setup

## With SD Card in Computer

Plug in SD card to computer.

Install Imager: `% brew install raspberry-pi-imager`

Use Imager to install "Rasp PI OS Lite".

```
eric@mbp-16 synesti % ls -ls /Volumes/
total 7
0 lrwxr-xr-x  1 root  wheel     1 Jun 25 10:54 Macintosh HD -> /
7 drwxrwxrwx@ 1 eric  staff  3584 Feb 12  2020 boot
eric@mbp-16 synesti % ls -ls /Volumes/boot
total 105106
   37 -rwxrwxrwx  1 eric  staff     18693 Jun 24  2019 COPYING.linux
    1 -rwxrwxrwx  1 eric  staff      145 May  7 15:00 issue.txt
11684 -rwxrwxrwx  1 eric  staff  5981944 Apr 30 14:01 kernel.img
12346 -rwxrwxrwx  1 eric  staff  6320888 Apr 30 14:01 kernel7.img
13076 -rwxrwxrwx  1 eric  staff  6694528 Apr 30 14:01 kernel7l.img
15153 -rwxrwxrwx  1 eric  staff  7758283 Apr 30 14:01 kernel8.img
   36 drwxrwxrwx  1 eric  staff    18432 May  7 15:00 overlays
 5768 -rwxrwxrwx  1 eric  staff  2952928 Apr 30 14:01 start.elf
 4354 -rwxrwxrwx  1 eric  staff  2228768 Apr 30 14:01 start4.elf
 1549 -rwxrwxrwx  1 eric  staff   793084 Apr 30 14:01 start4cd.elf
 7271 -rwxrwxrwx  1 eric  staff  3722504 Apr 30 14:01 start4db.elf
```

### Give SSH acess

Give ssh access with `% touch /Volumes/boot/ssh` like

```
% ls -ls /Volumes/boot
total 96341
   37 -rwxrwxrwx  1 eric  staff    18693 Jan  5 06:30 COPYING.linux
   ...
% touch /Volumes/boot/ssh
% ls -ls /Volumes/boot
total 96341
   37 -rwxrwxrwx  1 eric  staff    18693 Jan  5 06:30 COPYING.linux
    ...
    0 -rwxrwxrwx  1 eric  staff        0 Jun 25 18:17 ssh
    ...
```

### Allow USB access

Next, add `dtoverlay=dwc2` with `sudo nano /Volumes/boot/config.txt` like

```
# Allow USB access as gadget
dtoverlay=dwc2
```

See: https://raspberrypi.stackexchange.com/questions/77059/what-does-dtoverlay-dwc2-really-do/77061

Then using `sudo nano /Volumes/boot/cmdline.txt`, add `modules-load=dwc2,g_ether` after `rootwait` with one space on either side.

## Move SD card to Rasp Pi

Move SSD card to Rasp Pi. Ready when _RNDIS/Ethernet Gadget_ shows Self-Assigned IP (yellow dot) in _System Preferences > Network_.

### Setup SSH ids

See: https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md

If known host error, erase old pi in `% nano ~/.ssh/known_hosts`.

Add public key with `% ssh-copy-id pi@raspberrypi.local` from Mac side if `id_rsa.pub` exists in `ls ~/.ssh`, config.

Then connect with `ssh 'pi@raspberrypi.local'`.

To be safe, change password with `passwd` and save locally.

Connect with `% ssh pi@raspberrypi.local`. Success looks like `pi@raspberrypi:~ $ `

Note: default username password is: "pi" "raspberry".

Check OS version like

```
$ cat /etc/debian_version
10.9
```

### Setup Internet

(Note: 10.9 already has `nameserver 8.8.8.8`)
Check `ping 1.1.1.1`. If "Host Unreachable", use `sudo nano /etc/resolv.conf`. to set nameserver like

```
nameserver 1.1.1.3
nameserver 1.0.0.3

```

Connect to LAN with https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md and note that "On a fresh install ... you will need to specify the country in which the device is being used".

Generate an ecrypted key with `wpa_passphrase {SSID}`, then copy the result into `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf` minus the commented out plain text line. Note that SSID seems to affect the generated PSK.

Then `wpa_cli -i wlan0 reconfigure` and check with `ifconfig wlan0` for an something like `inet6 fe80::58b4:83c5:1bbf:a359`. If not working, check SSID and password.

### Update packages and install Go

Try `sudo apt update` and then, optionally `sudo apt list --upgradable`, then `sudo apt upgrade`.

Then finally, `sudo apt install golang` and check with

```sh
pi@raspberrypi:~ $ go version
go version go1.11.6 linux/arm
```

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

## Useful commands

apt install git

sudo reboot

ssh pi@raspberrypi.local

setup ssh key on pi for git commits
https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account

# check SSID of connected WiFi network

iwgetid

# more details about WiFi

iwconfig

# get ip address

ifconfig

wlan0: inet 192.168.87.37 netmask 255.255.255.0 broadcast 192.168.87.255

ip addr show
inet 192.168.87.37/24 brd 192.168.87.255 scope global dynamic noprefixroute wlan0

## Useful files

/etc/resolv.conf for name servers

sudo nano /etc/dhcpcd.conf for static IP

## Cables

## TODOs

Use ssh key rather than default password.

hostname
clientid

###########

Install fresh OS image

On Mac

`% brew install raspberry-pi-imager`

Then Install "Rasp PI OS Lite" to SD card.

Then
