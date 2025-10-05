import QuantLib as ql
import pandas as pd


def from_iso(date):
    if isinstance(date, pd.Timestamp):
        date = date.strftime("%Y-%m-%d")
    if isinstance(date, ql.Date):
        return date
    return ql.Date(date, "%Y-%m-%d")


def fixed_bond_schedule(
    trade_date, issue_date, maturity_date, first_cpn_date, last_cpn_date
):
    issue_dt = from_iso(issue_date)
    mat_dt = from_iso(maturity_date)
    first_cpn_dt = from_iso(first_cpn_date)
    last_cpn_dt = from_iso(last_cpn_date)
    ql.Settings.instance().evaluationDate = from_iso(trade_date)

    tenor = ql.Period(ql.Semiannual)
    calendar = ql.UnitedKingdom()
    business_convention = ql.Unadjusted
    termination_business_convention = ql.Unadjusted
    date_generation = ql.DateGeneration.Forward
    end_of_month = False

    fbSchedule = ql.Schedule(
        issue_dt,
        mat_dt,
        tenor,
        calendar,
        business_convention,
        termination_business_convention,
        date_generation,
        end_of_month,
        first_cpn_dt,
        last_cpn_dt,
    )

    return fbSchedule


def coupon_schedule(
    trade_date, issue_date, maturity_date, first_cpn_date, last_cpn_date
):
    schedule = fixed_bond_schedule(
        trade_date, issue_date, maturity_date, first_cpn_date, last_cpn_date
    )
    coupons = [d for d in schedule if d > from_iso(trade_date)]
    return coupons


class Gilt(ql.FixedRateBond):

    DAY_COUNT = ql.ActualActual(ql.ActualActual.ISMA)

    def __init__(
        self,
        trade_date,
        issue_date,
        maturity_date,
        first_cpn_date,
        last_cpn_date,
        coupon,
    ):
        trade_dt = from_iso(trade_date)
        issue_dt = from_iso(issue_date)
        mat_dt = from_iso(maturity_date)
        first_cpn_dt = from_iso(first_cpn_date)
        last_cpn_dt = from_iso(last_cpn_date)
        coupon = coupon

        ql.Settings.instance().evaluationDate = from_iso(trade_date)

        fbSchedule = fixed_bond_schedule(
            trade_dt, issue_dt, mat_dt, first_cpn_dt, last_cpn_dt
        )

        cpns = [coupon]

        settle_days = 1
        face_amt = 100.0
        rdm_amt = 100.0

        payment_calendar = ql.UnitedKingdom()
        ex_coupon_period = ql.Period(7, ql.Days)
        ex_coupon_calendar = ql.UnitedKingdom()
        business_convention = ql.Unadjusted

        super().__init__(
            settle_days,
            face_amt,
            fbSchedule,
            cpns,
            self.DAY_COUNT,
            business_convention,
            rdm_amt,
            issue_dt,
            payment_calendar,
            ex_coupon_period,
            ex_coupon_calendar,
        )

    def yield_to_maturity(self, price):
        clean_price = ql.BondPrice(price, ql.BondPrice.Clean)

        return self.bondYield(
            clean_price,
            ql.ActualActual(ql.ActualActual.Bond),
            ql.Compounded,
            ql.Semiannual,
        )

    def price(self, ytm):
        ytm_ql = ql.InterestRate(ytm, self.DAY_COUNT, ql.Compounded, ql.Semiannual)
        return ql.BondFunctions.cleanPrice(self, ytm_ql)


def gilt_yield(
    trade_date,
    issue_date,
    maturity_date,
    first_cpn_date,
    last_cpn_date,
    clean_price,
    coupon,
):

    fixedRateBond = Gilt(
        trade_date,
        issue_date,
        maturity_date,
        first_cpn_date,
        last_cpn_date,
        coupon,
    )

    # price = ql.BondPrice(clean_price, ql.BondPrice.Clean)

    # return (
    #     fixedRateBond.bondYield(
    #         price,
    #         ql.ActualActual(ql.ActualActual.Bond),
    #         ql.Compounded,
    #         ql.Semiannual,
    #     )
    # )

    return fixedRateBond.yield_to_maturity(clean_price)


