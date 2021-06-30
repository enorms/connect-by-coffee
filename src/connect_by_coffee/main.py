"""
Connect and subscribe to a plug, and use that to control the brightness for a color

CLI options:
    -t run test program
    -v verbose printouts
"""
__author__ = "Eric Norman"
__copyright__ = "Eric Norman"
__license__ = "None"

import argparse
import logging
import sys
from typing import Any
import asyncio, argparse, atexit, sys, time
from connect_by_coffee.bulb import Bulb, HSV
from connect_by_coffee.plug import Plug
from connect_by_coffee.utility import parse_args
from connect_by_coffee.globals import HSV, HUE, SATURATION, VALUE
from connect_by_coffee import __version__

_logger = logging.getLogger(__name__)

SHORT_TRANSITION = 2000  # ms


async def _test_setup(verbose):
    pass


async def _test_teardown(plug, verbose):
    pass


async def test(verbose):
    plug = await _test_setup(verbose)

    # run test

    await _test_teardown(plug, verbose)


async def setup_plug(plug: Plug, verbose: int = 0):
    await plug.on(verbose)


async def setup_bulb(bulb: Bulb, color: str = "BLUE", verbose: int = 0) -> None:
    """Color could be used to distinguish people or actions
    str color: must be known to HSV dictionary"""
    assert color in HSV
    await bulb.off(transition=SHORT_TRANSITION)
    await asyncio.sleep(SHORT_TRANSITION / 1000)
    hue: int = HSV.get(color, {}).get(HUE, 0)
    saturation: int = HSV.get(color, {}).get(SATURATION, 0)
    value: int = HSV.get(color, {}).get(VALUE, 0)
    await bulb.set_hsv(
        hue=hue, saturation=saturation, value=value, transition=SHORT_TRANSITION
    )
    await asyncio.sleep(SHORT_TRANSITION / 1000)
    await bulb.set_hsv(
        hue=hue, saturation=saturation, value=value, transition=SHORT_TRANSITION
    )
    await asyncio.sleep(SHORT_TRANSITION / 1000)
    hue, value = 0, 0
    await bulb.set_hsv(
        hue=hue, saturation=saturation, value=value, transition=SHORT_TRANSITION
    )
    await asyncio.sleep(SHORT_TRANSITION / 1000)
    await bulb.off(transition=SHORT_TRANSITION)
    await asyncio.sleep(SHORT_TRANSITION / 1000)


def map_power_to_brightness(power_mw, verbose=0):
    """
    int power: power_mw

    note:
        US circuits 1.8 kw but regulation usually limits to 1.5 kw
            that is for std 15A, some kitchens have 20A but not used individually
        kw = mw * 10^6
        max_mw observed iPad Pro 12.9": 20_000
        max_mw observed: Oxo kettle: 1_417_154
    """
    ACTUAL_POWER_MAX_MW = 1.8 * 10 ** 6
    EXPECTED_MAX_POWER_MW = 1.5 * 10 ** 6
    assert 0 <= power_mw <= ACTUAL_POWER_MAX_MW
    POWER_MIN, POWER_MAX = 0, EXPECTED_MAX_POWER_MW
    BRIGHTNESS_MIN, BRIGHTNESS_MAX = 0, 100
    brightness = min(
        round(power_mw / EXPECTED_MAX_POWER_MW * BRIGHTNESS_MAX), BRIGHTNESS_MAX
    )
    if verbose > 1:
        print(
            "[Main] map power -> brightness:",
            power_mw,
            "/",
            EXPECTED_MAX_POWER_MW,
            "->",
            brightness,
            "/",
            BRIGHTNESS_MAX,
        )
    elif verbose > 0:
        print(
            "[Main] map power:",
            round(power_mw / EXPECTED_MAX_POWER_MW * BRIGHTNESS_MAX),
            "% -> brightness",
            round(brightness),
            "%",
        )
    return brightness


async def _setup_devices(host_bulb, host_plug, color="BLUE", verbose=0) -> Any:
    """Return devices"""
    plug = Plug(verbose=verbose, host=host_plug)
    await setup_plug(plug=plug, verbose=verbose)
    bulb = Bulb(verbose=verbose, host=host_bulb)
    await setup_bulb(bulb=bulb, color=color, verbose=verbose)
    atexit.register(lambda: asyncio.get_event_loop().run_until_complete(bulb.off()))
    atexit.register(lambda: asyncio.get_event_loop().run_until_complete(plug.off()))
    return {"plug": plug, "bulb": bulb}


# TODO: thread this
async def _main_loop(bulb, plug, color="BLUE", verbose=0):
    power = 0
    timer = time.time()
    while await plug.is_on():  # end if turned off
        new_power = await plug.get_power(verbose)
        MIN_WAIT_BETWEEN_UPDATES = 1  # seconds
        if time.time() > MIN_WAIT_BETWEEN_UPDATES + timer and new_power != power:
            if verbose > 0:
                print(
                    "[Main] new power:",
                    f"{new_power:,}",
                    "mw (",
                    f"{new_power - power:,}",
                    "), interval",
                    f"{round(time.time() - timer):,}",
                    "s",
                )
            power = new_power
            timer = time.time()
            brightness = map_power_to_brightness(power_mw=power, verbose=verbose)
            if brightness == 0:
                await bulb.off(transition=SHORT_TRANSITION)
            else:
                await bulb.on(transition=SHORT_TRANSITION)
                await bulb.set_brightness(
                    brightness=brightness, transition=SHORT_TRANSITION
                )
        await asyncio.sleep(MIN_WAIT_BETWEEN_UPDATES)


async def main(host_bulb, host_plug, color="BLUE", verbose=0):
    """Map one plug energy usage to one bulb.

    Exit if plug is turned off or connection is lost a device.

    Upon exit, turn off plug and light.

    int verbose: 1 prints events console, 2 prints adds streaming (can be a lot!)
    str BULB_HOST: easiest way to find is `kasa discover`
    str PLUG_HOST: easiest way to find is `kasa discover`
    str color: must be known color in HSV dictionary
    """
    color = "BLUE"  # optional override
    assert host_bulb and host_plug
    assert color in HSV

    devices = await _setup_devices(
        host_bulb=host_bulb, host_plug=host_plug, color=color, verbose=verbose
    )
    plug, bulb = devices.get("plug"), devices.get("bulb")

    await _main_loop(bulb=bulb, plug=plug, color=color, verbose=verbose)
    sys.exit()


if __name__ == "__main__":
    args = parse_args(prog="main", argv=sys.argv)
    verbose = args.__getattribute__("VERBOSE")
    is_program_test = args.__getattribute__("TEST")
    host_bulb = args.__getattribute__("BULB_HOST")
    host_plug = args.__getattribute__("PLUG_HOST")

    if is_program_test:
        if verbose > 0:
            print("[Main] run test with verbose")
        asyncio.run(test(verbose))
    else:
        if verbose > 1:
            print("[Main] run main with info")
        elif verbose > 0:
            print("[Main] run main with verbose")
        else:
            pass
        asyncio.get_event_loop().run_until_complete(
            (main(verbose=verbose, host_bulb=host_bulb, host_plug=host_plug))
        )
