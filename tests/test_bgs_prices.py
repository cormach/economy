from bgs.load_bgs_prices import convert_to_float


def test_price_converter():
    tester = "98  27/32"
    result = convert_to_float(tester)
    assert 98.84375 == result