def yield_series(
    price_series, issue_date, maturity_date, first_cpn_date, last_cpn_date, coupon
):
    # Calculate the yield series based on the provided parameters
    name = price_series.name
    df = price_series.reset_index().rename(columns={name: "price"})
    df["yield"] = df.apply(
        lambda x: gilt_yield(
            trade_date=x["index"].isoformat().split("T")[0],
            issue_date=issue_date,
            maturity_date=maturity_date,
            first_cpn_date=first_cpn_date,
            last_cpn_date=last_cpn_date,
            clean_price=x["price"],
            coupon=coupon / 100,
        ),
        axis=1,
    )
    df.set_index("index", inplace=True)
    return df


CURVE_FITTING = {
    "Nelson/Siegel": ql.NelsonSiegelFitting(),
    "Exp. splines": ql.ExponentialSplinesFitting(True),
    "B splines": ql.CubicBSplinesFitting(
        [
            -30.0,
            -20.0,
            0.0,
            5.0,
            10.0,
            15.0,
            20.0,
            25.0,
            30.0,
            40.0,
            50.0,
        ],
        True,
    ),
    "Svensson": ql.SvenssonFitting(),
}


def yield_curves(trade_date, df: pd.DataFrame):
    """
    https://www.implementingquantlib.com/2024/03/using-quantlib-interactively.html
    """

    helpers = []
    bonds = []
    for i, row in df.iterrows():
        price = row["price"]
        coupon = row["%"] / 100
        issue_date = row["Issue date"]
        maturity = row["Latest redemption date"]
        first_cpn_date = row["First coupon payable on date"]
        last_cpn_date = row[
            "Latest redemption date"
        ]  # list of (start, maturity, coupon, price)

        bond = Gilt(
            trade_date=trade_date,
            issue_date=issue_date,
            maturity_date=maturity,
            first_cpn_date=first_cpn_date,
            last_cpn_date=last_cpn_date,
            coupon=coupon,
        )

        bonds.append(bond)
        helpers.append(ql.BondHelper(ql.QuoteHandle(ql.SimpleQuote(price)), bond))
    discount_curve = ql.RelinkableYieldTermStructureHandle()
    bond_engine = ql.DiscountingBondEngine(discount_curve)
    for b in bonds:
        b.setPricingEngine(bond_engine)

    tolerance = 1e-8
    max_iterations = 5000
    day_count = ql.ActualActual(ql.ActualActual.Bond)

    curves = {
        tag: ql.FittedBondDiscountCurve(
            from_iso(trade_date),
            helpers,
            day_count,
            CURVE_FITTING[tag],
            # tolerance,
            # max_iterations,
        )
        for tag in CURVE_FITTING
    }
    return curves


def yield_curves_pw(trade_date, df: pd.DataFrame):
    """
    https://www.implementingquantlib.com/2024/03/using-quantlib-interactively.html
    """

    helpers = []
    bonds = []
    for i, row in df.iterrows():
        price = row["price"]
        coupon = row["%"] / 100
        issue_date = row["Issue date"]
        maturity = row["Latest redemption date"]
        first_cpn_date = row["First coupon payable on date"]
        last_cpn_date = row[
            "Latest redemption date"
        ]  # list of (start, maturity, coupon, price)

        bond = Gilt(
            trade_date=trade_date,
            issue_date=issue_date,
            maturity_date=maturity,
            first_cpn_date=first_cpn_date,
            last_cpn_date=last_cpn_date,
            coupon=coupon,
        )

        bonds.append(bond)
        helpers.append(ql.BondHelper(ql.QuoteHandle(ql.SimpleQuote(price)), bond))
    discount_curve = ql.RelinkableYieldTermStructureHandle()
    bond_engine = ql.DiscountingBondEngine(discount_curve)
    for b in bonds:
        b.setPricingEngine(bond_engine)

    tolerance = 1e-8
    max_iterations = 5000
    day_count = ql.ActualActual(ql.ActualActual.Bond)
    params = [from_iso(trade_date), helpers, day_count]

    piecewiseMethods = {
        "logLinearDiscount": ql.PiecewiseLogLinearDiscount(*params),
        "logCubicDiscount": ql.PiecewiseLogCubicDiscount(*params),
        "linearZero": ql.PiecewiseLinearZero(*params),
        "cubicZero": ql.PiecewiseCubicZero(*params),
        "linearForward": ql.PiecewiseLinearForward(*params),
        "splineCubicDiscount": ql.PiecewiseSplineCubicDiscount(*params),
    }
    return piecewiseMethods


