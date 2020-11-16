import pytest

hardware = "fmcadc2"
classname = "adi.ad9625"


@pytest.mark.parametrize("classname, hardware", [(classname, hardware)])
@pytest.mark.parametrize("channel", [0])
def test_ad9625_rx_data(test_dma_rx, classname, hardware, channel):
    test_dma_rx(classname, hardware, channel)
