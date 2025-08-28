import QuantLib as ql

import pandas as pd

# https://www.quantlibguide.com/Inflation%20indexes%20and%20curves.html
# # https://stackoverflow.com/a/34436705


def ql_date(d):
    iso_ts = pd.to_datetime(d, format="%Y %b")
    return ql.Date(iso_ts.day, iso_ts.month, iso_ts.year)


def ql_inflation_list(ons_rpi_idx, cal, trade_date):
    rpi_idx = ons_rpi_idx.copy()
    rpi_idx["date"] = rpi_idx["date"].apply(ql_date)
    inflation_list = list(
        rpi_idx.loc[
            rpi_idx["date"] < cal.advance(trade_date, -1, ql.Months)
        ].itertuples(index=False, name=None)
    )
    return inflation_list


def linker_real_yield(
    trade_date,
    ons_rpi_idx,
    settlement_days,
    inflation_quotes,
    notional,
    issue_date,
    maturity_date,
    fixedRates,
    clean_price,
    first_coupon_date,
):
    ql.Settings.instance().evaluationDate = trade_date
    rpi = ql.UKRPI()
    calendar = ql.UnitedKingdom()
    ex_coupon_period = ql.Period(7, ql.Days)
    ex_coupon_calendar = ql.UnitedKingdom()

    inflation_list = ql_inflation_list(ons_rpi_idx, calendar, trade_date)

    for date, fixing in inflation_list:
        rpi.addFixing(date, fixing)

    lag = 3
    observation_lag = ql.Period(lag, ql.Months)
    day_counter = ql.ActualActual(ql.ActualActual.ISMA)
    interpolation = ql.CPI.Linear

    nominal_curve = ql.YieldTermStructureHandle(
        ql.FlatForward(trade_date, 0.05, day_counter)
    )

    helpers = []

    for tenor, quote in inflation_quotes:
        maturity = calendar.advance(trade_date, tenor)
        helpers.append(
            ql.ZeroCouponInflationSwapHelper(
                ql.makeQuoteHandle(quote / 100),
                observation_lag,
                maturity,
                calendar,
                ql.Following,
                day_counter,
                rpi,
                interpolation,
                nominal_curve,
            )
        )

    fixing_frequency = ql.Monthly

    inflation_curve = ql.PiecewiseZeroInflation(
        referenceDate=trade_date,
        baseDate=rpi.lastFixingDate(),
        frequency=fixing_frequency,
        dayCounter=ql.Actual365Fixed(),
        instruments=helpers,
    )

    inflation_handle = ql.RelinkableZeroInflationTermStructureHandle(inflation_curve)

    rpi = ql.UKRPI(inflation_handle)

    fixedDayCounter = ql.Actual365Fixed()
    fixedPaymentConvention = ql.ModifiedFollowing
    fixedPaymentCalendar = ql.UnitedKingdom()
    contractObservationLag = ql.Period(3, ql.Months)
    observationInterpolation = ql.CPI.Linear
    settlementDays = settlement_days
    growthOnly = False

    baseCPI = rpi.pastFixing(calendar.advance(issue_date, -2, ql.Months))

    fixedSchedule = ql.Schedule(
        issue_date,
        maturity_date,
        ql.Period(ql.Semiannual),
        fixedPaymentCalendar,
        ql.Unadjusted,
        ql.Unadjusted,
        ql.DateGeneration.Forward,
        False,
        first_coupon_date,
    )

    bond = ql.CPIBond(
        settlementDays=settlementDays,
        faceAmount=notional,
        growthOnly=growthOnly,
        baseCPI=baseCPI,
        observationLag=contractObservationLag,
        cpiIndex=rpi,
        observationInterpolation=observationInterpolation,
        schedule=fixedSchedule,
        coupons=fixedRates,
        accrualDayCounter=fixedDayCounter,
        paymentConvention=fixedPaymentConvention,
        exCouponPeriod=ex_coupon_period,
        paymentCalendar=ql.UnitedKingdom(),
        exCouponCalendar=ex_coupon_calendar,
    )

    bondEngine = ql.DiscountingBondEngine(nominal_curve)
    bond.setPricingEngine(bondEngine)

    compounding = ql.Compounded

    cashflows = [
        (cf.amount(), cf.date())
        for cf in bond.cashflows()
        if not cf.hasOccurred(bond.settlementDate())
    ]

    cpn = fixedRates[0]

    def real_price(rho):

        # Number of calendar days from the settlement date to the next quasi-coupon date r
        days_to_next_coupon = cashflows[0][1] - bond.settlementDate()

        # number of full days between quasi-coupon dates s
        previous_coupon = [s for s in fixedSchedule.until(bond.settlementDate())][-2]
        next_coupon = cashflows[0][1]
        year_ahead_coupon_date = cashflows[1][1]
        days_between_coupon = next_coupon - previous_coupon
        # print(previous_coupon, next_coupon, year_ahead_coupon_date)
        year_count = year_ahead_coupon_date - previous_coupon
        # print((days_between_coupon -1) / year_count)
        # print((year_ahead_coupon_date - next_coupon +1) / year_count)

        # Cash flow due on next quasi-coupon date, per £100 nominal of the gilt (may be zero if the gilt has a long first dividend period or if the gilt     settles in its ex-dividend period; or may be greater or less than 2 c      times the RPI Ratio during long or short first dividend periods      respectively).
        # d_1 = cpn * 100 / 2
        d_1 = cpn * 100 * (days_between_coupon - 1) / year_count

        # Cash flow due on next but one quasi-coupon date, per £100 nominal of the gilt (may be greater than 2 c times the RPI Ratio during     long first dividend periods)4.
        d_2 = cpn * 100 / 2
        # d_2 = cpn  * 100 *(year_ahead_coupon_date - next_coupon +1) / year_count
        # coupon per £100 nominal

        # number of full quasi-coupon periods from the next quasi-coupon date after the settlement date to the redemption date
        number_cpns = len(cashflows) - 2
        # Semi-annually compounded real redemption yield (decimal)

        # discount factor
        w_df = 1 / (1 + rho / 2)

        # Real dirty price per £100 nominal
        price = w_df ** (days_to_next_coupon / days_between_coupon) * (
            d_1
            + d_2 * w_df
            + cpn
            * 100
            * (w_df**2.0)
            * (1 - w_df ** (number_cpns - 1))
            / (2 * (1 - w_df))
            + 100 * w_df**number_cpns
        )

        # real_accrued = cpn  * 100 *  (days_between_coupon - days_to_next_coupon) / year_count

        real_accrued = (
            cpn
            / 2
            * 100
            * (days_between_coupon - days_to_next_coupon)
            / days_between_coupon
        )
        return price - real_accrued

    def find_rho(rho):
        rho = clean_price - real_price(rho=rho)
        return rho

    solver = ql.Brent()

    accuracy = 1e-7
    guess = 0.01
    step = 0.00001
    r = solver.solve(find_rho, accuracy, guess, step)

    return r


if __name__ == "__main__":

    df_ons_rpi = pd.read_csv("downloads/ONSRPI.csv", header=7, names=["date", "RPI"])
    monthly_start = df_ons_rpi[df_ons_rpi["date"] == "1987 JAN"].index[0]
    ons_rpi_index = df_ons_rpi.iloc[monthly_start:].copy()

    df_infl = pd.ExcelFile("downloads/GLC Inflation month end data_2016 to 2024.xlsx")
    df_spot = pd.read_excel(
        df_infl, sheet_name="4. spot curve", header=3, skiprows=[4]
    ).set_index("years:")
    date = "15/08/2023"

    previous_month_end = (
        pd.to_datetime(date, format="%d/%m/%Y") + pd.offsets.MonthEnd(-1)
    ).strftime("%Y-%m-%d")
    infl_curve = df_spot.loc[df_spot.index == previous_month_end].to_dict(orient="list")

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
        ons_rpi_idx=ons_rpi_index,
        settlement_days=1,
        inflation_quotes=inflation_quotes,
        notional=notional,
        issue_date=issue_date,
        first_coupon_date=first_coupon_date,
        maturity_date=maturity_date,
        fixedRates=fixed_rates,
        clean_price=clean_price,
    )
    print(r)
    # 1.386613
