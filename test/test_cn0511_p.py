import pytest

hardware = "cn0511"
classname = "adi.CN0511"


#########################################
@pytest.mark.parametrize("classname, hardware", [(classname, hardware)])
@pytest.mark.parametrize(
    "attr, val, tol",
    [
        (
            "frequency",
            [
                1,
                100000,
                100000000,
                500000001,
                1000000001,
                1400000001,
                1800000000,
                2200000000,
            ],
            8,
        ),
        (
            "raw",
            [0, 2 ** 10, 2 ** 11 - 1, 2 ** 12, 2 ** 13 - 1, 2 ** 14, 2 ** 15 - 1,],
            8,
        ),
        ("amp_enable", [True, False], 0),
    ],
)
def test_cn0511_attr(
    attribute_multipe_values, classname, hardware, attr, values, tol,
):
    attribute_multipe_values(
        classname, hardware, attr, values, tol,
    )
