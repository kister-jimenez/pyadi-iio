import pytest

hardware = "daq2"
classname = "adi.DAQ2"


#########################################
@pytest.mark.parametrize("classname, hardware", [(classname, hardware)])
@pytest.mark.parametrize("channel", [0, 1, [0, 1]])
def test_daq2_tx_data(test_dma_tx, classname, hardware, channel):
    test_dma_tx(classname, hardware, channel)


#########################################
@pytest.mark.parametrize("classname, hardware", [(classname, hardware)])
@pytest.mark.parametrize("channel", [0, 1, [0, 1]])
def test_daq2_rx_data(test_dma_rx, classname, hardware, channel):
    test_dma_rx(classname, hardware, channel)


#########################################
@pytest.mark.parametrize("classname, hardware", [(classname, hardware)])
@pytest.mark.parametrize("channel", [0, 1])
@pytest.mark.parametrize("frequency, scale", [(200000000, 0.5)])
@pytest.mark.parametrize("param_set", [dict()])
@pytest.mark.parametrize("peak_min", [-40])
def test_daq2_dds_loopback(
    test_dds_loopback,
    classname,
    hardware,
    param_set,
    channel,
    frequency,
    scale,
    peak_min,
):
    test_dds_loopback(
        classname, hardware, param_set, channel, frequency, scale, peak_min
    )
