# Copyright (C) 2019 Analog Devices, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#     - Neither the name of Analog Devices, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#     - The use of this software may or may not infringe the patent rights
#       of one or more patent holders.  This license does not release you
#       from the requirement that you obtain separate licenses from these
#       patent holders to use this software.
#     - Use of the software either in source or binary form, must be run
#       on or directly connected to an Analog Devices Inc. component.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT, MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED.
#
# IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, INTELLECTUAL PROPERTY
# RIGHTS, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import numpy as np
from adi.attribute import attribute
from adi.context_manager import context_manager


class ad7746(attribute, context_manager):
    """AD7746 24-Bit Capacitance-to-Digital Converter"""

    _device_name = "ad7746"
    _capacitance_channels = [
        {"1+": "capacitance0"},
        {"2+": "capacitance1"},
        {"1": "capacitance0-capacitance2"},
        {"2": "capacitance1-capacitance3"},
    ]
    capacitance = []  # type: ignore

    def __init__(self, uri=""):
        context_manager.__init__(self, uri, self._device_name)
        self._ctrl = self._ctx.find_device(self._device_name)
        for key, value in self._capacitance_channels.items:
            self.capacitance[key] = self._cap_channel(self._ctrl, value)

    @property
    def vin_raw(self):
        """ AD7746 raw vin value """
        return self._get_iio_attr("voltage0", "raw", False)

    @property
    def vin_sample_rate(self):
        """ sample_rate: Sample rate for the VIN channel """
        return self._get_iio_attr("voltage0", "sampling_frequency", False)

    @vin_sample_rate.setter
    def vin_sample_rate(self, rate):
        try:
            self._set_iio_attr("voltage0", "sampling_frequency", False, rate)
        except Exception as error:
            return error

    @property
    def vin_scale(self):
        """ AD7746 VIN scale """
        return float(self._get_iio_attr_str("voltage0", "scale", False))

    @property
    def supply_raw(self):
        """AD7746 Voltage supply raw value"""
        return self._get_iio_attr("voltage1", "supply_raw", False)

    @property
    def supply_sample_rate(self):
        """ sample_rate: Sample rate for the Voltage supply channel """
        return self._get_iio_attr("voltage1", "sampling_frequency", False)

    @supply_sample_rate.setter
    def supply_sample_rate(self, rate):
        try:
            self._set_iio_attr("voltage1", "sampling_frequency", False, rate)
        except Exception as error:
            return error

    @property
    def supply_scale(self):
        """ AD7746 Voltage supply scale """
        return float(self._get_iio_attr_str("voltage1", "scale", False))

    @property
    def temp_internal(self):
        """ AD7746 Internal Temperature Sensor reading in millidegrees Celsius """
        self._get_iio_attr("temp0", "input", False)

    @property
    def temp_external(self):
        """ AD7746 External Temperature Sensor reading in millidegrees Celsius """
        self._get_iio_attr("temp1", "input", False)

    class _cap_channel(attribute):
        def __init__(self, ctrl, channel_name):
            self.name = channel_name
            self._ctrl = ctrl

        @property
        def raw(self):
            """ AD7747 capacitance channel raw value """
            return self._get_iio_attr(self.name, "raw", False)

        @property
        def sample_rate(self):
            """ AD7746 capacitance channel sampling frequency """
            return self._get_iio_attr(self.name, "sampling_frequency", False)

        @sample_rate.setter
        def sample_rate(self, rate):
            try:
                self._set_iio_attr(self.name, "sampling_frequency", False, rate)
            except Exception as error:
                return error

        @property
        def sample_rate_available(self):
            """ AD7746 available sampling frequencies.
            Returns the available sampling frequencies """
            available = [91, 84, 50, 26, 16, 13, 11, 9]
            return available

        @property
        def calibbias(self):
            """ AD7746 channel calibration bias """
            return self._get_iio_attr(self.name, "calibbias", False)

        def calibbias_calibration(self):
            """ Calibrate calibbias value """
            self._set_iio_attr(self.name, "calibbias", False, 1)

        @property
        def calibscale(self):
            """ AD7746 channel calibration scale """
            return self._get_iio_attr(self.name, "calibscale", False)

        def calibscale_calibration(self):
            """ Calibrate calibscale value """
            self._set_iio_attr(self.name, "calibscale", False, 1)

        @property
        def offset(self):
            """ offset: Read and write AD7746 capacitance channel offset """
            return self._get_iio_attr(self.name, "offset", False)

        @offset.setter
        def offset(self, value):
            offset_val = value / self.scale
            self._set_iio_attr(self.name, "offset", False, offset_val)

        @property
        def scale(self):
            """ AD7746 capacitance channel scale """
            return float(self._get_iio_attr_str(self.name, "scale", False))
