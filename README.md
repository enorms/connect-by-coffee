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

## Examples

- electric kettle in your kitchen: plug => colored light in your office: bulb
- laundry machine: plug => (a different color) light in your office: bulb

## Feature roadmap:

- map across WiFi networks (currently works only one on local)

# setup

## Development env

```sh
python -m venv venv
source venv/bin/activate
pip install -e .
```

## Obtain hardware

### Get a set of one smart plug and one smart bulb:

- 1 x TP-Link plug emeter - KP115(US) [[Kasa](https://www.kasasmart.com/us/products/smart-plugs/kasa-smart-plug-slim-energy-monitoring-kp115)][[Amazon](https://www.amazon.com/Kasa-Energy-Monitoring-Smart-Plug/dp/B08LN3C7WK)]

  This is a really nice plug that is compact and does not take up the other outlet in a standard US 2-outlet plate. It should cost around $20-30. WiFi enabled, no hub required.

- 1 x TP-Link smart light KL 125 | 130 [[Kasa](https://www.kasasmart.com/us/products/smart-lighting/kasa-smart-light-bulb-multicolor-kl130)][[Amazon](https://www.amazon.com/gp/product/B07FZ6PLJG/ref=ppx_yo_dt_b_asin_title_o00_s00)]

  A multicolor, dimmable bulb, about $15. WiFi enabled, no hub required.

_Confirmed working_:

- KL130
- KP115

_Notes_:

- KL125 bulb: did not work. Seems like it should, and there are reports in HomeAssistant, but has not been confirmed with this software so try at your own risk; KL130 is recommended for now. Note that price is within a few $ at time of writing.
- For the KP115 plug make sure it has the energy meter! Amazon et. al. seem to seel lower prices bundles of other versions (that can look similar)...
- HS300 power strip is not supported. While it is supposed to have an energy meter but the kasa-python library does not seem to support, or may need additional setup, and it is bulkier and more expensive than the smaller plug.

_These products were chosen because:_

- there is an active python module that supports access
- TP-Link has a good reputation as a manufacturer of network gear
- the design is good - for example the outlet is careful only to use one plug
- the price is reasonable
- no WiFi hub is required
- the brand seems to support, or at least is not trying to shut down, this kind of 'hobby' access to their products

## Provision local access

Give the devices local WiFi access using she Kasa smartphone app.

- iOS app: https://apps.apple.com/us/app/kasa-smart/id1034035493

Follow the app flow to add devices with the following choices:

- Do not update firmware!
  - choose 'skip'
  - or close the app, if asked after connection success
  - because this may lead to being unable to access the device [[example](https://www.reddit.com/r/TPLinkKasa/comments/k26v9l/psa_tp_link_is_shutting_down_local_api_access/)]
- Do not log in; an account is not needed, unless you really really want one

Notes on using guest WiFi:

- on Google WiFi: adding to guest network not visible on main network
- if the devices are kept local only, this should not matter much for security

## Get device IP addresses:

Using the python module kasa. Success looks like:

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

Note the IP address, in this case `192.168.86.38`. You can confirm this by:

```sh
$ kasa --host 192.168.86.38 --plug led
LED state: True
```

## Run program

Set the IP addresses for the device, as in -b (bulb) and -p (plug), and then go

`python ./src/synesthesus/main.py -b 10.0.0.23 -p 10.0.0.22 -v `

# Contributing

Contributions are welcome. Please start by reading the material here, if there is still a question or problem, please post an issue to the repo: https://github.com/lifekaizen/synesthesus

# Troubleshooting

If you don't see the device appear with `% kasa`, check that they show properly in your smartphone app. If they do, try again.

Cannot discover devices. Are you scanning the same WiFi network the devices are on? Check Network settings then use `--target` flag. Example: Network > Wi-Fi > 192.168.87.46: kasa --target 192.168.87.255 discover: does discover KP115.
