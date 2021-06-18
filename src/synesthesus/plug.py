"""
Set host to correct IP address for desired device.

Devices that are confirmed to support Consumption Reading;
  HS110 - old circular
  HS300 - strip 6 + 3 USB (~$55)
  KP115 - new slim square shape (~$25)
  source: https://www.home-assistant.io/integrations/tplink/

HS105: works for power, no energy

Reference
# https://python-kasa.readthedocs.io/en/latest/smartplug.html
# https://community.home-assistant.io/t/installing-hass-on-macos-osx/69292/3


"""
import asyncio, atexit, sys, time
from typing import Any, Dict
from kasa import SmartPlug, SmartDeviceException # type: ignore
from synesthesus.utility import parse_args


class Plug:
    """
    Encapsulate the async commands into one simpler commands

    Call from a main function using asyncio.run(function())

    Typical use:
        plug = plug()
        await plug.update_state()

    host: get from kasa discover

    """

    def __init__(self, host: str, verbose: int = 0) -> None:
        """Does not update state since async"""
        assert "." in host
        self.plug = SmartPlug(host)
        self._state = Dict[Any, Any]

    async def update_state(self: Any, verbose: int = 0) -> dict:
        """Use like
        print(await plug.state())

        note: 'led_on' does not seem accurate with HS105"""
        keys_to_monitor = [
            "has_emeter",
            "is_on",
            "state_information",
            "host",
            "is_plug",
            "led",
            "model",  # KP115(US)
            "rssi",
            "device_id",
        ]
        try:
            await self.plug.update()
            assert self.plug.is_plug
            try:
                assert "KL130" not in self.plug.model  # this is a bulb
            except AssertionError as e:
                print(e)
        except [
            AssertionError,
            ConnectionResetError,
            SmartDeviceException, # type: ignore
            TypeError,
        ] as e:
            sys.exit(["exiting"])

        try:
            for key in keys_to_monitor:
                self._state.update({key: getattr(self.plug, key)})
        except KeyError as e:
            sys.exit("KeyError, exiting. Is this the host to the correct device?")
        if self._state.get("has_emeter") == True:
            self.REALTIME_POWER_MW_MIN = 0
            self.REALTIME_POWER_MW_MAX = 0
            if "KP115" in self._state.get("model"):
                # https://www.kasasmart.com/us/products/smart-plugs/kasa-smart-plug-slim-energy-monitoring-kp115
                # Maximum Load: 15 A, 1.8 KW for 120 V
                self.REALTIME_POWER_MW_MAX = 1.8 * 1000 * (10 ** 6)
            self._state.update(
                {
                    "emeter_realtime_current_ma": self.plug.emeter_realtime.get(
                        "current_ma"
                    )
                }
            )
            self._state.update(
                {
                    "emeter_realtime_voltage_mv": self.plug.emeter_realtime.get(
                        "voltage_mv"
                    )
                }
            )
            self._state.update(
                {"emeter_realtime_power_mw": self.plug.emeter_realtime.get("power_mw")}
            )
        return self._state

    async def led_off(
        self: Any,
        verbose: int = 0,
    ) -> bool:
        """
        Returns value of led state
        """
        await self.plug.set_led(True)
        await self.state()
        return self.plug.led

    async def led_on(self: Any, verbose: int = 0) -> bool:
        await self.plug.set_led(False)
        await self.plug.update_state()
        return self.plug.led

    async def on(self: Any, verbose: int = 0) -> bool:
        """
        Turn on and return true if on
        """
        if await self.is_on():
            if verbose > 0:
                print("[Plug] already on")
            return True
        await self.plug.turn_on()
        if verbose > 0:
            print("[Plug] did turn on")
        return await self.is_on()

    async def off(self: Any, verbose: int = 0) -> bool:
        """
        Turns off and return true if off
        """
        if await self.is_off():
            if verbose > 0:
                print("[Plug] already off")
            return True
        await self.plug.turn_off()
        if verbose > 0:
            print("[Plug] did turn off")
        return await self.is_off()

    async def is_on(self: Any, verbose: int = 0) -> bool:
        """Returns value of power state"""
        await self.update_state()
        if verbose > 0:
            print("[Plug] is_on:", self.plug.is_on)
        return self.plug.is_on

    async def is_off(self: Any, verbose: int = 0) -> bool:
        """Returns value of power state"""
        await self.update_state()
        if verbose > 0:
            print("[Plug] is_off:", not self.plug.is_on)
        return not self.plug.is_on

    async def get_power(self: Any, verbose: int = 0) -> int:
        """returns emeter_realtime_power_mw"""
        await self.update_state()
        if verbose > 0:
            print(
                "[Plug] realtime_power mw:",
                f'{self._state.get("emeter_realtime_power_mw"):,}',
                ",",
                "ma:",
                f'{self._state.get("emeter_realtime_current_ma"):,}',
            )

        return self._state.get("emeter_realtime_power_mw")


async def _test_setup(verbose, host_plug):
    plug = Plug(verbose=verbose, host=host_plug)
    atexit.register(lambda: asyncio.get_event_loop().run_until_complete(plug.off()))
    assert type(plug) == Plug
    await plug.update_state(verbose)
    is_on = await plug.is_on(verbose)
    is_off = await plug.is_off(verbose)
    assert is_on or is_off
    return plug


async def _test_power_cycle(plug, verbose):
    print("[Plug - Test] turn off. expect: True, actual:", await plug.off(verbose))
    await asyncio.sleep(1)
    print("[Plug - Test] turn on. expect: True, actual:", await plug.on(verbose))
    return await asyncio.sleep(5)


async def test(verbose: int, host_plug: str) -> None:
    plug = await _test_setup(verbose, host_plug)
    await _test_power_cycle(plug, verbose)


async def main(verbose, host_plug):
    pass


if __name__ == "__main__":
    args = parse_args(prog="plug", argv=sys.argv)
    verbose = args.__getattribute__("VERBOSE")
    is_program_test = args.__getattribute__("TEST")
    host_plug = args.__getattribute__("PLUG_HOST")

    if is_program_test:
        if verbose > 0:
            print("[Plug] run test with verbose")
        asyncio.get_event_loop().run_until_complete(
            test(verbose=verbose, host_plug=host_plug)
        )
    else:
        if verbose > 1:
            print("[Plug] run main with info")
        elif verbose > 0:
            print("[Plug] run main with verbose")
        else:
            pass  # print nothing
        asyncio.get_event_loop().run_until_complete(
            main(verbose=verbose, host_plug=host_plug)
        )
