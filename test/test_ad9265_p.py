import pytest

hardware = "ad9265-125ebz"
classname = "adi.ad9265"


@pytest.mark.parametrize("classname, hardware", [(classname, hardware)])
@pytest.mark.parametrize("channel", 0)
def test_ad9265_rx_data(test_dma_rx, classname, hardware, channel):
    test_dma_rx(classname, hardware, channel)
