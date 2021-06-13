Share daily activities with far away people you care about
by passively mapping your activity here to observable things there.

For example, every time you make tea in your kitchen,
your mom can see a pleasant orange glow in her kitchen,
and vice-versa.

# Status

Very much in development!

See below for help.

# Usage

## Overview

Obtain and setup a plug and lightbulb, connect to the program and keep it running, watch the light show!

It is suggested to use VS Code, debug run settings have been created for various tasks.

Otherwise, CLI away!

# setup

## Development env

```sh
python -m virtualenv venv
source venv/bin/activate
pip install -e .
```

## Obtain hardware

These products were chosen because

- there is an active python module that supports access
- TP-Link has a good reputation as a manufacturer of network gear
- the design is good - for example the outlet is careful only to use one plug
- the price is reasonable
- no WiFi hub is required
- the brand seems to support, or at least is not trying to shut down, this kind of 'hobby' access to their products

Get a set of the following:

- 1 x TP-Link plug emeter - KP115(US) [[Kasa](https://www.kasasmart.com/us/products/smart-plugs/kasa-smart-plug-slim-energy-monitoring-kp115)][[Amazon](https://www.amazon.com/Kasa-Energy-Monitoring-Smart-Plug/dp/B08LN3C7WK)]

  This is a really nice plug that is compact and does not take up the other outlet in a standard US 2-outlet plate. It should cost around $20-30. WiFi enabled, no hub required.

- 1 x TP-Link smart light KL 125 | 130 [[Kasa](https://www.kasasmart.com/us/products/smart-lighting/kasa-smart-light-bulb-multicolor-kl130)]

  A multicolor, dimmable bulb. WiFi enabled, no hub required.

_Notes_:

- Bulb: have only used the 130. The 125 looks fine but try at your own risk; it seems the newer version, despite the lower model number, with slightly lower wattage. But again, it has not been confirmed to work.
- For the KP115 plug make sure it has the energy meter! Amazon et. al. seem to seel lower prices bundles of other versions (that can look similar)...
- HS300 power strip is not supported. While it is supposed to have an energy meter but the kasa-python library does not seem to support, or may need additional setup, and it is bulkier and more expensive than the smaller plug.

## Provision local access

Give the devices local wifi access.

Add devices to app

- Do not log in
- Do not update
- Skip
- Note for Google WiFi: adding to guest network not visible on main network

iOS app: https://apps.apple.com/us/app/kasa-smart/id1034035493

## Get IP address:

```sh
% kasa discover
Discovering devices on 255.255.255.255 for 3 seconds
== plug emeter - KP115(US) ==
        Host: 192.168.86.38
        Device state: ON

        == Generic information ==
        Time:         2021-05-27 15:15:27
        Hardware:     1.0
        Software:     1.0.7 Build 200825 Rel.100128
        MAC (rssi):   C0:C9:E3:0E:26:CA (-35)
        Location:     {'latitude': 3...7, 'longitude': -1.....5}

        == Device specific information ==
        LED state: True
        On since: 2021-05-27 15:06:03.631958


        == Current State ==
        {'current_ma': 2, 'voltage_mv': 121744, 'power_mw': 0, 'total_wh': 0, 'err_code': 0}
```

Confirm access by:

```sh
$ kasa --host 192.168.86.38 --plug led
LED state: True
```

## Set program flags

As in -b (bulb) and -p (plug) in
`python ./src/synesthesus/main.py -b 10.0.0.23 -p 10.0.0.22 -v `

# Contributing

Contributions are welcome. Please start by reading the material here, if there is still a question or problem, please post an issue to the repo: https://github.com/lifekaizen/synesthesus
