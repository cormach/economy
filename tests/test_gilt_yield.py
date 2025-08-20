from bgs.gilt_analytics import gilt_yield

def test_yld():
    today = "2023-08-15"
    issue_date = "2008-09-03"
    maturity_date = "2049-12-07"
    first_cpn_date = "2008-12-07"
    last_cpn_date = "2049-12-07"
    clean_price = 91.660
    coupon = .0425

    yld = gilt_yield(today, issue_date, maturity_date, first_cpn_date, last_cpn_date, clean_price, coupon)

    assert round(yld,6) == 4.811837 # 4.811837 on tradeweb eod prices