def yield_curve(trade_date, df: pd.DataFrame, method="Nelson/Siegel"):
    """
    https://www.implementingquantlib.com/2024/03/using-quantlib-interactively.html
    """

    helpers = []
    bonds = []
    for i, row in df.iterrows():
        price = row["price"]
        coupon = row["%"] / 100
        issue_date = row["Issue date"]
        maturity = row["Latest redemption date"]
        first_cpn_date = row["First coupon payable on date"]
        last_cpn_date = row[
            "Latest redemption date"
        ]  # list of (start, maturity, coupon, price)

        bond = Gilt(
            trade_date=trade_date,
            issue_date=issue_date,
            maturity_date=maturity,
            first_cpn_date=first_cpn_date,
            last_cpn_date=last_cpn_date,
            coupon=coupon,
        )

        bonds.append(bond)
        helpers.append(ql.BondHelper(ql.QuoteHandle(ql.SimpleQuote(price)), bond))
    discount_curve = ql.RelinkableYieldTermStructureHandle()
    bond_engine = ql.DiscountingBondEngine(discount_curve)
    for b in bonds:
        b.setPricingEngine(bond_engine)

    method = CURVE_FITTING[method]

    tolerance = 1e-8
    max_iterations = 5000
    day_count = ql.ActualActual(ql.ActualActual.Bond)

    curve = ql.FittedBondDiscountCurve(
        from_iso(trade_date),
        helpers,
        day_count,
        method,
        # tolerance,
        # max_iterations,
    )

    return curve


def yield_curve_rv(trade_date, df: pd.DataFrame, method="Nelson/Siegel"):
    """
    https://www.implementingquantlib.com/2024/03/using-quantlib-interactively.html
    """

    helpers = []
    bonds = []

    for i, row in df.iterrows():
        price = row["price"]
        coupon = row["%"] / 100
        issue_date = row["Issue date"]
        maturity = row["Latest redemption date"]
        first_cpn_date = row["First coupon payable on date"]
        last_cpn_date = row[
            "Latest redemption date"
        ]  # list of (start, maturity, coupon, price)

        bond = Gilt(
            trade_date=trade_date,
            issue_date=issue_date,
            maturity_date=maturity,
            first_cpn_date=first_cpn_date,
            last_cpn_date=last_cpn_date,
            coupon=coupon,
        )

        bonds.append(bond)
        helpers.append(ql.BondHelper(ql.QuoteHandle(ql.SimpleQuote(price)), bond))

    discount_curve = ql.RelinkableYieldTermStructureHandle()
    bond_engine = ql.DiscountingBondEngine(discount_curve)
    for b in bonds:
        b.setPricingEngine(bond_engine)

    method = CURVE_FITTING[method]

    tolerance = 1e-8
    max_iterations = 5000
    day_count = ql.ActualActual(ql.ActualActual.Bond)

    curve = ql.FittedBondDiscountCurve(
        from_iso(trade_date),
        helpers,
        day_count,
        method,
        # tolerance,
        # max_iterations,
    )
    dates = [
        from_iso(x)
        for x in [
            x.strftime("%Y-%m-%d") for x in df["Latest redemption date"].to_list()
        ]
    ]
    fitted_yields = [curve.zeroRate(d, day_count, ql.Continuous).rate() for d in dates]

    df["curve_yield"] = fitted_yields

    # discount_curve.linkTo(curve)
    # fitted_prices = [b.cleanPrice() for b in bonds]
    # df['curve_price'] = fitted_prices
    # fitted_yields = [b.bondYield(day_count, ql.Compounded, ql.Semiannual) for b in bonds]
    # df['curve_yields'] = fitted_yields

    rate = [
        ql.InterestRate(x, day_count, ql.Compounded, ql.Semiannual)
        for x in fitted_yields
    ]
    bond_prices = [ql.BondFunctions.cleanPrice(b, rate[i]) for i, b in enumerate(bonds)]

    df["curve_price"] = bond_prices

    return df


