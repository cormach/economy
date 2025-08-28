import pytest
import pandas as pd
from bgs.linker_analytics import linker_real_yield

"""
Gilt Name,Close of Business Date,ISIN,Type,Coupon,Maturity,Clean Price,Dirty Price,Yield,Mod Duration,Accrued Interest
UKGI 0.125 03/24,15/08/2023,GB00B85SFQ54,Index-linked,0.125,22/03/2024,97.846,151.771979,3.786369,0.589073,0.077412
UKGI 0.125 03/26,15/08/2023,GB00BYY5F144,Index-linked,0.125,22/03/2026,96.114,139.952179,1.657916,2.574389,0.072669
UKGI 1.25 11/27,15/08/2023,GB00B128DH60,Index-linked,1.25,22/11/2027,100.456,195.109816,1.140085,4.132878,0.565722
UKGI 0.125 08/28,15/08/2023,GB00BZ1NTB69,Index-linked,0.125,10/08/2028,95.565,128.627499,1.040485,4.943536,0.002743
UKGI 0.125 03/29,15/08/2023,GB00B3Y1JG82,Index-linked,0.125,22/03/2029,95.124,150.658431,1.023029,5.550864,0.079041
UKGI 0.125 08/31,15/08/2023,GB00BNNGP551,Index-linked,0.125,10/08/2031,95.086,121.719345,0.760549,7.914991,0.002609
UKGI 1.25 11/32,15/08/2023,GB00B3D4VD98,Index-linked,1.25,22/11/2032,103.775,180.128737,0.825945,8.729635,0.505627
UKGI 0.75 11/33,15/08/2023,GB00BMF9LJ15,Index-linked,0.75,22/11/2033,98.56,99.611932,0.897134,9.842668,0.100828
UKGI 0.75 03/34,15/08/2023,GB00B46CGH68,Index-linked,0.75,22/03/2034,97.74,158.664335,0.974907,10.123791,0.484851
UKGI 0.125 11/36,15/08/2023,GB00BYZW3J87,Index-linked,0.125,22/11/2036,88.31,127.685497,1.072721,13.07768,0.042223
UKGI 1.125 11/37,15/08/2023,GB00B1L6W962,Index-linked,1.125,22/11/2037,99.85,186.041818,1.136389,13.110419,0.488566
UKGI 0.125 03/39,15/08/2023,GB00BLH38265,Index-linked,0.125,22/03/2039,84.34,106.888288,1.23139,15.333436,0.063244
UKGI 0.625 03/40,15/08/2023,GB00B3LZBF68,Index-linked,0.625,22/03/2040,90.73,157.918855,1.244818,15.601724,0.43335
UKGI 0.125 08/41,15/08/2023,GB00BGDYHF49,Index-linked,0.125,10/08/2041,81.82,109.805175,1.257709,17.649645,0.002735
UKGI 0.625 11/42,15/08/2023,GB00B3MYD345,Index-linked,0.625,22/11/2042,88.67,157.108504,1.291116,17.948387,0.258368
UKGI 0.125 03/44,15/08/2023,GB00B7RN0G65,Index-linked,0.125,22/03/2044,77.88,120.816332,1.359783,20.14787,0.077411
UKGI 0.625 03/45,15/08/2023,GB00BMF9LH90,Index-linked,0.625,22/03/2045,85.81,88.808951,1.387539,19.915732,0.19468
UKGI 0.125 03/46,15/08/2023,GB00BYMWG366,Index-linked,0.125,22/03/2046,75.59,110.275457,1.386866,22.060672,0.072796
UKGI 0.75 11/47,15/08/2023,GB00B24FFM16,Index-linked,0.75,22/11/2047,86.92,157.548379,1.386613,21.844264,0.317053
UKGI 0.125 08/48,15/08/2023,GB00BZ13DV40,Index-linked,0.125,10/08/2048,73.68,100.774187,1.373071,24.352453,0.002787
UKGI 0.5 03/50,15/08/2023,GB00B421JZ66,Index-linked,0.5,22/03/2050,80.75,142.565423,1.365469,24.465213,0.351753
UKGI 0.125 03/51,15/08/2023,GB00BNNGP882,Index-linked,0.125,22/03/2051,71.77,91.775818,1.354258,26.82401,0.063806
UKGI 0.25 03/52,15/08/2023,GB00B73ZYW09,Index-linked,0.25,22/03/2052,74.3,115.521413,1.333803,27.189386,0.15506
UKGI 1.25 11/55,15/08/2023,GB00B0CNHZ09,Index-linked,1.25,22/11/2055,99.34,194.822639,1.274995,26.382337,0.571216
UKGI 0.125 11/56,15/08/2023,GB00BYVP4K94,Index-linked,0.125,22/11/2056,69.97,99.319082,1.227211,32.203085,0.041448
UKGI 0.125 03/58,15/08/2023,GB00BP9DLZ64,Index-linked,0.125,22/03/2058,69.35,101.930456,1.212181,33.446167,0.073337
UKGI 0.375 03/62,15/08/2023,GB00B4PTCY75,Index-linked,0.375,22/03/2062,76.21,121.691553,1.138322,35.193889,0.238724
UKGI 0.125 11/65,15/08/2023,GB00BD9MZZ71,Index-linked,0.125,22/11/2065,68.25,98.533731,1.058704,40.635654,0.042156
UKGI 0.125 03/68,15/08/2023,GB00BDX8CX86,Index-linked,0.125,22/03/2068,67.97,102.379521,1.020794,42.790053,0.075155
UKGI 0.125 03/73,15/08/2023,GB00BM8Z2W66,Index-linked,0.125,22/03/2073,71.74,87.509773,0.819524,47.513593,0.060866
"""


