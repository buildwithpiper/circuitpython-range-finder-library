# The MIT License (MIT)
#
# Copyright (c) 2017 Mike Mabey
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`piper_range_finder`
====================================================

A CircuitPython library for the Grove ultrasonic range sensor.
Based on the CircuitPython library for the HC-SR04 ultrasonic range sensor.

The HC-SR04 functions by sending an ultrasonic signal, which is reflected by
many materials, and then sensing when the signal returns to the sensor. Knowing
that sound travels through dry air at `343.2 meters per second (at 20 °C)
<https://en.wikipedia.org/wiki/Speed_of_sound>`_, it's pretty straightforward
to calculate how far away the object is by timing how long the signal took to
go round-trip and do some simple arithmetic, which is handled for you by this
library.

* Original authors:

  - Mike Mabey
  - Jerry Needell - modified to add timeout while waiting for echo (2/26/2018)
  - ladyada - compatible with `distance` property standard, renaming, Pi compat
"""

import time
from pulseio import PulseIn

__version__ = "1.0.0"
__repo__ = "https://github.com/buildwithpiper/circuitpython-range-finder-library.git"


class GroveUltrasonicRanger:
	def __init__(self, sig_pin, unit=1.0, timeout=1.0):
		self.unit = unit
		self.timeout = timeout

		self.echo = PulseIn(sig_pin)
		self.echo.pause()
		self.echo.clear()

	def __enter__(self):
		"""Allows for use in context managers."""
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		"""Automatically de-initialize after a context manager."""
		self.deinit()

	def deinit(self):
		"""De-initialize the sig pin."""
		self.echo.deinit()

	def dist_two_wire(self):
		self.echo.clear()  # Discard any previous pulse values
		time.sleep(0.00001)  # 10 micro seconds 10/1000/1000
		timeout = time.monotonic()
		self.echo.resume(20)
		while len(self.echo) == 0:
			# Wait for a pulse
			if (time.monotonic() - timeout) > self.timeout:
				self.echo.pause()
				return -1
		self.echo.pause()
		if self.echo[0] == 65535:
			return -1

		return (self.echo[0] / 2) / (291 / 10)

	def distance(self):
		return self.dist_two_wire()
