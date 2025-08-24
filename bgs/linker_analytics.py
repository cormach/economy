import QuantLib as ql
import datetime as dt

# https://www.quantlibguide.com/Inflation%20indexes%20and%20curves.html

# today = ql.Date(11, ql.May, 2024)
# ql.Settings.instance().evaluationDate = today

# hicp = ql.EUHICP()

# inflation_fixings = [
#     ((2022, ql.January), 110.70),
#     ((2022, ql.February), 111.74),
#     ((2022, ql.March), 114.46),
#     ((2022, ql.April), 115.11),
#     ((2022, ql.May), 116.07),
#     ((2022, ql.June), 117.01),
#     ((2022, ql.July), 117.14),
#     ((2022, ql.August), 117.85),
#     ((2022, ql.September), 119.26),
#     ((2022, ql.October), 121.03),
#     ((2022, ql.November), 120.95),
#     ((2022, ql.December), 120.52),
#     ((2023, ql.January), 120.27),
#     ((2023, ql.February), 121.24),
#     ((2023, ql.March), 122.34),
#     ((2023, ql.April), 123.12),
#     ((2023, ql.May), 123.15),
#     ((2023, ql.June), 123.47),
#     ((2023, ql.July), 123.36),
#     ((2023, ql.August), 124.03),
#     ((2023, ql.September), 124.43),
#     ((2023, ql.October), 124.54),
#     ((2023, ql.November), 123.85),
#     ((2023, ql.December), 124.05),
#     ((2024, ql.January), 123.60),
#     ((2024, ql.February), 124.37),
#     ((2024, ql.March), 125.31),
#     ((2024, ql.April), 126.05),
# ]

# for (year, month), fixing in inflation_fixings:
#     hicp.addFixing(ql.Date(1, month, year), fixing)

# inflation_quotes = [
#     (ql.Period(1, ql.Years), 2.93),
#     (ql.Period(2, ql.Years), 2.95),
#     (ql.Period(3, ql.Years), 2.965),
#     (ql.Period(4, ql.Years), 2.98),
#     (ql.Period(5, ql.Years), 3.0),
#     (ql.Period(7, ql.Years), 3.06),
#     (ql.Period(10, ql.Years), 3.175),
#     (ql.Period(12, ql.Years), 3.243),
#     (ql.Period(15, ql.Years), 3.293),
#     (ql.Period(20, ql.Years), 3.338),
#     (ql.Period(25, ql.Years), 3.348),
#     (ql.Period(30, ql.Years), 3.348),
#     (ql.Period(40, ql.Years), 3.308),
#     (ql.Period(50, ql.Years), 3.228),
# ]

# calendar = ql.TARGET()
# observation_lag = ql.Period(3, ql.Months)
# day_counter = ql.Thirty360(ql.Thirty360.BondBasis)
# interpolation = ql.CPI.Linear

# nominal_curve = ql.YieldTermStructureHandle(
#     ql.FlatForward(today, 0.03, ql.Actual365Fixed())
# )

# helpers = []

# for tenor, quote in inflation_quotes:
#     maturity = calendar.advance(today, tenor)
#     helpers.append(
#         # ql.ZeroCouponInflationSwapHelper(
#         #     quote=ql.makeQuoteHandle(quote / 100),
#         #     lag=observation_lag,
#         #     maturity=maturity,
#         #     calendar=calendar,
#         #     bcd=ql.Following,
#         #     dayCounter=day_counter,
#         #     index=hicp,
#         #     observationInterpolation=interpolation,
#         # )
#         ql.ZeroCouponInflationSwapHelper(
#             ql.makeQuoteHandle(quote / 100),
#             observation_lag,
#             maturity,
#             calendar,
#             ql.Following,
#             day_counter,
#             hicp,
#             interpolation,
#             nominal_curve,
#         )
#     )

# fixing_frequency = ql.Monthly

