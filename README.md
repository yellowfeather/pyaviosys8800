pyaviosys8800
=============

Python USB driver for the [Aviosys USB Net Power 8800](http://www.aviosys.com/8800.html) switch.

With thanks to [Lance](http://raspberrypi.stackexchange.com/users/1237/lance) and [this](http://raspberrypi.stackexchange.com/a/1685/19199) answer on StackExchange.

## Dependencies:

[pyusb](http://walac.github.io/pyusb/)

pyusb is dependent on libusb.

## Installation:

To install libusb on Mac OS X using homebrew use:

    brew install libusb

## Testing:

There is a small test program that allows you to turn the switch on and off via the command line.

    git clone git@github.com:yellowfeather/pyaviosys8800.git
    cd pyaviosys8800
    python test.py
