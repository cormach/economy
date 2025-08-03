import QuantLib as ql

schedule = ql.Schedule(
    ql.Date(15, 12, 2019),
    ql.Date(15, 12, 2029),
    ql.Period('1Y'),
    ql.TARGET(),
    ql.Unadjusted,
    ql.Unadjusted,
    ql.DateGeneration.Backward,
    False
)

bond = ql.FixedRateBond(
    settlementDays=2,
    faceAmount=100.0,
    schedule=schedule,
    coupons=[0.05],
    paymentDayCounter=ql.ActualActual(ql.ActualActual.Bond),
)
p= bond.cleanPrice(
    0.03,
    ql.ActualActual(ql.ActualActual.Bond),
    ql.Compounded,
    ql.Annual,
)
print(f"Clean Price: {p:.2f}")