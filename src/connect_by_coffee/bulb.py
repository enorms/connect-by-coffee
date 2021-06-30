"""


"""
import asyncio, atexit, sys
from pprint import pprint
from typing import Any, Dict, Optional
from kasa import SmartBulb, SmartDeviceException # type: ignore
from connect-by-coffee.utility import parse_args
from connect-by-coffee.globals import HSV, HUE, SATURATION, VALUE

DEFAULT_TRANSITION = 10_000

class Bulb:
    """
    Encapsulate the async commands into one simpler commands

    Call from a main function using asyncio.run(function())

    host: get from kasa discover
    verbose: set at init

    """

    def __init__(self, host: str, verbose: int = 0) -> None:
        assert "." in host
        self.bulb: Any = SmartBulb(host)
        self._state = dict[Any, Any]()
        self.verbose: int = verbose
        if self.verbose > 0:
            print("[Bulb] did init")

    async def update_state(self: Any) -> None:
        """Must be run before some commands (like set_hsv())"""
        await self.bulb.update()
        for k, v in self.bulb.state_information.items():
            self._state[k] = v
        self._state["is_on"] = self.bulb.is_on
        self._state["is_color"] = self.bulb.is_color
        self._state["has_emeter"] = self.bulb.has_emeter
        if self.verbose > 1:
            print("[Bulb] did update state")

    async def is_off(self: Any) -> bool:
        """Update state and return true if *not* on"""
        await self.update_state()
        return not self._state.get("is_on")

    async def is_on(self: Any) -> bool:
        """Update state and return true if on"""
        await self.update_state()
        return self._state.get("is_on")

    async def off(self: Any, transition: int = DEFAULT_TRANSITION) -> bool:
        """
        Turn off and return true if off

        int transition: transition in milliseconds

        Note: in theory takes optional int transition ms
            but fails saying 1 too many arguments
        """
        if await self.is_off():
            if self.verbose > 0:
                print("[Bulb] already off")
            return True
        await self.bulb.turn_off(transition=transition)
        if self.verbose > 0:
            print("[Bulb] did turn off")
        return await self.is_off()

    async def on(self: Any, transition: int = DEFAULT_TRANSITION) -> bool:
        """
        Turn on and return true if on.
        Safe to call without knowing current state.

        Use set_hsv() to change.
        """
        if await self.is_on():
            if self.verbose > 0:
                print("[Bulb] already on")
            return True
        await self.bulb.turn_on(transition=transition)
        if self.verbose > 0:
            print("[Bulb] did turn on")
        return await self.is_on()

    async def set_brightness(
        self: Any, brightness: int, transition: int = DEFAULT_TRANSITION
    ) -> None:
        """Set brightness and returns dict.
        Assumes color has been set prior

        int brightness: brightness in percent
        int transition: time in ms"""
        assert 0 <= brightness <= 100
        await self.bulb.set_brightness(brightness, transition=transition)
        if self.verbose > 0:
            print("[Bulb] did set brightness to", brightness)

    async def set_hsv(
        self,
        hue: int,
        saturation: int,
        value: int,
        transition: int = DEFAULT_TRANSITION,
    ) -> None:
        """Set hsv and return dict.

        int hue: hue in percent
        int saturation: saturation in percent
        int value: brightness in percent
        int transition: time in ms"""
        assert 0 <= hue <= 360
        assert 0 <= saturation <= 100
        assert 0 <= value <= 100
        # await self.update_state()
        try:
            result = await self.bulb.set_hsv(
                hue, saturation, value, transition=transition
            )
        except SmartDeviceException as e:
            if self.verbose > 0:
                print(
                    "[Bulb] handling SmartDeviceException in set_hsv() by running update_state()"
                )
            await self.update_state()
            result = await self.bulb.set_hsv(
                hue, saturation, value, transition=transition
            )
        if self.verbose > 0:
            print("[Bulb] did set hsv to", hue, saturation, value)


async def _test_setup(verbose: int, host_bulb: str) -> Bulb:
    """Setup with red and leave in off state"""
    bulb = Bulb(verbose=verbose, host=host_bulb)
    atexit.register(lambda: asyncio.get_event_loop().run_until_complete(bulb.off()))
    assert type(bulb) == Bulb
    await bulb.update_state()
    is_on = await bulb.is_on()
    is_off = await bulb.is_off()
    assert is_on or is_off
    await bulb.off(transition=DEFAULT_TRANSITION)
    return bulb


async def _test_hsv(bulb: Bulb, color: str = "BLUE", verbose: int = 0) -> None:
    """Test for values of known color
    Fails for unknown color string

    str color: must be known to HSV dictionary"""
    assert color in HSV
    hue: int = HSV.get(color, {}).get(HUE, 0)
    saturation: int = HSV.get(color, {}).get(SATURATION, 0)
    value = 0
    transition = 10_000
    await bulb.set_hsv(hue, saturation, value, transition)


async def _test_brightness(bulb: Bulb, verbose: int = 0) -> None:
    """Assumes plugged in but off
    and color or hsv is already set up"""
    await bulb.on()
    brightness, transition = 100, 5_000
    if verbose > 0:
        print("set brightness to", brightness, "over", transition / 1000, "s")
    await bulb.set_brightness(brightness, transition)
    await asyncio.sleep(transition / 1000)

    brightness, transition = 0, 5_000
    if verbose > 0:
        print("set brightness to", brightness, "over", transition / 1000, "ms")
    await bulb.set_brightness(brightness, transition)
    await asyncio.sleep(transition / 1000)


async def _test(verbose: int, host_bulb: str):
    """Power cycle, end program in off state"""
    # setup
    bulb = await _test_setup(verbose=verbose, host_bulb=host_bulb)
    print("[Bulb - Test] turn off. expect: True, actual:", await bulb.off(transition=0))
    print("[Bulb - Test] turn on. expect: True, actual:", await bulb.on(transition=0))

    # await _test_hsv(bulb, color = "RED")
    await _test_brightness(bulb=bulb, verbose=verbose)


async def main(verbose: int, host_bulb: str) -> None:
    pass


if __name__ == "__main__":
    args = parse_args(prog="bulb", argv=sys.argv)
    verbose = args.__getattribute__("VERBOSE")
    is_program_test = args.__getattribute__("TEST")
    host_bulb = args.__getattribute__("BULB_HOST")

    if is_program_test:
        if verbose > 0:
            print("[Bulb] run test with verbose")
        asyncio.get_event_loop().run_until_complete(
            _test(verbose=verbose, host_bulb=host_bulb)
        )
    else:
        if verbose > 1:
            print("[Bulb] run main with info")
        elif verbose > 0:
            print("[Bulb] run main with verbose")
        else:
            pass  # print nothing
        asyncio.get_event_loop().run_until_complete(
            main(verbose=verbose, host_bulb=host_bulb)
        )
