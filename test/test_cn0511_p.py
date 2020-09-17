import pytest

hardware = "cn0511"
classname = "adi.CN0511"


#########################################
@pytest.mark.parametrize("classname, hardware", [(classname, hardware)])
@pytest.mark.parametrize(
    "attr, start, stop, step, tol",
    [
        ("frequency", 1, 500000000, 1, 8),
        ("frequency", 600000000, 1000000000, 1, 8),
        ("frequency", 1100000000, 2000000000, 1, 8),
        ("raw", 1, 2 ** 15 - 1, 1, 8),
    ],
)
def test_cn0511_attr(
    test_attribute_single_value,
    classname,
    hardware,
    attr,
    start,
    stop,
    step,
    tol,
    param_set,
):
    test_attribute_single_value(
        classname, hardware, attr, start, stop, step, tol, param_set
    )