@pytest.fixture
def monthly_rpi_index():
    df_ons_rpi = pd.read_csv("downloads/ONSRPI.csv", header=7, names=["date", "RPI"])
    monthly_start = df_ons_rpi[df_ons_rpi["date"] == "1987 JAN"].index[0]
    ons_rpi_index = df_ons_rpi.iloc[monthly_start:].copy()
    return ons_rpi_index


@pytest.fixture
def inflation_spot_curve():
    import openpyxl

    df_infl = pd.ExcelFile("downloads/GLC Inflation month end data_2016 to 2024.xlsx")
    df_spot = pd.read_excel(
        df_infl, sheet_name="4. spot curve", header=3, skiprows=[4]
    ).set_index("years:")
    return df_spot


def test_linker(monthly_rpi_index, inflation_spot_curve):
    # Tradeweb closing prices
    # UKGI 0.75 11/47	15/08/2023	GB00B24FFM16	Index-linked	0.750	22/11/2047	86.920	157.548379	1.386613	21.844264	0.317053

    import QuantLib as ql

    date = "15/08/2023"

    previous_month_end = (
        pd.to_datetime(date, format="%d/%m/%Y") + pd.offsets.MonthEnd(-1)
    ).strftime("%Y-%m-%d")
    infl_curve = inflation_spot_curve.loc[
        inflation_spot_curve.index == previous_month_end
    ].to_dict(orient="list")

    inflation_quotes = [
        (ql.Period(key, ql.Years), value[0])
        for key, value in infl_curve.items()
        if key * 2 // 2 == key
    ]

    today = ql.Date(date, "dd/MM/yyyy")
    issue_date = ql.Date(22, ql.November, 2007)
    first_coupon_date = ql.Date(22, ql.May, 2008)
    maturity_date = ql.Date(22, ql.November, 2047)
    notional = 100
    fixed_rates = [0.0075]

    clean_price = 86.92

    r = linker_real_yield(
        trade_date=today,
        ons_rpi_idx=monthly_rpi_index,
        settlement_days=1,
        inflation_quotes=inflation_quotes,
        notional=notional,
        issue_date=issue_date,
        maturity_date=maturity_date,
        fixedRates=fixed_rates,
        clean_price=clean_price,
        first_coupon_date=first_coupon_date,
    )
    assert round(r, 8) == 0.01386613

    # GB00B128DH60
    issue_date = ql.Date(26, ql.April, 2006)
    first_coupon_date = ql.Date(22, ql.November, 2006)
    maturity_date = ql.Date(22, ql.November, 2027)
    notional = 100
    fixed_rates = [0.0125]

    clean_price = 100.456

    r = linker_real_yield(
        trade_date=today,
        ons_rpi_idx=monthly_rpi_index,
        settlement_days=1,
        inflation_quotes=inflation_quotes,
        notional=notional,
        issue_date=issue_date,
        maturity_date=maturity_date,
        fixedRates=fixed_rates,
        clean_price=clean_price,
        first_coupon_date=first_coupon_date,
    )
    assert round(r, 8) == 0.01140085

    # UKGI 0.125 08/48	15/08/2023	GB00BZ13DV40	Index-linked	0.125	10/08/2048	73.680	100.774187	1.373071

    issue_date = ql.Date(8, ql.November, 2017)
    first_coupon_date = ql.Date(10, ql.February, 2018)
    maturity_date = ql.Date(10, ql.August, 2048)
    # TODO: the cashflows roll versus the issue date not the maturity date
    notional = 100
    fixed_rates = [0.00125]

    clean_price = 73.60

    r = linker_real_yield(
        trade_date=today,
        ons_rpi_idx=monthly_rpi_index,
        settlement_days=1,
        inflation_quotes=inflation_quotes,
        notional=notional,
        issue_date=issue_date,
        maturity_date=maturity_date,
        fixedRates=fixed_rates,
        clean_price=clean_price,
        first_coupon_date=first_coupon_date,
    )
    assert round(r, 8) == 0.01373071
