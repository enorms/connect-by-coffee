import argparse
import asyncio
from kasa import Discover


def parse_args(prog: str, argv: list) -> any:
    """Verbose will be determined here"""
    parser = argparse.ArgumentParser(prog)
    parser.add_argument(
        "-t", "--test", action="store_true", dest="TEST", help="run test program"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        const=1,
        dest="VERBOSE",
        help="use verbose mode",
    )
    parser.add_argument(
        "-i",
        "--info",
        action="store_const",
        const=2,
        dest="VERBOSE",
        help="use info (> verbose) mode",
    )
    if prog == "main" or prog == "bulb":
        parser.add_argument(
            "-b",
            "--bulb",
            required=True,
            dest="BULB_HOST",
            help="host ip address for bulb (i.e. 192.168.86.35)",
            metavar="",
        )
    if prog == "main" or prog == "plug":
        parser.add_argument(
            "-p",
            "--plug",
            required=True,
            dest="PLUG_HOST",
            help="host ip address for plug (i.e. 192.168.86.35)",
            metavar="",
        )
    if ".py" in str(argv):
        argv = argv[1:]
    args = parser.parse_args([arg.lower() for arg in argv])
    if not args.__getattribute__("VERBOSE"):
        args.__setattr__("VERBOSE", 0)
    if args.__getattribute__("VERBOSE") > 0:
        print("[Utility] args:", args)
    return args


async def discover_devices(verbose: int = 1) -> dict:
    to_return = dict()
    if verbose > 0:
        print("Discovering devices....may take a few seconds....")
    devices = await Discover.discover()
    for addr, dev in devices.items():
        await dev.update()
        dev_type = dev.__getattribute__("device_type").__getattribute__("name")
        if verbose > 0:
            print(addr, dev_type)
        to_return.update({addr: dev_type})
    return to_return


async def main(verbose):
    """Script to get and print devices and types."""
    devices = await discover_devices(verbose)


if __name__ == "__main__":
    verbose = 1
    asyncio.get_event_loop().run_until_complete((main(verbose)))
