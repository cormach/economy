import QuantLib as ql

def from_iso(date):
    return ql.Date(date, "%Y-%m-%d")


def gilt_yield(today, issue_date, maturity_date, first_cpn_date, last_cpn_date, clean_price, coupon):
    issue_dt = from_iso(issue_date)
    mat_dt = from_iso(maturity_date)
    first_cpn_dt = from_iso(first_cpn_date)
    last_cpn_dt = from_iso(last_cpn_date)
    ql.Settings.instance().evaluationDate = from_iso(today)

    price = ql.BondPrice(clean_price, ql.BondPrice.Clean)

    tenor=ql.Period(ql.Semiannual)
    calendar=ql.UnitedKingdom()
    business_convention=ql.Unadjusted
    termination_business_convention=ql.Unadjusted
    date_generation=ql.DateGeneration.Forward
    end_of_month=False
    coupon = .0425

    fbSchedule=ql.Schedule(issue_dt, 
                        mat_dt,
                        tenor,
                        calendar,
                        business_convention,
                        termination_business_convention,
                        date_generation,
                        end_of_month,
                        first_cpn_dt,
                        last_cpn_dt)
    sch = [x for x in fbSchedule]
    fbSchedule = ql.Schedule(
        sch,
        calendar,
        business_convention,
        termination_business_convention,
        tenor,
        date_generation,
        end_of_month,
        [True] * (len(sch)-1)
    )
    cpns = [coupon]

    settle_days=1
    face_amt = 100.
    rdm_amt = 100.

    payment_calendar = ql.UnitedKingdom()
    ex_coupon_period = ql.Period(7, ql.Days)
    ex_coupon_calendar = ql.UnitedKingdom()

    fixedRateBond = ql.FixedRateBond(
        settle_days,
        face_amt,
        fbSchedule,
        cpns,
        ql.ActualActual(ql.ActualActual.ISMA),
        business_convention,
        rdm_amt,
        issue_dt,
        payment_calendar,
        ex_coupon_period,
        ex_coupon_calendar,
    )

    return (fixedRateBond.bondYield(price, ql.ActualActual(ql.ActualActual.Bond),
        ql.Compounded,
        ql.Semiannual,)*100)
