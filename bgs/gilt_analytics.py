import QuantLib as ql

settlementDays=2
calendar=ql.TARGET()
faceAmount=100.0
startDate=ql.Date(15,12,2019)
maturityDate=ql.Date(15,12,2024)
tenor=ql.Period('1Y')
coupon=[0.05]
paymentConvention=ql.ActualActual(ql.ActualActual.Bond)
schedule = ql.MakeSchedule(startDate, maturityDate, tenor)

bond = ql.FixedRateBond(
    settlementDays=settlementDays,
    faceAmount=faceAmount,
    schedule=schedule,
    coupons=coupon,
    paymentConvention=paymentConvention,
    issueDate=startDate,
    paymentDayCounter=ql.ActualActual(ql.ActualActual.Bond),
    maturityDate=maturityDate,
    )