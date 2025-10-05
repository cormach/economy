from unittest.mock import mock_open, patch
import pandas as pd

from bgs.load_gilt_details import load_csv_blocks
import logging

logger = logging.getLogger(__name__)


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
END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END
Worksheet name:,,STRIPS,Last Updated December 2023,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,END
Strips,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,END
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,END
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,END
Sequence,Inst Code,ISIN Code,%,Stock,Suffix,Special features,First year,Last year,Issue date,First coupon payable on date,Earliest redemption date,Latest redemption date,"A (B, C ...) stock merged on date",Actually redeemed,Frequency,Payment date 1,Payment date 2,Payment date 3,Payment date 4,First coupon,Col for I-L,Col for I-L,Col for I-L,Col for I-L,Col for I-L,Number of calls,Call payment 1,due on,Call payment 2,due on,Call payment 3,due on,Call payment 4,due on,,,END
60000,UKT07JUN1998C,GB0000504471,,UK Treasury Strip 07JUN1998C ,,,,1998,,,,7 Jun 1998,,7 Jun 1998,,,,,,,,,,,,,,,,,,,,,,,END
END,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,END
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,END
END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END,END"""

    with patch("builtins.open", mock_open(read_data=mock_csv_content)):
        result = load_csv_blocks("dummy_path.csv")

    conv = pd.DataFrame(
        {
            "Sequence": ["100", "32700"],
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
            "Col for I-L 1": ["", ""],
            "Col for I-L 2": ["", ""],
            "Col for I-L 3": ["", ""],
            "Col for I-L 4": ["", ""],
            "Col for I-L 5": ["", ""],
            "Number of calls": ["", ""],
            "Call payment 1": ["", ""],
            "due on 1": ["", ""],
            "Call payment 2": ["", ""],
            "due on 2": ["", ""],
            "Call payment 3": ["", ""],
            "due on 3": ["", ""],
            "Call payment 4": ["", ""],
            "due on 4": ["", ""],
        }
    )

    il = pd.DataFrame(
        {
            "Sequence": ["55200", "55800"],
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
            "due on 1": ["", ""],
            "Call payment 2": ["", ""],
            "due on 2": ["", ""],
            "Call payment 3": ["", ""],
            "due on 3": ["", ""],
            "Call payment 4": ["", ""],
            "due on 4": ["", ""],
            "": ["", ""],
        }
    )

    old_style = pd.DataFrame(
        {
            "Sequence": ["50000", "51900"],
            "Inst Code": ["2IL88", "2IL35"],
            "Sedol": ["", "3179082"],
            "ISIN Code": ["", "GB0031790826"],
            "%": ["2", "2"],
            "Stock": ["Index-linked", "Index-linked"],
            "Suffix": ["", ""],
            "Special features": ["", ""],
            "First year": ["", ""],
            "Last year": ["1988", "2035"],
            "Issue date": ["19 Mar 1982", "11 Jul 2002"],
            "First coupon payable on date": ["30 Sep 1982", "26 Jan 2003"],
            "Earliest redemption date": ["", ""],
            "Latest redemption date": ["30 Mar 1988", "26 Jan 2035"],
            "A (B, C ...) stock merged on date": ["", ""],
            "Actually redeemed": ["30 Mar 1988", ""],
            "Frequency": ["2", "2"],
            "Payment date 1": ["30 Mar", "26 Jan"],
            "Payment date 2": ["30 Sep", "26 Jul"],
            "Payment date 3": ["", ""],
            "Payment date 4": ["", ""],
            "First coupon": ["0.9996", "1.099091"],
            "IL coupon rounding": ["4", "6"],
            "IL redemption rounding": ["4", "6"],
            "Indexing lag": ["8", "8"],
            "Base month": ["Jul 1981", "Nov 2001"],
            "Base RPI": ["75.310520", "173.6"],
            "Number of calls": ["2", ""],
            "Call payment 1": ["50", ""],
            "due on 1": ["19 Mar 1982", ""],
            "Call payment 2": ["47.5", ""],
            "due on 2": ["29 Apr 1982", ""],
            "Call payment 3": ["", ""],
            "due on 3": ["", ""],
            "Call payment 4": ["", ""],
            "due on 4": ["", ""],
            "": ["", ""],
        }
    )

    assert len(result) == 4
    assert set(result.keys()) == set(
        ["Conventionals", "Index-Linked New-style", "Index-Linked Old-style", "Strips"]
    )

    assert result["Conventionals"].equals(conv)
    assert result["Index-Linked New-style"].equals(il)
    assert result["Index-Linked Old-style"].equals(old_style)
