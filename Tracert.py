#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This package implements a traceroute tool faster than traceroute/tracert
#    executable but less accurate for response and without hostname resolution.
#    Copyright (C) 2023  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""
This package implements a traceroute tool faster than traceroute/tracert
executable but less accurate for response and without hostname resolution.
"""

__version__ = "0.0.1"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = """
This package implements a traceroute tool faster than traceroute/tracert
executable but less accurate for response.
"""
license = "GPL-3.0 License"
__url__ = "https://github.com/mauricelambert/Tracert"

copyright = """
Tracert  Copyright (C) 2023  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
__license__ = license
__copyright__ = copyright

__all__ = ["tracert", "Ping"]

print(copyright)

from scapy.all import IP, IPv6, ICMP, ICMPv6EchoRequest, sr1, conf
from socket import getaddrinfo, AF_INET, AF_INET6, gethostbyname
from PythonToolsKit.ScapyTools import get_gateway_route
from ipaddress import ip_address, IPv4Address
from argparse import ArgumentParser
from dataclasses import dataclass
from time import perf_counter
from typing import Iterable
from sys import stderr


@dataclass
class Ping:
    ip: str
    ttl: int
    time: float

    def __str__(self):
        return f"""{self.ttl:<6} {
                (str(round(self.time, ndigits=3) * 1000) + ' ms').ljust(9)
            } {self.ip}"""


def tracert(
    destination: str,
    version: int = None,
    max_steps: int = 30,
    timeout: float = 1,
    retry: int = 3,
) -> Iterable[Ping]:
    """
    This generator sends traceroute packets
    and yields Ping object built from the response.

    version: should be 4 for IPv4 packets or 6 for IPv6 packets.
    """

    iface = get_gateway_route()
    iface = iface.interface or conf.iface

    if version:
        inet, layer2, layer3, ttl_name = (
            (AF_INET, IP, ICMP, "ttl")
            if version == 4
            else (AF_INET6, IPv6, ICMPv6EchoRequest, "hlim")
        )
        ip = getaddrinfo(destination, None, inet)[0][4][0]
    else:
        ip = gethostbyname(destination)
        inet, layer2, layer3, ttl_name = (
            (AF_INET, IP, ICMP, "ttl")
            if isinstance(ip_address(ip), IPv4Address)
            else (AF_INET6, IPv6, ICMPv6EchoRequest, "hlim")
        )

    ip_response: str = None
    counter = 0

    while ip_response != ip:
        if max_steps < counter:
            print("The maximum number of steps is exceeded.", file=stderr)
            return None

        counter += 1
        ttl = {ttl_name: counter}
        ping = layer2(dst=ip, **ttl) / layer3()
        for _ in range(retry):
            start = perf_counter()
            reply = sr1(ping, timeout=timeout, verbose=0, iface=iface)
            end = perf_counter()
            if reply:
                break
        else:
            yield Ping("*", counter, 0)
            continue

        ip_response = reply[layer2].src
        yield Ping(ip_response, counter, end - start)


def main() -> int:
    """
    This function starts the tracert tool from the command line.
    """

    parser = ArgumentParser(description="Fast tracert tool.")
    add_argument = parser.add_argument
    version = parser.add_mutually_exclusive_group()
    version.add_argument("-4", action="store_true", help="Force IPv4.")
    version.add_argument("-6", action="store_true", help="Force IPv6.")
    add_argument(
        "--timeout", "-t", default=1, type=float, help="Timeout for each ping."
    )
    add_argument(
        "--retry",
        "-r",
        default=3,
        type=int,
        help="Number of retry for each steps.",
    )
    add_argument(
        "--max-steps",
        "-s",
        default=30,
        type=int,
        help="Maximum steps to trace.",
    )
    add_argument("destination", help="IP or hostname you want to trace.")
    arguments = parser.parse_args()

    if getattr(arguments, "6"):
        version = 6
    elif getattr(arguments, "4"):
        version = 4
    else:
        version = None

    tuple(
        print(x)
        for x in tracert(
            arguments.destination,
            version,
            arguments.max_steps,
            arguments.timeout,
            arguments.retry,
        )
    )

    return 0

if __name__ == "__main__":
    exit(main())