def yield_curve_pw(trade_date, df: pd.DataFrame):
    """
    https://www.implementingquantlib.com/2024/03/using-quantlib-interactively.html
    """

    helpers = []
    bonds = []
    for i, row in df.iterrows():
        price = row["price"]
        coupon = row["%"] / 100
        issue_date = row["Issue date"]
        maturity = row["Latest redemption date"]
        first_cpn_date = row["First coupon payable on date"]
        last_cpn_date = row[
            "Latest redemption date"
        ]  # list of (start, maturity, coupon, price)

        bond = Gilt(
            trade_date=trade_date,
            issue_date=issue_date,
            maturity_date=maturity,
            first_cpn_date=first_cpn_date,
            last_cpn_date=last_cpn_date,
            coupon=coupon,
        )

        bonds.append(bond)
        helpers.append(ql.BondHelper(ql.QuoteHandle(ql.SimpleQuote(price)), bond))
    # discount_curve = ql.RelinkableYieldTermStructureHandle()
    # bond_engine = ql.DiscountingBondEngine(discount_curve)
    # for b in bonds:
    #     b.setPricingEngine(bond_engine)

    tolerance = 1e-8
    max_iterations = 5000
    day_count = ql.ActualActual(ql.ActualActual.Bond)
    params = [from_iso(trade_date), helpers, day_count]

    #     piecewiseMethods = {
    #     'logLinearDiscount': ql.PiecewiseLogLinearDiscount(*params),
    #     'logCubicDiscount': ql.PiecewiseLogCubicDiscount(*params),
    #     'linearZero': ql.PiecewiseLinearZero(*params),
    #     'cubicZero': ql.PiecewiseCubicZero(*params),
    #     'linearForward': ql.PiecewiseLinearForward(*params),
    #     'splineCubicDiscount': ql.PiecewiseSplineCubicDiscount(*params),
    # }
    return ql.PiecewiseLinearZero(*params)


def yield_curves_pw_2(trade_date, df: pd.DataFrame):
    """
    https://www.implementingquantlib.com/2024/03/using-quantlib-interactively.html
    """

    helpers = []
    bonds = []
    for i, row in df.iterrows():
        price = row["price"]
        coupon = row["%"] / 100
        issue_date = row["Issue date"]
        maturity = row["Latest redemption date"]
        first_cpn_date = row["First coupon payable on date"]
        last_cpn_date = row[
            "Latest redemption date"
        ]  # list of (start, maturity, coupon, price)

        quote = ql.QuoteHandle(ql.SimpleQuote(price))
        settlementDays = 1
        faceAmount = 100
        schedule = fixed_bond_schedule(
            from_iso(trade_date),
            from_iso(issue_date),
            from_iso(maturity),
            from_iso(first_cpn_date),
            from_iso(last_cpn_date),
        )
        coupons = [coupon]
        dayCounter = ql.ActualActual(ql.ActualActual.Bond)
        helper = ql.FixedRateBondHelper(
            quote, settlementDays, faceAmount, schedule, coupons, dayCounter
        )

        helpers.append(helper)
    discount_curve = ql.RelinkableYieldTermStructureHandle()
    bond_engine = ql.DiscountingBondEngine(discount_curve)
    for b in bonds:
        b.setPricingEngine(bond_engine)

    tolerance = 1e-8
    max_iterations = 5000
    day_count = ql.ActualActual(ql.ActualActual.Bond)
    params = [from_iso(trade_date), helpers, day_count]

    piecewiseMethods = {
        "logLinearDiscount": ql.PiecewiseLogLinearDiscount(*params),
        "logCubicDiscount": ql.PiecewiseLogCubicDiscount(*params),
        "linearZero": ql.PiecewiseLinearZero(*params),
        "cubicZero": ql.PiecewiseCubicZero(*params),
        "linearForward": ql.PiecewiseLinearForward(*params),
        "splineCubicDiscount": ql.PiecewiseSplineCubicDiscount(*params),
    }
    return piecewiseMethods
