import pytest

hardware = "ad9434-fmc-500ebz"
classname = "adi.ad9434"


@pytest.mark.parametrize("classname, hardware", [(classname, hardware)])
@pytest.mark.parametrize("channel", 0)
def test_ad9434_rx_data(test_dma_rx, classname, hardware, channel):
    test_dma_rx(classname, hardware, channel)
