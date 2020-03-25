import pytest

hardware = "ad9265"
classname = "adi.ad9265"

#########################################
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize(
    "attr, val",
    [
        (
            "test_mode",
            [
                "midscale_short",
                "pos_fullscale",
                "neg_fullscale",
                "checkerboard",
                "pn_long",
                "pn_short",
                "one_zero_toggle",
                "off",
            ],
        )
    ],
)
def test_ad9265_str_attr(test_attribute_multipe_values, iio_uri, classname, attr, val):
    test_attribute_multipe_values(iio_uri, classname, attr, val, 0)


#########################################
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize("channel", [0])
def test_ad9265_rx_data(test_dma_rx, iio_uri, classname, channel):
    test_dma_rx(iio_uri, classname, channel)