# inflation_curve = ql.PiecewiseZeroInflation(
#     referenceDate=today,
#     baseDate=hicp.lastFixingDate(),
#     frequency=fixing_frequency,
#     dayCounter=ql.Actual365Fixed(),
#     instruments=helpers,
# )

# # https://stackoverflow.com/a/34436705

today = ql.Date(9, ql.October, 2009)

calendar = ql.UnitedKingdom()
evaluationDate = calendar.adjust(today)
ql.Settings.instance().evaluationDate = evaluationDate

rpi = ql.UKRPI()

inflation_fixings = [
    ((2007, ql.July), 206.1),
    ((2007, ql.August), 207.3),
    ((2007, ql.September), 208.0),
    ((2007, ql.October), 208.9),
    ((2007, ql.November), 209.7),
    ((2007, ql.December), 210.9),
    ((2008, ql.January), 209.8),
    ((2008, ql.February), 211.4),
    ((2008, ql.March), 212.1),
    ((2008, ql.April), 214.0),
    ((2008, ql.May), 215.1),
    ((2008, ql.June), 216.8),
    ((2008, ql.July), 216.5),
    ((2008, ql.August), 217.2),
    ((2008, ql.September), 218.4),
    ((2008, ql.October), 217.7),
    ((2008, ql.November), 216.0),
    ((2008, ql.December), 212.9),
    ((2009, ql.January), 210.1),
    ((2009, ql.February), 211.4),
    ((2009, ql.March), 211.3),
    ((2009, ql.April), 211.5),
    ((2009, ql.May), 212.8),
    ((2009, ql.June), 213.4),
    ((2009, ql.July), 213.4),
    ((2009, ql.August), 213.4),
    ((2009, ql.September), 214.4),
]

for (year, month), fixing in inflation_fixings:
    rpi.addFixing(ql.Date(1, month, year), fixing)

inflation_quotes = [
    (ql.Period(1, ql.Years), 3.0495),
    (ql.Period(2, ql.Years), 2.93),
    (ql.Period(3, ql.Years), 2.9795),
    (ql.Period(4, ql.Years), 3.029),
    (ql.Period(5, ql.Years), 3.1425),
    (ql.Period(6, ql.Years), 3.211),
    (ql.Period(7, ql.Years), 3.2675),
    (ql.Period(8, ql.Years), 3.3625),
    (ql.Period(9, ql.Years), 3.405),
    (ql.Period(10, ql.Years), 3.48),
    (ql.Period(12, ql.Years), 3.576),
    (ql.Period(15, ql.Years), 3.649),
    (ql.Period(20, ql.Years), 3.751),
    (ql.Period(25, ql.Years), 3.77225),
    (ql.Period(30, ql.Years), 3.77),
    (ql.Period(40, ql.Years), 3.734),
    (ql.Period(50, ql.Years), 3.714),
]

lag = 3
observation_lag = ql.Period(lag, ql.Months)
day_counter = ql.ActualActual(ql.ActualActual.ISMA)
interpolation = ql.CPI.Linear

nominal_curve = ql.YieldTermStructureHandle(
    ql.FlatForward(evaluationDate, 0.04, day_counter)
)

helpers = []


for tenor, quote in inflation_quotes:
    maturity = calendar.advance(today, tenor)
    helpers.append(
        #         ql.ZeroCouponInflationSwapHelper(
        #             quote=ql.makeQuoteHandle(quote / 100),
        #             swapObsLag=observation_lag,
        #             maturity=maturity_date,
        #             calendar=calendar,
        #             paymentConvention=ql.Following,
        #             dayCounter=day_counter,
        #             zii=rpi,
        #             observationInterpolation=interpolation,
        #             nominalTermStructure=nominal_curve,
        #         )
        #     )
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
    referenceDate=evaluationDate,
    baseDate=rpi.lastFixingDate(),
    frequency=fixing_frequency,
    dayCounter=ql.Actual365Fixed(),
    instruments=helpers,
)

