# Copyright (C) 2020 Analog Devices, Inc.
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
import time

import iio

from adi.rx_tx import phy


class multichip(phy):
    """ class type for devices with multichip capability"""

    slave: iio.Device = []

    def __init__(self, slave):
        if isinstance(slave, list):
            self.slave = slave
        else:
            self.slave = [slave]
        self.num_slaves = len(self.slave)

    def multichip_sync(self, sampling_sync=True, interface_sync=True):
        mcs_is_debug_attr = self._get_iio_debug_attr_str("multichip_sync") is not None
        if sampling_sync:
            tx_sample_freq = self._get_iio_attr("voltage0", "sampling_frequency", True)
            for slave in self.slave:
                tx_sample_freq_chip_b = self._get_iio_attr(
                    "voltage0", "sampling_frequency", True, slave
                )
                if tx_sample_freq != tx_sample_freq_chip_b:
                    # Set same sampling frequency
                    self._set_iio_attr(
                        "voltage0", "sampling_frequency", True, tx_sample_freq, slave
                    )
        if interface_sync:
            tmp = self._ctrl.reg_read(6)
            tmp2 = self._ctrl.reg_read(7)
            for slave in self.slave:
                slave.reg_write(6, tmp)
                slave.reg_write(7, tmp2)

        ensm = self._get_iio_dev_attr_str("ensm_mode")
        self._set_iio_dev_attr_str("ensm_mode", "alert")
        ensm_chip_b = []
        for index, slave in enumerate(self.slave):
            ensm_chip_b.append(self._get_iio_dev_attr_str("ensm_mode", slave))
            self._set_iio_dev_attr_str("ensm_mode", "alert", slave)

        for i in range(5):
            for slave in self.slave:
                if mcs_is_debug_attr:
                    self._set_iio_debug_attr_str("multichip_sync", i, slave)
                else:
                    self._set_iio_dev_attr_str("multichip_sync", i, slave)
            if mcs_is_debug_attr:
                self._set_iio_debug_attr_str("multichip_sync", i)
            else:
                self._set_iio_dev_attr_str("multichip_sync", i)
            time.sleep(0.01)

        self._set_iio_dev_attr_str("ensm_mode", ensm)
        for index, slave in enumerate(self.slave):
            self._set_iio_dev_attr_str("ensm_mode", ensm_chip_b[index], slave)

        def __del__(self):
            self.slave = []
