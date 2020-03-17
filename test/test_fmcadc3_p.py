import pytest

hardware = "fmcadc3"
classname = "adi.fmcadc3"


@pytest.mark.parametrize("classname, hardware", [(classname, hardware)])
@pytest.mark.parametrize("channel", [0])
def test_fmcadc3_rx_data(test_dma_rx, classname, hardware, channel):
    test_dma_rx(classname, hardware, channel)