inflation_handle = ql.RelinkableZeroInflationTermStructureHandle(inflation_curve)

rpi = ql.UKRPI(inflation_handle)

notional = 1000000
issue_date = ql.Date(22, ql.May, 2007)
maturity_date = ql.Date(21, ql.November, 2047)
fixing_date = calendar.advance(evaluationDate, -lag, ql.Months)

fixedRates = [0.0075]

fixedDayCounter = ql.Actual365Fixed()
fixedPaymentConvention = ql.ModifiedFollowing
fixedPaymentCalendar = ql.UnitedKingdom()
contractObservationLag = ql.Period(3, ql.Months)
observationInterpolation = ql.CPI.Linear
settlementDays = 3
growthOnly = False

baseCPI = rpi.pastFixing(calendar.advance(issue_date, -lag, ql.Months))


fixedSchedule = ql.Schedule(
    issue_date,
    maturity_date,
    ql.Period(ql.Semiannual),
    fixedPaymentCalendar,
    ql.Unadjusted,
    ql.Unadjusted,
    ql.DateGeneration.Backward,
    False,
)

bond = ql.CPIBond(
    settlementDays,
    notional,
    growthOnly,
    baseCPI,
    contractObservationLag,
    rpi,
    observationInterpolation,
    fixedSchedule,
    fixedRates,
    fixedDayCounter,
    fixedPaymentConvention,
)

# #bond2= ql.QuantLib.C

bondEngine = ql.DiscountingBondEngine(nominal_curve)
bond.setPricingEngine(bondEngine)
# print(bond.NPV())
clean_price = 99.75
price = ql.BondPrice(clean_price, ql.BondPrice.Clean)
print(bond.cleanPrice())
# print ("Dirty Price:", bond.dirtyPrice())
compounding = ql.Compounded
yield_rate = bond.bondYield(price, fixedDayCounter, compounding, ql.Semiannual)

print("Yield:", yield_rate)

cashflows = [
    (cf.amount(), cf.date())
    for cf in bond.cashflows()
    if not cf.hasOccurred(bond.settlementDate())
]

print(cashflows[0])
print(cashflows[1])
print(len(cashflows))
print(bond.settlementDate())
print([s for s in fixedSchedule.until(bond.settlementDate())])
# DMO

# Number of calendar days from the settlement date to the next quasi-coupon date r
days_to_next_coupon = cashflows[0][1] - bond.settlementDate()
print("Days to next coupon:", days_to_next_coupon)
# number of full days between quasi-coupon dates s
days_between_coupon = cashflows[0][1] - [s for s in fixedSchedule.until(bond.settlementDate())][-2] 
print("Days between coupon:", days_between_coupon)
# Cash flow due on next quasi-coupon date, per £100 nominal of the     gilt (may be zero if the gilt has a long first dividend period or if the gilt     settles in its ex-dividend period; or may be greater or less than 2 c      times the RPI Ratio during long or short first dividend periods      respectively).
d_1 = 0.0
# Cash flow due on next but one quasi-coupon date, per £100      nominal of the gilt (may be greater than 2 c times the RPI Ratio during     long first dividend periods)4.
d_2 = 0.0
# coupon per £100 nominal
cpn_ = 0.0
# number of full quasi-coupon periods from the next quasi-coupon date after the settlement date to the redemption date
number_cpns = 0.0
# Semi-annually compounded real redemption yield (decimal)
_rho = 0.025
# discount factor
w_df = 1 / (1 + _rho / 2)

# Real dirty price per £100 nominal
price = w_df ** (days_to_next_coupon / days_between_coupon) * (
    d_1
    + d_2 * w_df
    + cpn_ * (w_df**2.0) * (1 - w_df * (number_cpns - 1)) / (2 * (1 - w_df))
    + 100 * w_df**number_cpns
)
