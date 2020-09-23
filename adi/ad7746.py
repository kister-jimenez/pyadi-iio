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
from adi.context_manager import context_manager
from adi.rx_tx import rx


class ad7746(rx, context_manager):
    """AD7746 24-Bit Capacitance-to-Digital Converter"""

    _device_name = "ad7746"
    _rx_channel_names = ["voltage0", "voltage1"]

    def __init__(self, uri=""):
        context_manager.__init__(self, uri, self._device_name)
        self._rxadc = self._ctx.find_device("ad7746")
        rx.__init__(self)

    @property
    def raw_volt0(self):
        """AD7746 channel raw value"""
        return self._get_iio_attr("voltage0", "raw", False)

    @property
    def sampling_frequency_available(self):
        """sampling_frequency_available: AD7746 available sampling frequencies.
        Returns the available sampling frequencies"""
        available = [91, 84, 50, 26, 16, 13, 11, 9]
        return available

    @property
    def sampling_frequency_volt0(self):
        """sample_rate: Sample rate RX and TX paths in samples per second of
        second transceiver"""
        return self._get_iio_attr("voltage0", "sampling_frequency", False)

    @sampling_frequency_volt0.setter
    def sampling_frequency_volt0(self, rate):
        frequencies = self.sampling_frequency_available
        try:
            if rate in frequencies:
                self._set_iio_attr("voltage0", "sampling_frequency", False, rate)
        except Exception as error:
            return error

    @property
    def scale_volt0(self):
        """AD7746 channel scale(gain)"""
        return float(self._get_iio_attr_str("voltage0", "scale", False))

    @property
    def sampling_frequency_volt1(self):
        """sample_rate: Sample rate RX and TX paths in samples per second of
        second transceiver"""
        return self._get_iio_attr("voltage1", "sampling_frequency", False)

    @sampling_frequency_volt1.setter
    def sampling_frequency_volt1(self, rate):
        frequencies = self.sampling_frequency_available
        try:
            if rate in frequencies:
                self._set_iio_attr("voltage1", "sampling_frequency", False, rate)
        except Exception as error:
            return error

    @property
    def scale_volt1(self):
        """AD7746 channel scale(gain)"""
        return float(self._get_iio_attr_str("voltage1", "scale", False))

    @property
    def supply_raw(self):
        """AD7746 supply raw value"""
        return self._get_iio_attr("voltage1", "supply_raw", False)

    @property
    def calibbias_cap0(self):
        """AD7746 channel calibration bias"""
        return self._get_iio_attr("capacitance0", "calibbias", False)

    @calibbias_cap0.setter
    def calibbias_cap0(self, value):
        self._set_iio_attr("capacitance0", "calibbias", False, value)

    @property
    def calibscale_cap0(self):
        return self._get_iio_attr("capacitance0", "calibscale", False)

    @calibscale_cap0.setter
    def calibscale_cap0(self, value):
        self._set_iio_attr("capacitance0", "calibscale", False, value)

    @property
    def offset_cap0(self):
        return self._get_iio_attr("capacitance0", "offset", False)

    @property
    def raw_cap0(self):
        """AD7747 capacitance channel raw value"""
        return self._get_iio_attr("capacitance0", "raw", False)

    @property
    def scale_cap0(self):
        """AD7746 capacitance channel scale(gain)"""
        return float(self._get_iio_attr_str("capacitance0", "scale", False))

    @property
    def sampling_frequency_cap0(self):
        return self._get_iio_attr("capacitance0", "sampling_frequency", False)

    @sampling_frequency_cap0.setter
    def sampling_frequency_cap0(self, rate):
        frequencies = self.sampling_frequency_available
        try:
            if rate in frequencies:
                self._set_iio_attr("capacitance0", "sampling_frequency", False, rate)
        except Exception as error:
            return error

    @property
    def calibbias_cap1(self):
        """AD7746 channel calibration bias"""
        return self._get_iio_attr("capacitance1", "calibbias", False)

    @calibbias_cap1.setter
    def calibbias_cap1(self, value):
        self._set_iio_attr("capacitance1", "calibbias", False, value)

    @property
    def calibscale_cap1(self):
        return self._get_iio_attr("capacitance1", "calibscale", False)

    @calibscale_cap1.setter
    def calibscale_cap1(self, value):
        self._set_iio_attr("capacitance1", "calibscale", False, value)

    @property
    def offset_cap1(self):
        return self._get_iio_attr("capacitance1", "offset", False)

    @property
    def raw_cap1(self):
        """AD7747 capacitance channel raw value"""
        return self._get_iio_attr("capacitance1", "raw", False)

    @property
    def scale_cap1(self):
        """AD7746 capacitance channel scale(gain)"""
        return float(self._get_iio_attr_str("capacitance1", "scale", False))

    @property
    def sampling_frequency_cap1(self):
        return self._get_iio_attr("capacitance1", "sampling_frequency", False)

    @sampling_frequency_cap1.setter
    def sampling_frequency_cap1(self, rate):
        frequencies = self.sampling_frequency_available
        try:
            if rate in frequencies:
                self._set_iio_attr("capacitance1", "sampling_frequency", False, rate)
        except Exception as error:
            return error
