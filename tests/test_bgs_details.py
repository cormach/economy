from unittest.mock import mock_open, patch
import pandas as pd

from bgs.load_gilt_details import load_csv_blocks, process_index_linked_stocks


def test_load_details():
    mock_csv_content = """Worksheet name:,,Details,Last Updated 31Dec2024,,,New Stocks in Bold,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,END
Conventional stocks,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,END
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,END
,New Stocks in Bold,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,END
Sequence,Inst Code,Sedol,ISIN Code,%,Stock,Suffix,Special features,First year,Last year,Issue date,First coupon payable on date,Earliest redemption date,Latest redemption date,"A (B, C ...) stock merged on date",Actually redeemed or amalgamated,Frequency,Payment date 1,Payment date 2,Payment date 3,Payment date 4,First coupon,Last coupon,Col for I-L,Col for I-L,Col for I-L,Col for I-L,Col for I-L,Number of calls,Call payment 1,due on,Call payment 2,due on,Call payment 3,due on,Call payment 4,due on,END
100,4HCV64,,,4.5,Conversion,,,,1964,15 Jan 1959,14 May 1959,,14 May 1964,,14 May 1964,2,14 May,14 Nov,,,1.470800,,,,,,,,,,,,,,,,END
32700,2TAN,,GB0000436294,2.75,Annuities,,Redemption 5/7/2015 announced 27/3/2015,,,1 Jan 1900,,,,,5 Jul 2015,4,5 Jan,5 Apr,5 Jul,5 Oct,,0.6875,,,,,,,,,,,,,,,END
Worksheet name:,,IL Details,Last Updated 30 June 2023,,,IL Details,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,END
Index linked stocks,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,END
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,END
Sequence,Inst Code,Sedol,ISIN Code,%,Stock,Suffix,Special features,First year,Last year,Issue date,First coupon payable on date,Earliest redemption date,Latest redemption date,"A (B, C ...) stock merged on date",Actually redeemed,Frequency,Payment date 1,Payment date 2,Payment date 3,Payment date 4,First coupon,IL coupon rounding,IL redemption rounding,Indexing lag,Base month,Base RPI,Number of calls,Call payment 1,due on,Call payment 2,due on,Call payment 3,due on,Call payment 4,due on,,END
Old-style,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,END
50000,2IL88,,,2,Index-linked,,,,1988,19 Mar 1982,30 Sep 1982,,30 Mar 1988,,30 Mar 1988,2,30 Mar,30 Sep,,,0.9996,4,4,8,Jul 1981,75.310520,2,50,19 Mar 1982,47.5,29 Apr 1982,,,,,,END
51900,2IL35,3179082,GB0031790826,2,Index-linked,,,,2035,11 Jul 2002,26 Jan 2003,,26 Jan 2035,,,2,26 Jan,26 Jul,,,1.099091,6,6,8,Nov 2001,173.6,,,,,,,,,,,END
New-style,,,,,,,,,,,,,,,,,,,,,unindexed,,,,,interpolated,,,,,,,,,,,END
55200,1QIL17,B0V3WQ7,GB00B0V3WQ75,1.25,Index-linked,,,,2017,8 Feb 2006,22 May 2006,,22 Nov 2017,,22 Nov 2017,2,22 May,22 Nov,,,0.355663,,,,,193.72500,,,,,,,,,,,END
55800,0AIL73,BM8Z2W6,GB00BM8Z2W66,0.125,Index-linked,,,,2073,24 Nov 2021,22 Mar 2022,,22 Mar 2073,,,2,22 Mar,22 Sep,,,??,,,,,,,,,,,,,,,,END
END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END"""

    with patch("builtins.open", mock_open(read_data=mock_csv_content)):
        result = load_csv_blocks("dummy_path.csv")

    pd.DataFrame(
        {
            "Inst Code": ["4HCV64", "2TAN"],
            "Sedol": ["", ""],
            "ISIN Code": ["", "GB0000436294"],
            "%": ["4.5", "2.75"],
            "Stock": ["Conversion", "Annuities"],
            "Suffix": ["", ""],
            "Special features": ["", "Redemption 5/7/2015 announced 27/3/2015"],
            "First year": ["", ""],
            "Last year": ["1964", ""],
            "Issue date": ["15 Jan 1959", "1 Jan 1900"],
            "First coupon payable on date": ["14 May 1959", ""],
            "Earliest redemption date": ["", ""],
            "Latest redemption date": ["14 May 1964", ""],
            "A (B, C ...) stock merged on date": ["", ""],
            "Actually redeemed or amalgamated": ["14 May 1964", "5 Jul 2015"],
            "Frequency": ["2", "4"],
            "Payment date 1": ["14 May", "5 Jan"],
            "Payment date 2": ["14 Nov", "5 Apr"],
            "Payment date 3": ["", "5 Jul"],
            "Payment date 4": ["", "5 Oct"],
            "First coupon": ["1.470800", ""],
            "Last coupon": ["", "0.6875"],
            "Col for I-L": ["", ""],
            "Number of calls": ["", ""],
            "Call payment 1": ["", ""],
            "due on": ["", ""],
            "Call payment 2": ["", ""],
            "Call payment 3": ["", ""],
            "Call payment 4": ["", ""],
        },
        index=["100", "32700"],
    )

    pd.DataFrame(
        {
            "Inst Code": ["1QIL17", "0AIL73"],
            "Sedol": ["B0V3WQ7", "BM8Z2W6"],
            "ISIN Code": ["GB00B0V3WQ75", "GB00BM8Z2W66"],
            "%": ["1.25", "0.125"],
            "Stock": ["Index-linked", "Index-linked"],
            "Suffix": ["", ""],
            "Special features": ["", ""],
            "First year": ["", ""],
            "Last year": ["2017", "2073"],
            "Issue date": ["8 Feb 2006", "24 Nov 2021"],
            "First coupon payable on date": ["22 May 2006", "22 Mar 2022"],
            "Earliest redemption date": ["", ""],
            "Latest redemption date": ["22 Nov 2017", "22 Mar 2073"],
            "A (B, C ...) stock merged on date": ["", ""],
            "Actually redeemed": ["22 Nov 2017", ""],
            "Frequency": ["2", "2"],
            "Payment date 1": ["22 May", "22 Mar"],
            "Payment date 2": ["22 Nov", "22 Sep"],
            "Payment date 3": ["", ""],
            "Payment date 4": ["", ""],
            "First coupon": ["0.355663", "??"],
            "IL coupon rounding": ["", ""],
            "IL redemption rounding": ["", ""],
            "Indexing lag": ["", ""],
            "Base month": ["", ""],
            "Base RPI": ["193.72500", ""],
            "Number of calls": ["", ""],
            "Call payment 1": ["", ""],
            "due on": ["", ""],
            "Call payment 2": ["", ""],
            "Call payment 3": ["", ""],
            "Call payment 4": ["", ""],
            "": ["", ""],
        },
        index=["55200", "55800"],
    )

    assert "Conventionals" in result
    assert "Index-Linked New-style" in result
    assert len(result) == 3
