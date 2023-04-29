![Tracert logo](https://mauricelambert.github.io/info/python/code/Tracert_small.png "Tracert logo")

# Tracert

## Description

This package implements a traceroute tool faster than traceroute/tracert executable but less accurate for response and without hostname resolution.

## Requirements

This package require :
 - python3
 - python3 Standard Library
 - Scapy
 - PythonToolsKit

## Installation

```bash
pip install Tracert
```

## Usages

### Command lines

```bash
python3 -m Tracert 8.8.8.8
python3 Tracert.pyz dns.google.com
Tracert 8.8.4.4
Tracert --help
Tracert -h
Tracert -6 -t 2 -r 5 -s 64 dns.google.com
```

### Python3

```python
from Tracert import tracert

tracert("8.8.8.8")
tracert("dns.google.com", 6, 64, 2, 5)
```

## Links

 - [Github Page](https://github.com/mauricelambert/Tracert)
 - [Pypi](https://pypi.org/project/Tracert/)
 - [Documentation](https://mauricelambert.github.io/info/python/code/Tracert.html)
 - [Executable](https://mauricelambert.github.io/info/python/code/Tracert.pyz)

## Help

```text
usage: traceroute.py [-h] [-4 | -6] [--timeout TIMEOUT] [--retry RETRY] [--max-steps MAX_STEPS] destination

Fast tracert tool.

positional arguments:
  destination           IP or hostname you want to trace.

options:
  -h, --help            show this help message and exit
  -4                    Force IPv4.
  -6                    Force IPv6.
  --timeout TIMEOUT, -t TIMEOUT
                        Timeout for each ping.
  --retry RETRY, -r RETRY
                        Number of retry for each steps.
  --max-steps MAX_STEPS, -s MAX_STEPS
                        Maximum steps to trace.
```

## Licence

Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
