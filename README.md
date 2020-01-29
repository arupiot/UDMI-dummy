# UDMI-dummy

If you need to simulate arbitrary telemetry data from a device that doesn't work yet, what do you do? Use this!

High level notes:  
  
- **Python 3**
- Designed for testing!
- Sends MQTT messages to a broker based on a [UDMI 'pointset'](https://github.com/faucetsdn/daq/blob/master/schemas/udmi/pointset.tests/example.json) configuration
- Control actuators (digital on/off) with config defined keyboard keys
- Generate random floating point data within a range
- Tries to be as Pythonic as possible (may fall short)
- Fork at will!
- **Definitely Python 3**

## Installation

Use a [venv](https://docs.python.org/3/library/venv.html) if you wish, either way:

```
$ pip install -r requirements.txt
```

## Usage

```
usage: run.py [-h] [--interface] [--config CONFIG] [--broker_host BROKER_HOST]
              [--broker_port BROKER_PORT]

optional arguments:
  -h, --help            show this help message and exit
  --interface, -i       For configurations with controllable points, launch
                        the 'interface'
  --config CONFIG, -c CONFIG
                        Path to the JSON config. If blank, revert to UDMIduino
                        format
  --broker_host BROKER_HOST, -bh BROKER_HOST
                        MQTT broker hostname string. If blank, set to
                        'localhost'
  --broker_port BROKER_PORT, -bp BROKER_PORT
                        MQTT broker TCP port. If blank, set to 3389
```

## Interface

The included interface has only been tested on a Debian-like terminal. It uses the [curses](https://docs.python.org/3/howto/curses.html) module included with most Python 3 distributions. [YMMV](https://lmgtfy.com/?q=python+3+curses+on+windows) on Windows 3.1/98/ME/7/8/10.

Launch the interface with:

```
$ python3 run.py -i
```

If the interface is not launched: 

- The curses module will not be loaded at all
- random messages will be sent to your broker anyway 
- Digital point values will stay fixed at 0

## Topic configuration

Looks like this:

```
...
"namespace" : "sursamen",
"device_name" : "DRONE-001",
...
```

The above configuration will send all messages on the topic:

```
sursamen/DRONE-001/events
```

## Pointset Configuration

Ridulous references from Iain M Banks' [Matter](https://en.wikipedia.org/wiki/Matter_(novel))  
  
See `./sample-config`, `./sample-ishiki.json` or `./sample-udmiduino-temp.json`. These examples will work as they are with, e.g.

```
$ python3 run.py --config ./sample-config.json
```

### Digital

Digital points have a value of either 0 or 100 and are toggled (between 0 and 100) by a single keyboard character defined in a JSON file. They look like this:

```
{
    "name" : "lum_value",
    "digital": "true",
    "keybinding": "l"
}
```

### Analogue

Analogue points are defined within a 'low' and 'high' range. Random floating point values are generated between these bounds. They look like this:

```
{
    "name" : "temp",
    "digital": "false",
    "analogue": {
        "high": 30,
        "low": 0
    }
}
```